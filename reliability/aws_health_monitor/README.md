---
title: AWS Health monitor
description: Announce AWS Health events in Slack channels, based on resource ownership data in a Google Sheet
integrations: ["aws", "slack", "googlesheets"]
categories: ["Reliability"]
tags: ["activity", "scheduled_tasks", "monitoring", "notifications", "data_processing", "essential"]
---

# AWS Health Monitor

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=reliability/aws_health_monitor)

Announce AWS health events in Slack channels, based on resource ownership data in a Google Sheet.

This leverages the AWS Health API to fetch events, and Google Sheets to map AWS project tags to Slack channels.

API documentation:

- https://docs.aws.amazon.com/health/
- https://aws.amazon.com/blogs/mt/tag/aws-health-api/

## How It Works

1. Poll the AWS Health API once a minute to detect new events
2. Read tag-to-Slack-channel mappings from a Google Sheet
3. Post relevant health events to the corresponding Slack channels, based on step 2

## Google Sheets Configuration

The Google Sheet format for mapping project tags to Slack channels:

| Project Tag | Slack Channel   |
| :---------- | :-------------- |
| clubs       | clubs_team      |
| diamonds    | diamonds_alerts |
| hearts      | hearts_oncall   |
| spades      | C12345678       |

Read-only template: https://docs.google.com/spreadsheets/d/1PalmLwSZOPW9k668_jU-wFI5xCj88a4mDfNUtJAupMQ/

## Cloud Usage

1. Initialize your connections (AWS, Google Sheets, Slack)
2. Set the `GOOGLE_SHEET_URL` project variable (based on the [Google Sheets Configuration](#google-sheets-configuration) section above)
3. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all the connections (AWS, Google Sheets, Slack) are properly initialized; otherwise the workflow will raise a `ConnectionInitError`.
>
> Also ensure the `GOOGLE_SHEET_URL` project variable is configured correctly, and the Google Sheet is properly formatted; otherwise the workflow may not work as expected.

After the project is deployed, the workflow runs automatically at the beginning of every minute.

You may modify this by modifying the `TRIGGER_INTERVAL` project variable and the `schedule` field in the trigger.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
