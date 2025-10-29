---
title: Notion sample
description: Simple usage of the Notion API
integrations: ["notion"]
categories: ["Samples"]
---

# Notion Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=samples/notion)

The Notion sample demonstrates how to manage pages and databases using AutoKitteh's Notion integration.

The sample includes two separate workflows:

1. **Create page** - create a notion page
2. **Get Page info** - get the information about a certain page

API details:

- [Notion API](https://developers.notion.com/)
- [Python client library](https://github.com/ramnes/notion-sdk-py)

## How It Works

1. Create a new page in a Notion database with a custom title
2. Retrieve information about an existing page using its page ID

## Cloud Usage

1. Initialize your Notion connection through the UI
2. Copy the webhook trigger's URL (for the [Trigger Workflows](#trigger-workflows) section below):
   - Hover over the trigger's (i) icon for the webhook you want to use
   - Click the copy icon next to the webhook URL for your selected trigger
   - (Detailed instructions [here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Update the `DATABASE_ID` project variable with your Notion database ID

## Trigger Workflows

> [!IMPORTANT]
> Ensure your Notion integration has access to the database you want to use.

### Create a Page

```shell
curl -X POST "${WEBHOOK_URL}" -d "title=My New Page"
```

Replace `WEBHOOK_URL` with the URL of `create_page_webhook` webhook in the triggers section.

> [!NOTE]
> The `title` parameter is optional. If not provided, it defaults to `'AutoKitteh Page'`.

### Get Page Information

```shell
curl "${WEBHOOK_URL}?page_id=<PAGE_ID>"
```

- Replace `WEBHOOK_URL` with the URL of `get_page_webhook` webhook in the triggers section.
- Replace `<PAGE_ID>` with the ID of the Notion page you want to retrieve.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
