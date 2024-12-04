"""Monitor Hacker News for new articles on a specific topic, and post updates to a Slack channel."""

import os
import requests
import time
import urllib.parse

from autokitteh.slack import slack_client


slack = slack_client("slack_connection")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")


def on_slack_command(event):
    """
    Workflow's entry-point.

    The function extracts a topic from a Slack command, monitors for new articles,
    and posts updates to the Slack channel.
    """
    topic = event.data.text
    slack.chat_postMessage(
        channel=SLACK_CHANNEL, text=f"Waiting for new articles on the topic: `{topic}`."
    )
    current_articles = set()
    fetch_articles(topic, current_articles)

    # NOTE: For low-traffic topics, it might take a while for new articles to be published,
    # so users may experience delays in receiving notifications.
    while True:
        all_articles = set(current_articles)
        fetch_articles(topic, all_articles)
        new_articles = all_articles - current_articles

        if new_articles:
            for article in new_articles:
                _, title, url = article
                s_message = f"Title: {title}, URL: {url if url else 'No URL'}"
                print(s_message)
                slack.chat_postMessage(channel=SLACK_CHANNEL, text=s_message)
            current_articles.update(new_articles)

        time.sleep(120)


def fetch_articles(topic, all_articles):
    encoded_query = urllib.parse.quote(topic)
    full_url = f"http://hn.algolia.com/api/v1/search_by_date?query={encoded_query}&tags=story&page=0"
    hits = requests.get(full_url).json().get("hits", [])

    # Extract some of the article fields from API response
    for article in hits:
        object_id = article["objectID"]
        title = article["title"]
        url = article.get("url")
        all_articles.add((object_id, title, url))
