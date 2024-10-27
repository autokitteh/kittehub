---
title: AWS Health to Slack
description: Monitor AWS health events
integrations: ["aws", "slack", "sheets"]
categories: ["DevOps"]
---

# Announce AWS Health Events in Slack

This project automates the process of announcing AWS health events in Slack based on resource ownership listed in a Google Sheet. It leverages AWS Health API to fetch events and Google Sheets to map projects to Slack channels. This is not meant to be a complete solution but a solid starting point.

## How It Works

1. Fetches AWS Health events from AWS API.
2. Reads project-to-Slack-channel mappings from a Google Sheet.
3. Posts relevant health events to the corresponding Slack channels based on the Google Sheet data.

## How It Works

1. Fetches AWS Health events from AWS API.
2. Reads project-to-Slack-channel mappings from a Google Sheet.
3. Posts relevant health events to the corresponding Slack channels based on the Google Sheet data.

### Google Sheets Data

The default Google Sheet used for mapping projects to Slack channels is as follows:

| Project Tag | Slack Channel      |
|-------------|--------------------|
| clubs       | clubs_team         |
| diamonds    | diamonds_alerts    |
| hearts      | hearts_oncall      |
| spades      | C12345678          |

This table represents how each project is linked to a specific Slack channel, guiding where health events will be posted.

> [!NOTE] You can configure your own project-to-Slack-channel mappings by specifying a different Google Sheet in the [`autokitteh.yaml`](autokitteh.yaml) file.


## Installation and Usage 

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)

### Configure Integrations

Ensure you have set up the required integrations and environment variables. This project uses Google Sheets, AWS Health API, and Slack API.

- [Google Sheets](https://docs.autokitteh.com/integrations/google)
- [Slack](https://docs.autokitteh.com/integrations/slack)

### Clone the Repository

```shell
git clone https://github.com/autokitteh/kittehub.git
cd kittehub/aws_health_to_slack
```

Alternatively, you can copy the individual files in this directory.

### Run the AutoKitteh Server

Simply run this command:

```shell
ak up --mode dev
```

### Apply Manifest and Deploy Project

1. Navigate to the aws_health_slack directory:

```shell
cd aws_health_slack
```

2. Apply manifest and deploy project by running the following command:

```shell
ak deploy --manifest autokitteh.yaml
```

The output of this command will be important for initializing connections in the following step if you're using the CLI.

For example, for each configured connection, you will see a line that looks similar to the one below:

```shell
[exec] create_connection "aws_health_slack/google_sheets_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
```

`con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

### Initialize Connections

Using the connection IDs from the previous step, run these commands:

```shell
ak connection init aws_connection <connection ID>
ak connection init google_sheets_connection <connection ID>
ak connection init slack_connection <connection ID>
```

### Trigger the Workflow

The workflow is triggered automatically after deployment to run every minute. The interval can be configured in `autokitteh.yaml`.
