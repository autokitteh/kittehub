---
title: Anthropic Slack Thread TLDR
description: Summarizes a Slack thread using Claude
integrations: ["slack"]
categories: ["AI"]
---

# Anthropic Slack Thread TLDR

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=anthropic_slack_thread_tldr)

Allows Slack users to summarize a Slack thread by posting `!tldr` in a thread.

API documentation:

- Anthropic Python SDK: https://github.com/anthropics/anthropic-sdk-python

## How It Works

1. In any Slack thread in a channel where the bot is present, use the command:

   ```
   !tldr
   ```

2. The bot will reply with a concise thread summary.

## Cloud Usage

1. Initialize Slack connection
2. Configure the `ANTHROPIC_API_KEY` project variable with your API key
3. Configure the `INVOCATION_CMD` variable to set the command prefix (default: "tldr")
4. Configure the `MAX_TOKENS` variable to limit maximum tokens per interaction (default: 1000)
5. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Slack connection is initialized; otherwise, the workflow will raise a `ConnectionInitError`.

In any Slack thread in a channel where the bot is present, use the command:

```
!tldr
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
