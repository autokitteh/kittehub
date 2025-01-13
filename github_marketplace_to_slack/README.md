---
title: GitHub Marketplace to Slack
description: Forward GitHub Marketplace webhook notifications to Slack
integrations: ["GitHub", "HTTP", "Slack"]
categories: ["GitHub", "Sales"]
---

# GitHub Marketplace to Slack

Forward [GitHub Marketplace webhook notifications](https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes) to Slack.

This allows you to handle [marketplace_purchase](https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/webhook-events-for-the-github-marketplace-api) events in your GitHub app.

## Configuration and Deployment

### GitHub Webhook

Configure the GitHub app's webhook in the GitHub Marketplace:
`https://github.com/marketplace/YOUR-APP-NAME/hook`

- **Payload URL:** _(you will set this later, see steps 3 and 6 in the_
  _[Cloud Usage](#cloud-usage) section below)_
- **Content type:** `application/json`
- **Secret:** a random string of text with high entropy, save for later

> [!IMPORTANT]
> Don't click the "Create/Update webhook" button yet.

### Cloud Usage

1. Import/upload the project
2. Initialize your connections
3. Edit the trigger:

   - Copy the generated webhook URL for step 6 later
   - No need to actually change anything

4. Set/modify these project variables:

   - `GITHUB_WEBHOOK_SECRET`: the secret value from the
     [GitHub Webhook](#github-webhook) section above
   - `SLACK_CHANNEL_NAME_OR_ID`: send notifications to this Slack channel
     name/ID (default = `github-marketplace`)

5. Deploy the project
6. Finish the webhook configuration from the [GitHub Webhook](#github-webhook)
   section above:

   - Set the **payload URL** to the one you copied from the trigger in step 3
     above
   - Click the "Create/Update webhook" button

### Self-Hosted CLI Usage

1. Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment)
   to deploy the project on a self-hosted server

2. Follow step 2 in the [Cloud Usage](#cloud-usage) section above

3. _CLI alternative for step 3 in the [Cloud Usage](#cloud-usage) section above:_
   look for the following line in the output of the `ak deploy` command, and
   copy the URL path for the last step:

```
[!!!!] trigger "webhook_notification" created, webhook path is "/webhooks/SLUG"
```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the `webhook_slug` from the output:
>
> ```shell
> ak trigger get webhook_notification --project github_marketplace_to_slack -J
> ```

4. Follow steps 4-6 in the [Cloud Usage](#cloud-usage) section above

> [!IMPORTANT]
> The host address in the payload URL in step 6 must be public, not
> `http://localhost:9980`, see https://docs.autokitteh.com/config/http_tunneling

## Testing

https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/testing-your-app
