---
title: ScrapingBee News Digest
description: Fetch news from RSS feeds and post article summaries to Slack using ScrapingBee
integrations: ["slack"]
categories: ["Samples"]
tags: ["web_scraping"]
---

# ScrapingBee News Digest

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=scrapingbee_fetch_news)

This sample demonstrates how to use ScrapingBee to fetch and scrape news articles from RSS feeds, then post formatted digests to Slack.

API details:

- [ScrapingBee API](https://www.scrapingbee.com/documentation/)
- [Python client library](https://github.com/ScrapingBee/scrapingbee-python)

## How It Works

1. Bot is mentioned in a Slack channel
2. Fetches the latest articles from the configured RSS feed
3. Scrapes full article content using ScrapingBee
4. Extracts excerpts from each article
5. Posts a formatted digest with top 5 headlines to Slack

## Cloud Usage

1. Initialize your Slack connection through the UI
2. Configure project variables:
   - `SB_API_KEY`: Your ScrapingBee API key (required)
   - `NEWS_URL`: RSS feed URL (optional, defaults to The Guardian)
   - `SLACK_CHANNEL`: Target Slack channel (optional, defaults to `#news`)

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Slack connection is initialized; otherwise, the workflow will raise a `ConnectionInitError`.

Mention the bot in any Slack channel where it's present:

```
@YourBotName
```

The bot will respond with a news digest containing the top 5 articles from your configured RSS feed.

> [!NOTE]
> You can customize the RSS feed by setting the `NEWS_URL` variable to any valid RSS feed URL (e.g., BBC News, TechCrunch, Hacker News).

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

Not all URLs may work. Some websites may return errors or be inaccessible during scraping attempts.
