# Jira-Slack Issue Workflow Automation

This project automates the process of creating Slack channels for new Jira issues and streamlines issue management. It listens for new Jira issues, creates a dedicated Slack channel for each issue, invites the issue creator to the channel, and waits for the user to confirm completion by mentioning the Slack app with `@ak done`. Once confirmed, it archives the channel, notifies the channel members, and updates the Jira issue status to `DONE`.

> [!IMPORTANT]  
> The mention `@autokitteh done` assumes that you have named your custom Slack app "autokitteh." If you used a different name, be sure to substitute "autokitteh" with the appropriate name of your Slack app when mentioning it in a Slack channel.

## How It Works

- **Detect New Jira Issues:** The program listens for new issues created in Jira.
- **Create Slack Channel:** When a new issue is detected, it creates a Slack channel named after the issue key and summary.
- **Invite Issue Creator:** Invites the issue creator to the Slack channel.
- **Await User Confirmation:** Waits for the user to confirm completion by typing `@autokitteh done` in the Slack channel.
- **Archive Channel and Update Jira:** Notifies channel members, archives the Slack channel, and updates the Jira issue status to `DONE`.

## Installation and Usage

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

- [Jira Integration](https://docs.autokitteh.com/integrations/atlassian/config)
- [Slack Integration](https://docs.autokitteh.com/integrations/slack/config)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/jira_ticket_handling
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `jira_slack_issue_workflow` directory:

   ```shell
   cd jira_slack_issue_workflow
   ```

2. Apply the manifest and deploy the project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "jira_slack_issue_workflow/slack_conn": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

> [!IMPORTANT]
> `slack_conn` and `jira_conn_api_key` need to be initialized using the IDs from the previous step.

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init jira_conn_api_key <connection ID>
ak connection init jira_events_oauth <connection ID>
ak connection init slack_conn <connection ID>
```
> [!WARNING]
> The `jira_conn_api_key` connection is used to send requests to the Jira API and needs to be initialized with an API key.
> The `jira_events_oauth` connection is used to listen for events from Jira. It must be initialized with the OAuth connection ID.

### Trigger the Workflow

The workflow is triggered when a new issue is created in Jira.

## Customization

Feel free to customize the workflow to suit your needs. For example, you can:

- Change the trigger event or conditions.
- Modify the message content or notification methods.
- Integrate additional services or automate more steps.
