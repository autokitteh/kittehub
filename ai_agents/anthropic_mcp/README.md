---
title: Anthropic MCP Sample
description: Simple usage of the Anthropic API via AutoKitteh
integrations: ["anthropic", "slack"]
categories: ["AI", "Productivity"]
---

# Anthropic MCP Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=ai_agents/anthropic_mcp)

This sample demonstrates how to interact with Anthropic's API using AutoKitteh, enabling you to leverage advanced language models for your automation workflows.

It includes functionality to send prompts to Anthropic's Claude models and process the responses.

API details:

- [Anthropic API documentation](https://docs.anthropic.com/claude/docs)
- [AutoKitteh Anthropic integration](https://docs.autokitteh.com/integrations/anthropic)

## How It Works

1. Sends a prompt to the Anthropic Claude API.
2. Receives and logs the model's response in the AutoKitteh session.

## Cloud Usage (Recommended)

1. Initialize your Anthropic connection through the AutoKitteh UI.
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):

   - Hover over the trigger's (i) icon for the webhook you want to use.
   - Click the copy icon next to the webhook URL for your selected trigger.
   - (Detailed instructions
     [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

3. Set any required environment variables or project variables (such as your Anthropic API key).

## Trigger Workflows

`send_prompt`:

```shell
curl -i "${WEBHOOK_URL}" --url-query prompt="Your question for Claude"
```
