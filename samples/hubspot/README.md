---
title: HubSpot sample
description: Simple usage of the HubSpot API
integrations: ["hubspot"]
categories: ["CRM", "Samples"]
---

# HubSpot Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/hubspot)

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates integration with [HubSpot](https://www.hubspot.com).

It sends a couple of requests to the HubSpot API, adds a contact, retrieves deals, and prints the responses back to the user.

API details:

- [HubSpot API](https://pypi.org/project/hubspot-api-client/)
- [Python client library](https://github.com/HubSpot/hubspot-api-python)

## How It Works

1. Create a new contact in HubSpot with predefined details
2. Retrieve and list all deals from HubSpot, displaying their IDs and names

## Cloud Usage

1. Initialize your HubSpot connection
2. Copy the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

## Trigger Workflow

> [!IMPORTANT]
> Ensure the HubSpot connection is properly initialized; otherwise the workflow will raise a `ConnectionInitError`.

Send HTTP GET and POST requests to the webhook URLs from step 2 in the [Cloud Usage](#cloud-usage) section above.

For `create_contact_webhook`:

```shell
curl -i -X POST "${WEBHOOK_URL}" -d email=meow@autokitteh.com \
     -d firstname=Kitty -d lastname=Meowington
```

For `list_deals_webhook`:

```shell
curl -i "${WEBHOOK_URL}"
```

> [!TIP]
> The `list_deals` workflow can also be triggered manually by clicking the "Run" button in the UI, and setting the `list_deals` function as the entry point.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
