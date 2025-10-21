---
title: Gmail new email notification
description: Poll for new emails in Gmail inbox and handle them with custom logic
integrations: ["gmail"]
categories: ["Productivity"]
---

# Gmail New Email Notification

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=walkthroughs/new_gmail_notification)

This AutoKitteh project demonstrates how to create a custom Gmail event system that triggers when new emails arrive. It uses polling to detect new messages and processes them with custom logic.

API Documentation

- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events

## How It Works

1. Polls Gmail inbox every 15 minutes using a scheduled trigger (timing can be changed in trigger settings)
2. Tracks the last known message ID to detect new emails
3. Processes new messages by extracting headers and details
4. Handles multiple new messages in batch processing

## Cloud Usage

1. Initialize your connection with Gmail
2. Deploy project

## Trigger Workflow

The workflow runs automatically every 15 minutes via scheduled trigger. You can also manually trigger it:

1. Deploy the project and wait for the scheduled trigger to run
2. Send yourself a new email
3. Wait up to 1 hour for the next polling cycle to detect it

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases
- **Scheduled trigger**: runs every 15 minutes, so there may be a delay in detecting new emails
- **History ID**: due to limitations in Gmail's native history ID event handling, this project uses a custom polling approach
