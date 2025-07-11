---
title: AutoKitteh session errors monitor
description: Send Slack alerts when AutoKitteh sessions end due to errors
integrations: ["autokitteh", "slack"]
categories: ["Reliability"]
tags: ["monitoring", "notifications", "scheduled_tasks", "error_handling"]
---

# AutoKitteh Session Errors Monitor

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=reliability/session_errors_monitor)

Send Slack alerts when AutoKitteh sessions end due to errors.

This is a detection tool for incidents due to unexpected exceptions in workflows that are usually stable and dependable. It can also be used as a development and debugging tool.

It gets triggered by the AutoKitteh scheduler every minute, on the minute, to look for sessions that ended with an error status in the previous minute.

## Cloud Usage

1. Generate a personal API auth token in the web UI:

   - Click your user icon in the bottom-left corner of the page
   - Click the "Client Setup" menu option to go to that page
   - Click the "Generate Token" button, and copy the generated [JWT](https://jwt.io/)

2. Navigate to this project in the web UI
3. Initialize your Slack connection
4. Set/modify these project variables:

   - `AUTOKITTEH_API_BASE_URL` (default = `https://api.autokitteh.cloud`, use `http://localhost:9980` for self-hosted servers)
   - `AUTOKITTEH_UI_BASE_URL` (default = `https://app.autokitteh.cloud`, use `http://localhost:9982` for self-hosted servers)
   - `AUTOKITTEH_AUTH_TOKEN`: the API auth token generated in step 1 above
   - `SLACK_CHANNEL_NAME_OR_ID`: send alert messages to this Slack channel (default = `autokitteh-alerts`)

5. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Slack connection is properly initialized; otherwise the workflow will raise a `ConnectionInitError`.
>
> Also ensure the project variables are configured correctly; otherwise the workflow may not work as expected.

After the project is deployed, the workflow runs automatically at the beginning of every minute.

You may modify this by modifying the `TRIGGER_INTERVAL` project variable and the `schedule` field in the trigger.

Test the trigger by running any other AutoKitteh workflow that ends with an error.

## Self-Hosted Deployment

1. Generate a personal API auth token, by running this CLI command:

   ```shell
   ak auth create-token
   ```

2. Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server

3. Follow steps 3-4 in the [Cloud Usage](#cloud-usage) section above
