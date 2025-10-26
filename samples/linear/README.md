---
title: Linear sample
description: Simple usage of the Linear API
integrations: ["linear"]
categories: ["Samples"]
---

# Linear Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/linear)

The Linear sample demonstrates how to manage issues using AutoKitteh's Linear integration.

It features functionality to create new issues within a Linear team, retrieve information about existing issues, and update issue properties.

API details:

- [Linear API](https://developers.linear.app/docs)
- [Python client library](https://github.com/linear/linear-client-python)

## How It Works

1. Create a new issue in Linear with a custom title and description
2. Retrieve information about an existing issue using its issue ID
3. Update an issue's title or state

## Cloud Usage

1. Initialize your Linear connection through the UI
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):
   - Hover over the trigger's (i) icon for the webhook you want to use
   - Click the copy icon next to the webhook URL for your selected trigger
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Update the `TEAM_ID` project variable with your Linear team ID
   - You can find your team ID in Linear's URL: `https://linear.app/team/<TEAM_ID>/...`

## Trigger Workflows

### Create an Issue

```shell
curl -X POST "${WEBHOOK_URL}" \
  -d "title=Fix login bug" \
  -d "description=Users are unable to login with SSO"
```

> [!NOTE]
> Both `title` and `description` parameters are optional. If not provided, they default to `'AutoKitteh Issue'` and `'Created by AutoKitteh'`.

### Get Issue Information

```shell
curl "${WEBHOOK_URL}?issue_id=<ISSUE_ID>"
```

Replace `<ISSUE_ID>` with the ID of the Linear issue you want to retrieve.

### Update an Issue

```shell
curl -X POST "${WEBHOOK_URL}" \
  -d "issue_id=<ISSUE_ID>" \
  -d "title=Updated issue title" \
  -d "state_id=<STATE_ID>"
```

Replace `<ISSUE_ID>` with the issue ID and optionally provide a new `title` or `state_id`.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
