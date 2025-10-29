---
title: Linear sample
description: Simple usage of the Linear API
integrations: ["linear"]
categories: ["Samples"]
---

# Linear Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/linear)

The Linear sample demonstrates how to manage issues using AutoKitteh's Linear integration.

The sample includes three separate workflows:

1. **Create Issue** - Create new issues within a Linear team
2. **Get Issue** - Retrieve information about existing issues
3. **Update Issue** - Update issue properties like title or state

API details:

- [Linear API](https://developers.linear.app/docs)

## How It Works

- Create a new issue in Linear with a custom title and description
- Retrieve information about an existing issue using its issue ID
- Update an issue's title or state

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
  -d "title=<Replace with the title of the issue>" \
  -d "description=<Replace with the description of the issue>"
```

- Replace `WEBHOOK_URL` with the URL of `create_issue_webhook` webhook in the triggers section.
- Provide a title and a description.

> [!NOTE]
> Both `title` and `description` parameters are optional. If not provided, they default to `'AutoKitteh Issue'` and `'Created by AutoKitteh'`.

### Get Issue Information

```shell
curl "${WEBHOOK_URL}?issue_id=<ISSUE_ID>"
```

- Replace `WEBHOOK_URL` with the URL of `get_issue_webhook` webhook in the triggers section.
- Replace `<ISSUE_ID>` with the ID of the Linear issue you want to retrieve.

### Update an Issue

```shell
curl -X POST "${WEBHOOK_URL}" \
  -d "issue_id=<ISSUE_ID>" \
  -d "title=Updated issue title" \
  -d "state_id=<STATE_ID>"
```

- Replace `WEBHOOK_URL` with the URL of `update_issue_webhook` webhook in the triggers section.
- Replace `<ISSUE_ID>` with the issue ID, provide a new `title` and optionally provide a `state_id`.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
