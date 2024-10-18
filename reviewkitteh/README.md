# GitHub Pull Request to Slack Workflow

This project automates the process of listening for GitHub pull request events and posting updates to a Slack channel. The workflow tracks the state of the pull request and meows at random people from a Google Sheet in the Slack channel.

## How It Works

1. **Trigger**: The workflow is triggered by a GitHub pull request event (opened or reopened).
2. **Post to Slack**: The program posts an initial message to the Slack channel and continues to update the message as the pull request's state changes.
3. **Random Paging**: Every 15 seconds, the program selects a random person from a Google Sheet and pages them in the Slack channel.
4. **Completion**: The workflow continues until the pull request is closed or merged.

## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure integrations

> [!IMPORTANT]
>  The `autokitteh.yaml` file includes environment variables for the GitHub, Slack, and Google Sheets connections that need to be configured. When setting the `CHANNEL` variable, be sure to use the channel ID, not the channel name.

Ensure you have set up the required integrations:

- [GitHub](https://docs.autokitteh.com/integrations/github)
- [Google Sheets](https://docs.autokitteh.com/integrations/google)
- [Slack](https://docs.autokitteh.com/integrations/slack)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/reviewkitteh
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `reviewkitteh` directory:

```shell
cd reviewkitteh
```

2. Apply manifest and deploy the project by running the following command:

```shell
ak deploy --manifest autokitteh.yaml --file program.py
```

The output of this command will be important for initializing connections in the following step if you're using the CLI.

For example, for each configured connection, you will see a line that looks similar to the one below:

```shell
[exec] create_connection "reviewkitteh/slack_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
```

`con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initiliaze Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init my_github <connection ID>
ak connection init my_slack <connection ID>
ak connection init my_googlesheets <connection ID>
```

### Trigger the Workflow

Once deployed, the workflow is triggered by a GitHub pull request event and continues to run, updating Slack until the pull request is closed or merged.
