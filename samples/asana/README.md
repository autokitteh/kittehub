---
title: Asana
description: Simple usage of the Asana API
integrations: ["asana"]
categories: ["Samples"]
---

# Asana Sample

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
 2. Update the `WORKSPACE_GID` variable with the gid value from the response after logging into Asana and visiting https://app.asana.com/api/1.0/workspaces
 3. Edit the trigger of the workflow you want to trigger, in the "TRIGGERS" tab, under the "Actions" column
 4. Copy the provided webhook URL
 5. Send GET request to the webhook of your choice

## Trigger Workflow

- For `create_task`:
       ```shell
       curl "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}" 
       ```
- For `update_task`:
       ```shell
       curl "https://api.autokitteh.cloud/webhooks/{your-webhook-slug}" \
            -d task_gid=<task_gid> \
            -d new_due_date=<new_date> \
            -d name_suffixe=<added_name>
       ```

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

