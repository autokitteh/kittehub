---
title: Hacker News alerts in Slack
description: Track Hacker News articles by topic and send updates to Slack
integrations: ["slack"]
categories: ["Productivity"]
tags:
  [
    "user_interactions",
    "long_running",
    "data_processing",
    "notifications",
    "monitoring",
    "webhook_handling",
  ]
---

# Hacker News Alerts in Slack

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=hackernews)

This project monitors Hacker News for new articles matching a specific topic, fetching their details in real-time. It compares the latest results with previously fetched articles to identify new ones and sends their title and URL as notifications to a Slack channel.

## How It Works

1. Extract the topic from the Slack app mention.
2. Add the topic to the Hacker News search query (check out [Algolia's REST API](https://www.algolia.com/doc/api-reference/rest-api) for more details).
3. Return all the new articles related to the topic that were published since the last check.

## Deployment & Configuration

#### Cloud Usage (Recommended)

- Initialize your connection with Slack through the UI

#### Prerequisites

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Slack](https://docs.autokitteh.com/integrations/slack)

## Trigger Workflow

- Type `@your-slack-app topic` in the Slack channel you set in the environment variable, replacing `topic` with what you want to search for, to start tracking articles
- The workflow runs automatically every two minutes after deployment

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
