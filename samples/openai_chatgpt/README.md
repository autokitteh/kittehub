---
title: OpenAI ChatGPT sample
description: Samples using chatGPT APIs
integrations: ["chatgpt"]
categories: ["AI", "Samples"]
---

# OpenAI ChatGPT Sample

This project demonstrates integration with ChatGPT for text generation and response analysis. It showcases how to make API calls to ChatGPT and track token usage statistics.

API documentation:

- [OpenAI developer platform](https://platform.openai.com/)
- [Python client API](https://github.com/openai/openai-python)

## How It Works

1. Receive text input via HTTP POST requests
2. Send the input to ChatGPT's API for processing
3. Print the AI-generated response and token usage statistics

## Cloud Usage

1. Initialize your OpenAI ChatGPT connection
2. Copy the webhook trigger's URL:
   - Hover over the trigger's (i) icon
   - Click the copy icon next to the webhook URL
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the OpenAI ChatGPT integration is initialized with a valid API key; otherwise, workflows will raise `ConnectionInitError`.

Send an HTTP POST request to trigger the workflow:

```shell
curl -i -X POST "${WEBHOOK_URL}" -H "Content-Type: text/plain" -d "Meow"
```

> [!TIP]
> You can modify the request body to send custom text and observe ChatGPT's dynamic responses.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

> [!NOTE]
> The [`autokitteh.yaml`](autokitteh.yaml) manifest file includes HTTP request filtering. You can modify or remove this filter as needed.
