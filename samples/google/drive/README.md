---
title: Google Drive sample
description: Samples using Google Drive APIs
integrations: ["drive"]
categories: ["Samples"]
---

# Google Drive Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/google/drive)

This project automates Google Drive file monitoring and management by integrating with the Google Drive API. It demonstrates creating new documents, monitoring file changes, and handling Drive events through AutoKitteh's Google Drive integration.

API documentation:

- Google Drive API: https://docs.autokitteh.com/integrations/google/drive
- Google Drive Events: https://docs.autokitteh.com/integrations/google/drive/events

## How It Works

1. Create new Google Drive documents programmatically
2. Monitor file changes in real-time using Drive's change notification system

## Cloud Usage

1. Initialize your Google Drive connection.
2. Deploy the project
3. Copy the webhook trigger's URL:
   - Hover over the trigger's (i) icon
   - Click the copy icon next to the webhook URL
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

## Trigger Workflow

> [!IMPORTANT]
> Ensure the Google Drive connection is initialized; otherwise, workflows raise `ConnectionInitError`.

1. Create a new document:

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>"
   ```

2. Monitor file changes by creating, updating, or deleting files in your connected Drive

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- Currently, we are restricted to the `drive.file` scope, which means only files created by the app can be monitored
