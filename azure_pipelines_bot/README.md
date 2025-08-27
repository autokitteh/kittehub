---
title: Azure Pipelines Bot for Microsoft Teams
description: Monitor Azure DevOps build completions and enable interactive pipeline management through Microsoft Teams conversations
integrations: ["azurebot"]
categories: ["DevOps"]
tags:
  [
    "webhook",
    "interactive_workflows",
    "user_interactions",
    "subscribe",
    "next_event",
    "event_loops",
  ]
---

# Azure Pipelines Bot

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=azure_pipelines_bot)

This automation connects Azure DevOps pipelines to Microsoft Teams, enabling teams to monitor build completions and interact with pipelines directly from Teams conversations. When a build completes, the bot posts a notification to a Teams channel and allows users to retry failed builds through simple chat commands.

## How It Works

1. Receives webhook notifications when Azure DevOps builds complete
2. Posts build completion messages to a Microsoft Teams channel
3. Listens for user interactions in the Teams conversation
4. Allows users to retry builds by typing "retry" in response to build notifications
5. Queues new builds with the same parameters as the original failed build

## Cloud Usage

1. Initialize your Azure Bot connection
2. Set these required project variables:
   - `CHANNEL_CONVO_ID` - Microsoft Teams channel conversation ID
   - `AZURE_DEVOPS_PAT` - Azure DevOps Personal Access Token (marked as secret)
   - `AZURE_DEVOPS_ORG` - Azure DevOps organization name
3. Deploy project
4. Configure Azure DevOps webhook to point to the generated webhook URL

## Trigger Workflow

The workflow is triggered by Azure DevOps webhooks when builds complete with `eventType='build.complete'`. Users can then interact with the bot by:

- Typing `@<Bot Name> retry` in response to build completion messages to queue a new build
