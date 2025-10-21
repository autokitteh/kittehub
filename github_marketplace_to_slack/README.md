---
title: GitHub Marketplace to Slack
description: Forward GitHub Marketplace notifications to Slack
integrations: ["github", "slack"]
categories: ["CRM"]
tags: ["webhook_handling", "notifications", "data_processing"]
---

# GitHub Marketplace to Slack

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=github_marketplace_to_slack)

Forward [GitHub Marketplace notifications](https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes) to Slack.

This allows you to handle [`marketplace_purchase`](https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/webhook-events-for-the-github-marketplace-api) notifications for your GitHub app.

## How It Works

1. Receive notifications from GitHub Marketplace:

   - [`marketplace_purchase`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#marketplace_purchase)
   - [`ping`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#ping)

2. Verify their authenticity (based on [this](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries))
3. Format the JSON content of the notifications, and post them as messages in a preconfigured Slack channel

## GitHub Webhook Configuration

Configure the GitHub app's webhook in the GitHub Marketplace:
`https://github.com/marketplace/YOUR-APP-NAME/hook`

- **Payload URL:** _(you will set this later, based on step 2 in the [Cloud Usage](#cloud-usage) section below)_
- **Content type:** `application/json`
- **Secret:** a random string of text with high entropy _(save it for later, in step 3 in the [Cloud Usage](#cloud-usage) section below)_

> [!IMPORTANT]
> Do not click the "Create/Update webhook" button and keep this browser tab open. You will need to return here later, in step 5 of the [Cloud Usage](#cloud-usage) section below.

## Cloud Usage

1. Initialize your Slack connection
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Set/modify these project variables:

   - `GITHUB_WEBHOOK_SECRET`: the secret value from the [GitHub Webhook Configuration](#github-webhook-configuration) section above
   - `SLACK_CHANNEL_NAME_OR_ID`: send notifications to this Slack channel name/ID (default = `github-marketplace`)

4. Deploy the project
5. Finish the GitHub webhook configuration from the [GitHub Webhook Configuration](#github-webhook-configuration) section above:

   - Set the **Payload URL** to the one you copied from the trigger in step 2 above
   - Click the "Create/Update webhook" button

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Slack connection is properly initialized; otherwise the workflow will raise a `ConnectionInitError`.
>
> Also ensure the project variables are configured correctly; otherwise the workflow may not work as expected.

How to test the project's webhook trigger:

https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/testing-your-app

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

Also follow the relevant instructions in the Cloud Usage section above.
