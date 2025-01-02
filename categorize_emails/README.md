---
title: Slack notify on categorized email
description: Categorizes incoming emails and notifies relevant Slack channels by integrating Gmail, ChatGPT, and Slack
integrations: ["gmail", "slack", "chatgpt"]
categories: ["Office Automation"]
---

# Email Categorization and Notification Workflow

This project automates the process of categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## How It Works

1. Fetch new emails from Gmail API
2. Use ChatGPT to analyze and categorize email content
3. Post categorized emails to relevant Slack channels
4. Label processed emails in Gmail

For more details, refer to [this blog post](https://autokitteh.com/technical-blog/from-inbox-to-slack-automating-email-categorization-and-notifications-with-ai/).

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Edit the "receive_http_get" trigger, in the "TRIGGERS" tab, under the "Actions" column
3. Copy the provided webhook URL
4. Test the webhook by sending a curl request with the webhook URL
      ```shell
      curl -i "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}"
      ```
5. Send yourself a new email to validate the connection


> [!IMPORTANT]
> Ensure all connections (Gmail, Slack, and ChatGPT) are properly initialized before the workflow starts running.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Trigger Workflow

Trigger the workflow using the webhook URL. Refer to the [Cloud Usage](#cloud-usage-recommended) section for detailed steps.

### Steps to Retrieve the Webhook URL

- The webhook URL is provided in the output of the `ak deploy` command.
- Run the following command to retrieve the URL:
  ```shell
  ak trigger get <trigger name or ID>
  ```

> [!TIP]
> The trigger name can be found in the `autokitteh.yaml` file.

## Known Limitations

- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases.
