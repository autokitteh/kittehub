---
title: Gmail sample
description: Samples using Gmail APIs
integrations: ["gmail"]
categories: ["Samples"]
---

# Gmail Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/google/gmail)

This AutoKitteh project demonstrates 2-way integration with
[Gmail](https://www.google.com/gmail/about/).

API Documentation

- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events

## How It Works

1. Handles HTTP GET requests to interact with Gmail
2. Retrieves profile details, drafts, and messages, and sends emails to the authenticated user

## Cloud Usage

1. Initialize your connection with Gmail
2. Deploy project

## Trigger Workflow

Run these commands to interact with Gmail via HTTP trigger using query parameters:

```shell
curl -i "${WEBHOOK_URL}" --url-query cmd=get_profile
curl -i "${WEBHOOK_URL}" --url-query cmd=list_drafts [--url-query query=optional_query]
curl -i "${WEBHOOK_URL}" --url-query cmd=get_draft&draft_id=<draft_ID>
curl -i "${WEBHOOK_URL}" --url-query cmd=list_messages&query=optional_query
curl -i "${WEBHOOK_URL}" --url-query cmd=get_message&message_id=<message_ID>
curl -i "${WEBHOOK_URL}" --url-query cmd=send_message&text=<message_text>
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
