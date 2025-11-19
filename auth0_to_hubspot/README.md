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

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=auth0_to_hubspot)

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

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
