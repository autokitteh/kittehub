---
title: ReviewKitteh
description: Monitor a GitHub PR in Slack until it's closed
integrations: ["github", "sheets", "slack"]
categories: ["DevOps"]
---

# ReviewKitteh

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=devops/reviewkitteh)

This project automates the process of listening for GitHub pull request events and posting updates to a Slack channel. The workflow tracks the state of the pull request and meows at random people from a Google Sheet in the Slack channel.

## How It Works

1. Receive [GitHub pull request events](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request) (opened or reopened)
2. Post updates to Slack with an initial message and dynamic updates as the pull request’s status changes
3. Page team members by selecting a random person from a Google Sheet every 15 seconds and notifying them in Slack
4. Conclude workflow when the pull request is closed or merged

## Cloud Usage

1. Initialize your connections (GitHub, Google Sheets, Slack)
2. Set the `SLACK_CHANNEL_ID`, `GOOGLE_SHEET_ID`, and `ORG_DOMAIN` project variables

   > [!IMPORTANT]
   > Use the Slack channel ID (e.g., `C01ABCD2EFG`), not the name (e.g., `#general`).

3. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all the connections (GitHub, Google Sheets, Slack) are properly initialized; otherwise the workflow will raise a `ConnectionInitError`.

After the project is deployed, the workflow is triggered when a GitHub pull request is (re)opened, and continues to run, updating Slack until the pull request is closed or merged.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
