---
title: AI-driven Slack bot for assistance requests
description: Automatically route help requests to the right expert based on topic analysis and expertise matching
integrations: ["slack", "sheets", "googlegemini"]
categories: ["AI", "Productivity"]
---

# AI Driven Slack Support

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=slack_support)

This project automates help request management by assigning experts based on AI-inferred topics and predefined expertise. It tracks requests, allows experts to claim and resolve them, and sends reminders if unclaimed.

For example, given this expertise table:

```
   | A       | B         | C
---+---------+-----------+--------------
 1 | Itay    | U12345678 | cats,dogs
 2 | Haim    | U87654321 | russian
```

This would happen:

![demo](/slack_support/demo.png)

## How It Works

1. Receive a help request from a user
2. Identify the request topic using Gemini AI
3. Assign the request to the appropriate expert based on the expertise table
4. Confirm the expert’s acceptance of the request
5. Track the request until the expert resolves it
6. Remind the expert if the request remains unresolved within a set time

## Cloud Usage

1. Initialize your connections (Google Sheets, Google Gemini, Slack)
2. Set the `DIRECTORY_GOOGLE_SHEET_ID` project variable, in the "VARIABLES" tab, to point to your Google Sheet
3. (Optional) Set the `HELP_REQUEST_TIMEOUT_MINUTES` project variable, in the "VARIABLES" tab, to set the timeout for unclaimed requests
4. Deploy project

## Trigger Workflow

The workflow is triggered when the bot is mentioned in a message within a channel where it is a member. For example:

```
@autokitteh help me with my cat
```

When a topic matches an expert's expertise, the bot notifies them. The expert can use:

- `!take` to claim the request
- `!resolve` to mark it complete

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
