"""Web scraping with ScrapingBee to fetch news articles and post summaries to Slack."""

import os
from scrapingbee import ScrapingBeeClient
from bs4 import BeautifulSoup
from autokitteh.slack import slack_client

SB_API_KEY = os.getenv("SB_API_KEY")
NEWS_WEBSITE_URL = os.getenv("NEWS_WEBSITE_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#news")

client = ScrapingBeeClient(api_key=SB_API_KEY)
slack = slack_client("slack_conn")


def on_app_mention(event):
    """Fetch news articles and post summaries to Slack."""
    if not NEWS_WEBSITE_URL:
        print("NEWS_WEBSITE_URL not set")
        return

    feed = client.get(
        NEWS_WEBSITE_URL, params={"render_js": False, "block_resources": True}
    )
    if feed.status_code != 200:
        slack.chat_postMessage(
            channel=SLACK_CHANNEL,
            text=f"Failed to fetch news feed: HTTP {feed.status_code}",
        )
        print("Feed fetch failed:", feed.status_code)
        return

    soup = BeautifulSoup(feed.content, "xml")
    items = soup.select("item")[:5]

    if not items:
        slack.chat_postMessage(
            channel=SLACK_CHANNEL,
            text="No news items found in the feed.",
        )
        print("No items found in feed.")
        return

    slack.chat_postMessage(
        channel=SLACK_CHANNEL,
        text="News Digest",
        blocks=build_blocks(items),
    )


def extract_excerpt(html):
    """Best-effort article body extraction."""
    soup = BeautifulSoup(html, "html.parser")
    body = (
        soup.select_one('[data-gu-name="body"]')
        or soup.select_one("article")
        or soup.select_one('[itemprop="articleBody"]')
    )
    text = body.get_text(" ", strip=True) if body else ""
    return text[:400] + ("…" if len(text) > 400 else "")


def build_blocks(items):
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "Top Headlines"}},
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Source: <{NEWS_WEBSITE_URL}|RSS>"}
            ],
        },
        {"type": "divider"},
    ]

    for item in items:
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        r = client.get(link, params={"render_js": False, "block_resources": True})
        excerpt = (
            extract_excerpt(r.content)
            if r.status_code == 200
            else "_Unable to fetch article_"
        )

        blocks += [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*<{link}|{title}>*\n{excerpt}"},
            },
            {"type": "divider"},
        ]
    return blocks
