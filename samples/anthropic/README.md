---
title: Anthropic Claude sample
description: Sample using Anthropic Claude API
integrations: ["anthropic"]
categories: ["AI", "Samples"]
---

# Anthropic Claude Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/anthropic)

This project demonstrates integration with Anthropic's Claude for text generation and conversational AI. It showcases how to make API calls to Claude and track token usage statistics.

The sample includes two separate workflows:

- **With custom prompt**: Accepts user input via HTTP POST and processes it with Claude
- **Demo mode**: Uses a preset prompt via HTTP GET for quick testing

API documentation:

- [Anthropic documentation](https://docs.anthropic.com/)
- [Python client API](https://github.com/anthropics/anthropic-sdk-python)

## How It Works

### Workflow 1: Custom Prompt (POST)

1. Triggered by an HTTP POST request with a text prompt in the body
2. Claude processes the prompt with system instructions (as a coding assistant)
3. Response and usage statistics are logged in the AutoKitteh session

### Workflow 2: Demo Mode (GET)

1. Triggered by an HTTP GET request with no body required
2. Claude processes a default prompt (cat facts)
3. Response and usage statistics are logged in the AutoKitteh session

## Cloud Usage

1. Initialize your Anthropic connection
2. Copy the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Anthropic integration is initialized with a valid API key; otherwise, the Anthropic connection won't be saved.

### Option 1: Custom Prompt (POST)

Send an HTTP POST request with your custom prompt:

```shell
curl -i -X POST "${WEBHOOK_URL_POST}" -H "Content-Type: text/plain" -d "Why do cats purr?"
```

### Option 2: Demo Mode (GET)

Send an HTTP GET request with no body:

```shell
curl -i -X GET "${WEBHOOK_URL_GET}"
```

> [!TIP]
> Function `on_http_get_demo` can also be triggered manually by clicking the "Run" button in the UI.
> You can modify the POST request body to send custom text and observe Claude's dynamic responses.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

> [!NOTE]
> The [`autokitteh.yaml`](autokitteh.yaml) manifest file includes HTTP request filtering. You can modify or remove this filter as needed.
