---
title: OpenAI ChatGPT sample
description: Samples using chatGPT APIs
integrations: ["chatgpt"]
categories: ["AI", "Samples"]
---

# OpenAI ChatGPT Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/openai_chatgpt)

This project demonstrates integration with ChatGPT for text generation and response analysis. It showcases how to make API calls to ChatGPT and track token usage statistics.

API documentation:

- [OpenAI developer platform](https://platform.openai.com/)
- [Python client API](https://github.com/openai/openai-python)

## Cloud Usage

1. Initialize your OpenAI ChatGPT connection
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the OpenAI ChatGPT integration is initialized with a valid API key; otherwise, workflows will raise `ConnectionInitError`.

Send an HTTP POST request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i -X POST "${WEBHOOK_URL}" -H "Content-Type: text/plain" -d "prompt"
```

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI.
>
> You can modify the request body to send custom text and observe ChatGPT's dynamic responses.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

> [!NOTE]
> The [`autokitteh.yaml`](autokitteh.yaml) manifest file includes HTTP request filtering. You can modify or remove this filter as needed.
