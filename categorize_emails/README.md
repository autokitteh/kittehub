---
title: Email categorization and notification
description: Categorize incoming emails and notify relevant Slack channels
integrations: ["gmail", "chatgpt", "slack"]
categories: ["AI", "Productivity"]
---

# Email Categorization and Notification

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=categorize_emails)

Categorize incoming emails and notify relevant Slack channels by integrating Gmail, ChatGPT, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## How It Works

1. Fetch new emails from Gmail API
2. Use ChatGPT to analyze and categorize email content
3. Post categorized emails to relevant Slack channels
4. Label processed emails in Gmail

For more details, refer to [this blog post](https://autokitteh.com/technical-blog/from-inbox-to-slack-automating-email-categorization-and-notifications-with-ai/).

## Cloud Usage

1. Initialize your connections (ChatGPT, Gmail, Slack)
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy the project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all the connections (ChatGPT, Gmail, Slack) are properly initialized; otherwise the workflow will raise a `ConnectionInitError`.

1. Start a long-running AutoKitteh session by sending an HTTP GET request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

   ```shell
   curl -i "${WEBHOOK_URL}"
   ```

2. Send yourself a new email
3. Wait up to 10 seconds for the workflow's polling loop to detect it

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases.
