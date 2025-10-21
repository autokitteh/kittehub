---
title: Sync Webhook sample
description: Sample demonstrating synchronous webhook handling with multiple triggers
integrations: []
categories: ["Samples"]
tags: ["webhook", "sync", "subscribe", "next_event", "http_outcome", "outcome", "essential"]
---

# Sync Webhook Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/sync_webhook)

This AutoKitteh project demonstrates how to handle synchronous webhooks with multiple triggers, showing how to wait for a second webhook before responding to the first one.

## How It Works

1. **First Webhook** - Receives a webhook trigger that starts the workflow
2. **Wait for Second** - Uses `subscribe` and `next_event` to wait for the second webhook to be triggered
3. **Synchronous Response** - Returns an HTTP response with the body from the second webhook

The workflow demonstrates:

- Synchronous webhook handling (`is_sync: true`)
- Cross-trigger communication using `subscribe` and `next_event`
- Custom HTTP responses using `http_outcome`

## Cloud Usage

1. Copy the webhook URLs from the "Triggers" tab for both `first` and `second` triggers (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
2. Deploy the project

## Trigger Workflow

1. Send a request to the `first` webhook URL - this will start the workflow but won't respond immediately:

```shell
curl -i "${FIRST_WEBHOOK_URL}"
```

2. While the first request is waiting, send a request to the `second` webhook URL:

```shell
curl -i -d "Hello from second webhook" "${SECOND_WEBHOOK_URL}"
```

3. The first webhook request will now complete and return a 200 response with the body from the second webhook.
