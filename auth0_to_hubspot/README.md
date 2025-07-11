---
title: Copy Auth0 Users to HubSpot
description: Periodically add new Auth0 users to HubSpot as contacts
integrations: ["auth0", "hubspot"]
categories: ["CRM"]
tags:
  [
    "data_pipeline",
    "data_processing",
    "error_handling",
    "notifications",
    "scheduled_tasks",
  ]
---

# Auth0 to HubSpot

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=auth0_to_hubspot)

This project adds new Auth0 users to HubSpot as contacts, on a recurring basis.

## How It Works

1. Fetch new Auth0 users from the last `HOURS` hours
2. Create HubSpot contacts for each user

## Deployment & Configuration

### Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. (Optional) Configure the `HOURS` variable to set the time range for new users to fetch.

> [!NOTE]
> To sync the schedule with the lookup time, update the schedule in the "TRIGGERS" tab. The default "Cron expression" is `@every 24h`.

3. Deploy the project

## Trigger Workflow

The workflow is triggered automatically every `HOURS` hours.

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI. Make sure to set the `check_for_new_users` function as the entrypoint.

> [!IMPORTANT]
> Ensure all connections (Auth0 and HubSpot) are properly initialized before the workflow starts running.

## Self-Hosted Deployment

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Auth0](https://docs.autokitteh.com/integrations/auth0)
  - [HubSpot](https://docs.autokitteh.com/integrations/hubspot)

#### Installation Steps

1. Clone the repository:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/auth0_to_hubspot
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
   [exec] create_connection "auth0_to_hubspot/auth0_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   [exec] create_connection "auth0_to_hubspot/hubspot_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   In this example, `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init auth0_connection <connection ID>
   ak connection init hubspot_connection <connection ID>
   ```

> [!TIP]
> You can also initialize your connections through the UI.
