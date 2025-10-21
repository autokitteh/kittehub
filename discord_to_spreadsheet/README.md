---
title: Discord to Spreadsheet Workflow
description: Log Discord messages to a Google Sheets document automatically
integrations: ["discord", "googlesheets"]
categories: ["Productivity"]
tags: ["webhook_handling", "data_processing", "notifications"]
---

# Discord to Spreadsheet Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=discord_to_spreadsheet)

This project automates the process of logging Discord messages to a Google Sheets document. It captures message events from a Discord server and appends the author's username and message content into the specified spreadsheet. This is intended as a starting point rather than a complete solution.

## Benefits

- **Ease of Use:** Demonstrates how simple it is to connect Discord and Google Sheets into an automated workflow.
- **Low Complexity:** The workflow is implemented with minimal code and setup.
- **Free and Open Source:** Available for use or modification to fit specific use cases.

## How It Works

- **Detect Discord Message:** The program listens for new message events in a Discord server using the Discord API.
- **Log Message to Google Sheets:** The message author's username and content are appended to the designated range in a Google Sheets document using the Google Sheets API.

## Installation and Usage

> [!NOTE]
> This sample currently works only on the local version of AutoKitteh and is not compatible with the cloud version.

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

- [Discord](https://docs.autokitteh.com/integrations/discord/connection)
- [Google Sheets](https://docs.autokitteh.com/integrations/google/config)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/discord_to_spreadsheet
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the `discord_to_spreadsheet` directory:

   ```shell
   cd discord_to_spreadsheet
   ```

2. Apply manifest and deploy project by running the following command:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output of this command will be important for initializing connections in the following step if you're using the CLI.

   For example, for each configured connection, you will see a line that looks similar to the one below:

   ```shell
   [exec] create_connection "discord_to_spreadsheet/discord_conn": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

> [!IMPORTANT]
> `googlesheets_conn` and `discord_conn` need to be initialized using the IDs from the previous step.

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init discord_conn <connection ID>
ak connection init googlesheets_conn <connection ID>
```

### Trigger the Workflow

The workflow is triggered when a message is sent in a Discord server where the bot is present.
