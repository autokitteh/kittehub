---
title: GitHub issue alert
description: Send GitHub issue comments to Slack
integrations: ["github", "slack"]
categories: ["DevOps"]
---

# GitHub Issue Alert

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=devops/github_issue_alert)

This project automates notifications for GitHub issue activity by monitoring issue creation and comments. It sends real-time updates to a designated Slack channel to keep teams informed.

## How It Works

1. Monitor GitHub for new issue creation or comment activity (created, edited, or deleted)
2. Trigger the workflow to process the event and format the information
3. Send the details as a notification to the designated Slack channel

## Cloud Usage

1. Initialize your connections (GitHub, Slack)
2. Set the `SLACK_CHANNEL_NAME_OR_ID` project variable to the Slack channel where you want to receive updates

## Trigger Workflow

Once deployed, the workflow is triggered by the creation of a new GitHub issue or any comment activity on an issue, including creation, editing, or deletion.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
