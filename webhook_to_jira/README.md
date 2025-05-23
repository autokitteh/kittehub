---
title: Create Jira ticket from webhook data
description: Create Jira issues automatically from HTTP webhooks
integrations: ["jira", "http"]
categories: ["DevOps"]
---

# Create Jira Ticket From Webhook Data

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=webhook_to_jira)

This project automates Jira issue creation through HTTP requests. It supports multiple formats, including GET parameters, POST form data, and JSON payloads, making it adaptable to various external systems.

API documentation:

- Atlassian Jira: https://docs.autokitteh.com/integrations/atlassian/jira/python
- HTTP: https://docs.autokitteh.com/integrations/http/events

## How It Works

1. Receive HTTP requests via webhook (GET or POST)
2. Parse request data based on content type
3. Create corresponding Jira issue using the parsed data
4. Return the created issue details in the response

## Cloud Usage

1. Initialize your Jira connection
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Jira connection is initialized; otherwise, the workflow will raise a `ConnectionInitError`.

Send HTTP requests to your webhook URL using any of these methods:

1. GET request with query parameters:

   ```shell
   curl -i "${WEBHOOK_URL}" \
        --url-query project=TEST --url-query issuetype=Task \
        --url-query "summary=Test issue" \
        --url-query "description=Created with HTTP GET"
   ```

2. POST request with form data:

   ```shell
   curl -i -X POST "${WEBHOOK_URL}" \
        --data project=TEST --data issuetype=Task \
        --data "summary=Test issue" \
        --data "description=Created with form data"
   ```

3. POST request with JSON (supports [all Jira issue fields](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-post-request-body)):
   ```shell
   curl -i -X POST "${WEBHOOK_URL}" \
      -H "Content-Type: application/json" \
      -d @path/to/your/file.json
   ```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
