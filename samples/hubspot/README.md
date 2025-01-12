---
title: HubSpot
description: Simple usage of the HubSpot API
integrations: ["hubspot"]
categories: ["Samples"]
---

# HubSpot Sample

This [AutoKitteh](https://github.com/autokitteh/autokitteh) project
demonstrates integration with [HubSpot](https://www.hubspot.com).

It sends a couple of requests to the HubSpot API, adds a contact, retrieves deals, and prints the responses back to the user.

API details:

- [HubSpot API](https://pypi.org/project/hubspot-api-client/)
- [Python client library](https://github.com/HubSpot/hubspot-api-python)

## How It Works

1. Create a new contact in HubSpot with predefined details
2. Retrieve and list all deals from HubSpot, displaying their IDs and names

## Cloud Usage (Recommended)

1. Initialize your connection through the UI
2. Edit the trigger of the workflow you want to trigger, in the "TRIGGERS" tab, under the "Actions" column.
3. Copy the provided webhook URL.
4. Send GET or POST requests to the webhook of your choice:

   - For create_contact_webhook:
      ```shell
      curl "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}" \
           -d email=meow@autokitteh.com \
           -d firstname=Kitty \
           -d lastname=Meowington
      ```
   - For list_deals_webhook:
      ```shell
         curl -X GET "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}"
      ```

## Trigger Workflow

Trigger the workflow using the webhook URL. Refer to the [Cloud Usage](#cloud-usage-recommended) section for detailed steps.

### Steps to Retrieve the Webhook URL

- The webhook URL is provided in the output of the `ak deploy` command.
- Run the following command to retrieve the URL:
  ```shell
  ak trigger get <trigger name or ID>
  ```

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI. Ensure the function you want to run is set as the entrypoint.

> [!IMPORTANT]
> Ensure that the connection with HubSpot is properly initialized before the workflow starts running.

### Self-Hosted Server

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

