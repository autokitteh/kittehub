---
title: Manage emergency AWS access requests via Slack
description: Submit emergency AWS access requests via Slack, which are then approved or denied based on a set of predefined conditions
integrations: ["slack", "jira"]
categories: ["DevOps"]
tags:
  [
    "approval_workflows",
    "interactive_workflows",
    "user_interactions",
    "activity",
  ]
---

# Break-Glass Request Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=break_glass)

This project implements a break-glass request workflow that allows users to submit emergency access requests via Slack, which are then approved or denied based on a set of predefined conditions. The project integrates Slack and Jira with custom modals and messages.

## How It Works

1. Users submit a `break-glass` request via a custom Slack modal.
2. The request is sent for approval to designated approvers.
3. Approvers can approve or deny the request via Slack.
4. The approval or denial is logged and the requester is notified.

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Set the `APPROVAL_CHANNEL` project variable to a Slack channel where the AutoKitteh app is invited
3. Deploy the project

## Trigger Workflow

The workflow is triggered by using a Slack slash command with the following text: `break-glass`. (Self-hosted only) The text of the command can be configured in `autokitteh.yaml`.

> [!IMPORTANT]
> Ensure all connections (Slack, Jira, and AWS) are properly initialized before the workflow starts running.

## Self-Hosted Deployment

#### Prerequisites

- [Install AutoKitteh](https://docs.autokitteh.com/get_started/install)
- Set up required integrations:
  - [Jira](https://docs.autokitteh.com/integrations/atlassian)
  - [Slack](https://docs.autokitteh.com/integrations/slack)

#### Installation Steps

1. Clone the repository:
   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   cd kittehub/break_glass
   ```

````

2. Start the AutoKitteh server:
   ```shell
   ak up --mode dev
````

3. Deploy the project:

   ```shell
   ak deploy --manifest autokitteh.yaml
   ```

   The output will show your connection IDs, which you'll need for the next step. Look for lines like:

   ```shell
   [exec] create_connection "break_glass/jira_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   [exec] create_connection "break_glass/slack_connection": con_01j36p9gj6e2nt87p9vap6rbmz created
   ```

   In this example, `con_01j36p9gj6e2nt87p9vap6rbmz` is the connection ID.

4. Initialize your connections using the CLI:
   ```shell
   ak connection init jira_connection <connection ID>
   ak connection init slack_connection <connection ID>
   ```
