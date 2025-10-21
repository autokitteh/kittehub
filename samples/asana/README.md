---
title: Asana sample
description: Simple usage of the Asana API
integrations: ["asana"]
categories: ["Samples"]
---

# Asana Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/asana)

The Asana sample demonstrates how to streamline task management using AutoKitteh's Asana integration.

It features functionality to create tasks within a workspace and update existing ones,
including changes to their names and due dates.

API details:

- [Asana API](https://developers.asana.com/docs/quick-start)
- [Python client library](https://developers.asana.com/docs/migration-guide-python-v5)

## How It Works

1. Create a new task in asana
2. Update the name and the due date of an existing task

## Cloud Usage (Recommended)

1. Initialize your connection through the UI
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):

   - Hover over the trigger's (i) icon for the webhook you want to use
   - Click the copy icon next to the webhook URL for your selected trigger
   - (Detailed instructions
     [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

3. Update the `WORKSPACE_GID` project variable with the `gid` value from the response after logging into Asana and visiting https://app.asana.com/api/1.0/workspaces

## Trigger Workflows

`create_task`:

```shell
curl -i "${WEBHOOK_URL}" --url-query name=<TASK_NAME>
```

`update_task`:

```shell
curl -X POST "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}" \
       -d task_gid=<task_gid> \
       -d new_due_date=<new_date> \
       -d name_suffixe=<added_name>
```

> [!NOTE]
> The `name` query parameter is optional. If not provided, it defaults to `'autokitteh task'`.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
