---
title: Slack notify on important Email
description: Categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack
integrations: ["gmail", "slack", "chatgpt"]
categories: ["Office Automation"]
---

# Email Categorization and Notification Workflow

This project automates the process of categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## How It Works

1. Fetches new emails from Gmail API
2. Uses ChatGPT to analyze and categorize email content
3. Posts categorized emails to relevant Slack channels
4. Labels processed emails in Gmail

For more details, refer to [this blog post](https://autokitteh.com/technical-blog/from-inbox-to-slack-automating-email-categorization-and-notifications-with-ai/).

## Cloud Usage (Recommended)

1. Initialize your connections through the UI.
2. Navigate to the "TRIGGERS" tab in your project settings.
3. Find the "receive_http_get" trigger under the "Actions" column.
4. Click "Edit".
5. Copy the provided webhook URL.
6. Test the webhook by sending a curl request with the webhook URL.
      ```shell
      curl -i "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}"
      ```
7. Send yourself a new email to validate the connection.


> [!IMPORTANT]
> Ensure all connections (Gmail, Slack, and ChatGPT) are properly initialized before the workflow starts running.

## Self-Hosted Deployment

### Prerequisites

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Gmail](https://docs.autokitteh.com/integrations/google)
  - [Slack](https://docs.autokitteh.com/integrations/slack)
  - [ChatGPT](https://docs.autokitteh.com/integrations/chatgpt)

### Installation Steps

1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/categorize_emails
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
   [exec] create_connection "categorize_emails/gmail_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```
   
   In this example, `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init gmail_connection <connection ID>
   ak connection init slack_connection <connection ID>
   ak connection init chatgpt_connection <connection ID>
   ```

## Trigger Workflow

Trigger the workflow using the webhook URL. Refer to the [Cloud Usage](#cloud-usage-recommended) section for detailed steps.

### Steps to Retrieve the Webhook URL

- The webhook URL is provided in the output of the `ak deploy` command.
- Run the following command to retrieve the URL:
  ```bash
  ak trigger get <trigger name or ID>
  ```

> [!TIP]
> The trigger name can be found in the `autokitteh.yaml` file.

## Known Limitations

- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases.
