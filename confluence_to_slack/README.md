---
title: Slack notify on Confluence page created
description: When Confluence page is created the user will be notified on Slack
integrations: ["confluence", "slack"]
categories: ["DevOps"]
tags:
  ["webhook_handling", "notifications", "data_processing", "event_filtering"]
---

# Confluence To Slack Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=confluence_to_slack)

This workflow automates notifications to a Slack channel whenever a new Confluence page is created in a specified space.

## How It Works

1. Create a new Confluence page in a designated space.
2. Send a Slack message to a selected channel containing data from the newly created Confluence page.

## Known Limitations

- Confluence returns HTML, and this program does not format it in any way. The purpose of this workflow is to demonstrate how data can move between different services. Desired formatting can be easily added to suit individual needs.

## Deployment & Configuration

### Cloud Usage (Recommended)

1. Initialize your connections
2. Navigate to the "TRIGGERS" tab and under the "Actions" column click "Edit"
3. Update the "CONFLUENCE_SPACE_KEY" placeholder in the filter string, with the ID of the Confluence space you want to monitor
4. Set/modify these project variables:

   - `FILTER_LABEL` (optional): a specific Confluence page label you limit this project to
   - `SLACK_CHANNEL_NAME_OR_ID`: the Slack channel you want to send messages to

5. Deploy the project

> [!IMPORTANT]
> Ensure all connections (Atlassian Confluence, Slack) are properly initialized before the workflow starts running.

## Trigger Workflow

Once the project has been properly installed, configured and deployed, the workflow will be triggered by an event from Confluence.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
