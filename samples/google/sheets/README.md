---
title: Google Sheets sample
description: Samples using Google Sheets APIs
integrations: ["googlesheets"]
categories: ["Samples"]
---

# Google Sheets Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/google/sheets)

This AutoKitteh project demonstrates 2-way integration with
[Google Sheets](https://workspace.google.com/products/sheets/).

## API Documentation

https://docs.autokitteh.com/integrations/google/sheets/python

## How It Works

1. Processes HTTP GET requests with a Google Sheets ID in the URL
2. Writes various data types, including formulas, to a specified Google Sheet
3. Reads and prints both formatted and unformatted cell values
4. Retrieves and prints formula details and their evaluated results

## Trigger Workflow

1. Copy the Google Sheets ID from the URL (the string between `/d/` and `/edit`)

2. Copy the webhook URLs from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))

3. Make an HTTP request:

   ```shell
   curl -i "${WEBHOOK_URL}" --url-query id=<Google-Sheet-ID>
   ```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
