---
title: Google Drive
description: Samples using Google Drive APIs
integrations: ["drive"]
categories: ["Samples"]
---

# Google Drive Sample

This AutoKitteh project demonstrates 2-way integration with
[Google Drive](https://workspace.google.com/products/drive/).

## API Documentation

- https://docs.autokitteh.com/integrations/google/drive/python
- https://docs.autokitteh.com/integrations/google/drive/events

## Usage Instructions

1. Run this command to create a new file in your Google Drive:

   ```shell
   curl -i "http://localhost:9980/webhooks/<webhook-slug>"
   ```

2. Check the responses in your terminal after making the requests.

3. Create/update/delete files in your Google Drive to trigger events that will be
   handled by the AutoKitteh server.

4. Check out the resulting session logs in the AutoKitteh server.

## Setup Instructions (for self-hosted servers)

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud

2. Optional for self-hosted servers (preconfigured in AutoKitteh Cloud):
   [enable Google connections to use OAuth 2.0](https://docs.autokitteh.com/integrations/google/config)

> [!NOTE]
> No need to configure GCP Cloud Pub/Sub for this sample - only the Gmail and
> Google Forms integrations require it.

3. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/google/drive/autokitteh.yaml
   ```

4. Look for the following line in the output of the `ak deploy` command, and
   copy the URL path for later:

   ```
   [!!!!] trigger "list_events" created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run this command
> instead, and use the webhook slug from the output:
>
> ```shell
> ak trigger get list_events --project google_drive_sample -J
> ```

5. Initialize this project's Google Drive connection, with user impersonation
   using OAuth 2.0 (based on step 2), or a GCP service account's JSON key

> [!TIP]
> The exact CLI command to do so (`ak connection init ...`) will appear in the
> output of the `ak deploy` command from step 3 when you create the project on
> the server, i.e. when you run that command for the first time.
