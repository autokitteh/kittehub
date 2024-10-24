# Email Categorization and Notification Workflow

This project automates the process of categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## Benefits

- **Ease of Use:** Demonstrates how easy it is to connect multiple integrations into a cohesive workflow.
- **Low Complexity:** The workflow is implemented with a minimal amount of code.
- **Free and Open Source:** Available for use or modification to fit specific use cases. 

## How It Works

- **Detect New Email**: The program monitors the Gmail inbox for new emails using the Gmail API.
- **Categorize Email**: ChatGPT analyzes the email content and categorizes it into predefined categories.
- **Send Slack Notification**: The program sends the categorized email content to the corresponding Slack channel using the Slack API.
- **Label Email**: Adds a label to the processed email in Gmail for tracking.

For more details, refer to [this blog post](https://autokitteh.com/technical-blog/from-inbox-to-slack-automating-email-categorization-and-notifications-with-ai/).


### Configure integrations

- [Gmail](https://docs.autokitteh.com/integrations/google/config)
- [Slack](https://docs.autokitteh.com/integrations/slack/config)

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/categorize_emails/autokitteh.yaml
   ```

3. Look for the following lines in the output of the `ak deploy` command, and
   copy the URL paths for later:

   ```
   [!!!!] trigger "..." created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run these
> commands instead, and use the webhook slugs from their outputs:
>
> ```shell
> ak trigger get receive_http_get --project categorize_emails -J
> ```

## Usage Instructions

Run the following command, replacing {your-webhook-slug} with the webhook slug from the previous step:

```shell
curl -v "http://localhost:9980/webhooks/{your-webhook-slug}"
```

Now send yourself a new email and watch the workflow do its job!

## Known Limitations

- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases.
