# Slack-Discord Message Mirroring Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=slack_discord_sync)

This project automates the process of mirroring messages between Slack and Discord channels. It listens for new message events in Discord or Slack and sends them to the corresponding channel on the other platform. This project is intended as a starting point rather than a complete solution.

## Benefits

- **Cross-Platform Communication:** Automatically mirrors messages between Discord and Slack, keeping teams connected across both platforms.
- **Ease of Use:** Demonstrates how to easily integrate AutoKitteh with Slack and Discord APIs.
- **Low Complexity:** The workflow is implemented with minimal code and setup.

## How It Works

- **Detect Discord and Slack Messages:** The program listens for new message events in Discord or Slack.
- **Mirror Messages:** When a message is sent in one platform, it is immediately forwarded to the corresponding channel on the other platform.

## Installation and Usage

> [!NOTE]
> This sample currently works only on the local version of AutoKitteh and is not compatible with the cloud version.

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

- [Discord](https://docs.autokitteh.com/integrations/discord/connection)
- [Slack](https://docs.autokitteh.com/integrations/slack/config)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/slack_discord_sync
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `slack_discord_sync` directory:

   ```shell
   cd slack_discord_sync
   ```

2. Apply manifest and deploy project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "slack_discord_sync/discord_conn": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

> [!IMPORTANT]
> `slack_conn` and `discord_conn` need to be initialized using the IDs from the previous step.

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init discord_conn <connection ID>
ak connection init slack_conn <connection ID>
```

### Trigger the Workflow

The workflow is triggered when a message is sent in either Slack or Discord, where the bot is present.
