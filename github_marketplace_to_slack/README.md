# Webhook to Jira

This project receives
[webhook notifications from the GitHub Marketplace](https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes),
when changes to customer account plans occur, and posts them to a Slack
channel.

This allows you to handle
[marketplace_purchase](https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/webhook-events-for-the-github-marketplace-api)
events in your GitHub app.

## API Documentation

GitHub:

- [Configuring a webhook to notify you of plan changes](https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes)

HTTP:

- https://docs.autokitteh.com/integrations/http/events

Slack:

- https://docs.autokitteh.com/integrations/slack/python

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud): \

   - [enable Slack connections to use an OAuth v2 app](https://docs.autokitteh.com/integrations/slack/config)

3. Run this command to clone the Kittehub repository, which contains this
   project:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ```

4. Set these variables in this project's [autokitteh.yaml](./autokitteh.yaml)
   manifest file:

   - `GITHUB_WEBHOOK_SECRET`
   - `SLACK_CHANNEL_NAME_OR_ID`

5. Run this command to deploy this project's manifest file:

   ```shell
   ak deploy --manifest kittehub/github_marketplace_to_slack/autokitteh.yaml
   ```

6. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "webhook_notification" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get webhook_notification --project github_marketplace_to_slack -J
> ```

7. Initialize this project's Slack connection with an OAuth v2 app (based on
   step 2), or a Socket Mode app

> [!TIP]
> The exact CLI command to do so (`ak connection init ...`) will appear in the
> output of the `ak deploy` command from step 5 when you create the project on
> the server, i.e. when you run that command for the first time.

## Usage Instructions

1. Configure the GitHub app's webhook in the GitHub Marketplace:
   https://github.com/marketplace/YOUR-APP-NAME/hook

   - Payload URL: https://PUBLIC-AK-ADDRESS/webhooks/SLUG
     - `PUBLIC-AK-ADDRESS` is the AutoKitteh server's
       [public address](https://docs.autokitteh.com/config/http_tunneling)
     - `SLUG` is the last element in the webhook trigger's URL path (from step 6 above)
   - Content type: `application/json`
   - Secret: (same as in step 4 above)

2. https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/testing-your-app
