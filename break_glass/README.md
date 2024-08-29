
# Break-Glass Request Workflow

This project implements a break-glass request workflow that allows users to submit emergency access requests via Slack, which are then approved or denied based on a set of predefined conditions. The project integrates Slack and Jira with custom modals and messages.

## Benefits

- Provides a clear audit trail of emergency access requests.
- Simplifies the process of requesting and granting emergency access.

## How It Works

1. Users submit a break-glass request via a custom Slack modal.
2. The request is sent for approval to designated approvers.
3. Approvers can approve or deny the request via Slack.
4. The approval or denial is logged and the requester is notified.

## Installation and Usage 

[Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

> [!IMPORTANT]
> The `autokitteh.yaml` file includes an environment variable for the Slack connection that needs to be configured.

Ensure you have set up the required integrations and environment variables:

- [Atlassian Jira](https://docs.autokitteh.com/integrations/atlassian)
- [Slack](https://docs.autokitteh.com/integrations/slack)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/break_glass
```
Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the project directory:

   ```shell
   cd break_glass
   ```

2. Apply manifest and deploy the project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "break_glass/slack_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init slack_connection <connection ID>
ak connection init jira_connection <connection ID>
```

### Trigger the Workflow

The workflow is triggered by using a Slack slash command with the following text: `break-glass`. The text of the command can be configured in `autokitteh.yaml`.
