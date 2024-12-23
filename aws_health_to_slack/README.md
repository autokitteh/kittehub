---
title: AWS Health to Slack
description: Monitor AWS health events
integrations: ["aws", "slack", "sheets"]
categories: ["DevOps"]
---

# Announce AWS Health Events in Slack

This project automates the process of announcing AWS health events in Slack based on resource ownership listed in a Google Sheet. It leverages AWS Health API to fetch events and Google Sheets to map projects to Slack channels. This is not meant to be a complete solution but a solid starting point.

## How It Works

1. Fetches AWS Health events from AWS API.
2. Reads project-to-Slack-channel mappings from a Google Sheet.
3. Posts relevant health events to the corresponding Slack channels based on the Google Sheet data.

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Configure your Google Sheet mapping (see [Google Sheets Configuration](#google-sheets-configuration) below)
3. Deploy the project

## Google Sheets Configuration

The default Google Sheet format for mapping projects to Slack channels:

| Project Tag | Slack Channel      |
|-------------|--------------------|
| clubs       | clubs_team         |
| diamonds    | diamonds_alerts    |
| hearts      | hearts_oncall      |
| spades      | C12345678          |

This table represents how each project is linked to a specific Slack channel, guiding where health events will be posted.

> [!NOTE]
> You can configure your own project-to-Slack-channel mappings by either:
> - Cloud/UI: Navigate to the Variables tab in your project settings and update the `GOOGLE_SHEET_URL` value
> - Self-hosted (VSCode / CLI): Modify the Google Sheet URL in the [`autokitteh.yaml`](autokitteh.yaml) file

## Trigger Workflow

The workflow runs automatically every minute after deployment. You can modify this interval:
- Cloud/UI: Navigate to the Variables tab in your project settings and update the `SCHEDULE_INTERVAL` value
- Self-hosted (VSCode / CLI): Modify the schedule interval in the [`autokitteh.yaml`](autokitteh.yaml) file

> [!IMPORTANT]
> Ensure all connections (AWS, Google Sheets, and Slack) are properly initialized before the workflow starts running.

## Self-Hosted Deployment

#### Prerequisites
- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Google Sheets](https://docs.autokitteh.com/integrations/google)
  - [Slack](https://docs.autokitteh.com/integrations/slack)
  - AWS Health API

#### Installation Steps
1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/aws_health_to_slack
   ```

2. Start the AutoKitteh server:
   ```shell
   ak up --mode dev
   ```

3. Deploy the project:
   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output will show your connection IDs, which you'll need for the next step. Look for lines like:
   ```shell
   [exec] create_connection "aws_health_slack/google_sheets_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```
   
   In this example, `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init aws_connection <connection ID>
   ak connection init google_sheets_connection <connection ID>
   ak connection init slack_connection <connection ID>
   ```
