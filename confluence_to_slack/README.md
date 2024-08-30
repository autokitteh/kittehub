
# Confluence To Slack Workflow 

This workflow automates notifications to a Slack channel whenever a new Confluence page is created in a specified space.

## Benefits

- **Small overhead**: Run the `ak` server, deploy the project, and write code.
- **Filtering**: Add filters in the configuration to limit the number of times your code is triggered, or filter data in the code itself. This workflow demonstrates both.

## How It Works

- **Trigger**: A new Confluence page is created in a designated space.
- **Result**: A Slack message is sent to a selected channel containing data from the newly created Confluence page.

## Known Limitations

- Confluence returns HTML, and this program does not format it in any way. The purpose of this workflow is to demonstrate how data can move between different services. Desired formatting can be easily added to suit individual needs.

## Additional Comment

- Environment variables are set in [`autokitteh.yaml`](./autokitteh.yaml) (e.g., Slack channel, Confluence page, etc.).

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

> [!IMPORTANT]
> The `autokitteh.yaml` file includes environment variables for the Confluence and Slack connections that need to be configured.

Ensure you have set up the required integrations and environment variables. This project uses Confluence and Slack APIs.

- [Atlassian Confluence](https://docs.autokitteh.com/integrations/atlassian)
- [Slack](https://docs.autokitteh.com/integrations/slack)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/
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
   cd confluence_to_slack
   ```

2. Apply manifest and deploy the project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml --file program.py
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "confluence_to_slack/slack_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init slack_connection <connection ID>
ak connection init confluence_connection <connection ID>
```

### Trigger the Workflow

Once the project has been properly installed, configured and deployed, the workflow will be triggered by an event from Confluence.
