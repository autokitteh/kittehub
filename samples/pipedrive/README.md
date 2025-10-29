---
title: Pipedrive sample
description: Simple usage of the Pipedrive API
integrations: ["pipedrive"]
categories: ["Samples"]
---

# Pipedrive Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/pipedrive)

The Pipedrive sample demonstrates how to manage deals using AutoKitteh's Pipedrive integration.

The sample includes two separate workflows:

1. **Create Deal** - Create a Pipedrive deal
2. **Fetch all deals** - Get all the deals

API details:

- [Pipedrive API](https://developers.pipedrive.com/)
- [Python client library](https://github.com/pipedrive/client-python)

## How It Works

1. Create a new deal in Pipedrive with a custom title and value
2. Fetch all deals from your Pipedrive account and display their details

## Cloud Usage

1. Initialize your Pipedrive connection through the UI
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):
   - Hover over the trigger's (i) icon for the webhook you want to use
   - Click the copy icon next to the webhook URL for your selected trigger
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

## Trigger Workflows

> [!IMPORTANT]
> Ensure your Pipedrive connection is initialized with valid credentials.

### Create a Deal

```shell
curl -X POST "${WEBHOOK_URL}" -d "title=New Deal&value=5000"
```

- Replace `WEBHOOK_URL` with the URL of `create_deal_webhook` webhook in the triggers section.
- Provide a title and a value.

> [!NOTE]
> Both `title` and `value` parameters are optional. Defaults are `'AutoKitteh Deal'` and `1000` respectively.

### Fetch All Deals

```shell
curl "${WEBHOOK_URL}"
```

Replace `WEBHOOK_URL` with the URL of `fetch_all_deals_webhook` webhook in the triggers section.

> [!TIP]
> Function `fetch_all_deals` can also be triggered manually by clicking the "Run" button in the UI.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
