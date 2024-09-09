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

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure integrations

- [Gmail](https://docs.autokitteh.com/integrations/google/config)
- [Slack](https://docs.autokitteh.com/integrations/slack/config)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/categorize_notify
```
Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `categorize_notify` directory:

   ```shell
   cd categorize_notify
   ```

2. Apply manifest and deploy project by running the following command:

   ```shell
   ak deploy --manifest autokitteh-python.yaml --file program.py
    ```
    The output of this command will be important for initializing connections in the following step if you're using the CLI.

    For example, for each configured connection, you will see a line that looks similar to the one below:

    ```shell
    [exec] create_connection "categorize_notify/my_chatgpt": con_01j36p9gj6e2nt87p9vap6rbmz created
    ```

    `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initiliaze Connections

> [!NOTE] 
> `my_http` does not need to initialized

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init my_chatgpt <connection ID>
ak connection init my_gmail <connection ID>
ak connection init my_slack <connection ID>
```

### Trigger the Workflow

Run this command:

```shell
curl -v "http://localhost:9980/http/categorize_notify/"
```

Now send yourself a new email and watch the workflow do its job!

## Known Limitations

- **ChatGPT**: the prompt for this workflow works for simple cases. It may have mixed results for emails that lack detail or have nothing to do with the channels provided.
- **Gmail mailbox polling**: the polling mechanism is basic and does not cover edge cases.
