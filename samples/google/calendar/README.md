---
title: Google Calendar sample
description: Samples using Google Calendar APIs
integrations: ["calendar"]
categories: ["Samples"]
---

# Google Calendar Sample

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/google/calendar)

This AutoKitteh project demonstrates 2-way integration with
[Google Calendar](https://workspace.google.com/products/calendar/).

API Documentation:

- https://docs.autokitteh.com/integrations/google/calendar/python
- https://docs.autokitteh.com/integrations/google/calendar/events

## How It Works

- List Calendar Events - Fetch upcoming events from Google Calendar using the Calendar API
- Monitor Calendar Changes - Watch for event modifications (create/update/delete)
- Process Calendar Events - Handle and log all calendar event changes

## Cloud Usage

1. Initialize your connection with Google Calendar
2. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Deploy the project

## Trigger Workflow

1. Start a long-running AutoKitteh session by sending an HTTP GET request to the webhook URL from step 2 in the [Cloud Usage](#cloud-usage) section above:

   ```shell
   curl -i "${WEBHOOK_URL}"
   ```

2. Create/Edit/Delete an event in Google Calendar to trigger the corresponding event handlers:
   - Creating triggers on_calendar_event_created
   - Updating triggers on_calendar_event_updated
   - Deleting triggers on_calendar_event_deleted

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
