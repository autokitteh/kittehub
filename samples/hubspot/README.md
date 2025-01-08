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

1. Create a new contact in HubSpot with predefined details.
2. Retrieve and list all deals from HubSpot, displaying their IDs and names.

## Deployment & Configuration

### Cloud Usage

- Initialize your connection with HubSpot through the UI

### Self-Hosted Server

#### Prerequisites

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

#### Installation Steps

1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/samples/hubspot
   ```

2. Start the AutoKitteh server:
   ```shell
   ak up --mode dev
   ```

3. Deploy the project:
   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output will show your connection IDs, which you'll need for the next step. Look for lines like:
   ```shell
   [exec] create_connection "hubspot/hubspot_conn": con_01jh2gx9jce6jr436fsz43g5zf created
   ```
   
   In this example, `con_01jh2gx9jce6jr436fsz43g5zf` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init <connection ID>
   ```

## Trigger Workflow

The workflow is triggered by sending an HTTP GET request.

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI. Ensure the function you want to run is set as the entrypoint.

> [!IMPORTANT]
> Ensure that the connection with HubSpot is properly initialized before the workflow starts running.

