---
title: YouTube Video Notifier
description: Polls YouTube channels for new videos and sends Slack notifications
integrations: ["youtube", "slack"]
categories: ["Productivity"]
tags: ["Polling", "notifications", "memory vars"]
---

# YouTube Video Poller

monitoring of YouTube channels for new video uploads by integrating YouTube Data API and Slack for instant notifications.

API documentation:

- Slack: https://docs.autokitteh.com/integrations/slack

## How It Works

1. Polls a specified YouTube channel using a scheduled trigger
2. Compares new videos against the last check timestamp
3. Sends Slack notifications with details for any newly detected videos
4. Updates the last checked timestamp to track state

## Cloud Usage

1. Initialize your connections (YouTube and Slack)
2. Set environment variables:
   - `YOUTUBE_CHANNEL_NAME`: The YouTube channel to monitor (default: "autokitteh")
   - `SLACK_CHANNEL`: The Slack channel for notifications (default: "#general")
3. Deploy project

> [!IMPORTANT]
> Ensure all connections (YouTube and Slack) are initialized.

## Trigger Workflow

The project automatically starts polling every 5 minutes once deployed.

> [!NOTE]
> scheduler timing can be changed in the trigger section by editing the trigger

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- Relies on scheduled polling rather than real-time webhooks
- Uses YouTube channel search which may have API rate limits
- First run sets baseline timestamp without reporting existing videos
