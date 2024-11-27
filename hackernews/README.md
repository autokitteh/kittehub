---
title: Hackernews Alert with Slack 
description: A bot that tracks Hacker News articles by topic and sends updates to Slack.
integrations: ["slack"]
categories: ["Office Automation"]
---


# Hackernews Slack Sample

This project monitors Hacker News for new articles matching a specific topic, fetching their details in real-time. It compares the latest results with previously fetched articles to identify new ones and sends their title and URL as notifications to a Slack channel.

## API Documentation

- Slack connection. https://docs.autokitteh.com/integrations/slack.
- Fetches articles from Hacker News. https://www.algolia.com/doc/api-reference/rest-api.

## Setup Instructions

1. Set the `SLACK_CHANNEL` environment value

2. Via the ak CLI tool or the AutoKitteh VS Code extension, deploy the autokitteh.yaml manifest file, or you can use the cloud version for easy deployment and management.

## Usage Instruction 

- Type `/your_slack_app` `topic` in the Slack channel you set in the environment variable, replacing `topic` with what you want to search for, to start tracking articles.

