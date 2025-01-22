---
title: Slack sample
description: Samples using Slack APIs
integrations: ["slack"]
categories: ["Samples"]
---

# Slack Sample

This sample project demonstrates AutoKitteh's 2-way integration with
[Slack](https://slack.com).

The code file [`program.py`](./program.py) implements multiple entry-point
functions that are triggered by incoming Slack events, as defined in the
[`autokitteh.yaml`](./autokitteh.yaml) manifest file. These functions also
execute various Slack API calls.

Slack API documentation:

- [Web API reference](https://api.slack.com/methods)
- [Events API reference](https://api.slack.com/events?filter=Events)
- [Python client API](https://slack.dev/python-slack-sdk/api-docs/slack_sdk/)

This project isn't meant to cover all available functions and events. It
merely showcases a few illustrative, annotated, reusable examples.

## How It Works

1. Listens for Slack events such as mentions, slash commands, new messages, edited messages, and emoji reactions.
2. Processes the event data to extract relevant information (e.g., user, message, or action details).
3. Sends responses or updates messages in Slack channels or threads based on the event type.
4. The `on_slack_reaction_added` function prints event details when a reaction is added.

## Cloud Usage

1. Initialize your connection with Slack

## Trigger Workflow

1. Mention the Slack app in a message (e.g., "Hi @autokitteh") to trigger a response
2. Interact with a Slack block element (e.g., click a button or select from a dropdown)
3. Send a message or reply in a Slack channel
4. Add a reaction (emoji) to a message in Slack
5. Use a registered slash command (e.g., `/autokitteh <channel name or ID>`)
> [!IMPORTANT]  
> Self-hosted users who set up their Slack App using https://docs.autokitteh.com/integrations/slack/connection will have their commands registered as expected. If you set up your app differently, your registered commands may vary.
> [!NOTE]
> Ensure the Slack app is added to the relevant channel for these events to trigger the workflow.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
