---
title: Monitor PR until completion in Slack
description: Create a Slack channel for each PR, update team leads until completion
integrations: ["slack", "github", "sheets"]
categories: ["DevOps"]
---

# GitHub Pull Request to Slack Workflow

This project automates the process of listening for GitHub pull request events and posting updates to a Slack channel. The workflow tracks the state of the pull request and meows at random people from a Google Sheet in the Slack channel.

## How It Works

1.	Receive GitHub pull request events (opened or reopened)
2.	Post updates to Slack with an initial message and dynamic updates as the pull request’s status changes
3.	Page team members by selecting a random person from a Google Sheet every 15 seconds and notifying them in Slack
4.	Conclude workflow when the pull request is closed or merged

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Set the `CHANNEL_ID`, `ORG_DOMAIN`, and `SHEET_ID` project variables in the "VARIABLES" tab

> [!IMPORTANT]
> Must be a Slack channel ID, not a Slack channel name.

3. Deploy the project

## Trigger Workflow

Once deployed, the workflow is triggered by a GitHub pull request event and continues to run, updating Slack until the pull request is closed or merged.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
