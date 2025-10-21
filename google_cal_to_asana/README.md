---
title: Google Calendar To Asana
description: Creates Asana tasks based on Google Calendar events
integrations: ["googlecalendar", "asana"]
categories: ["Productivity"]
tags: ["webhook_handling", "data_processing", "notifications"]
---

# Google Calendar To Asana

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=google_cal_to_asana)

This project automates task creation by integrating Google Calendar and Asana.

## API Documentation

- Google Calendar: https://docs.autokitteh.com/integrations/google/calendar
- Asana: https://docs.autokitteh.com/integrations/asana

## How It Works

1. Monitor specified Google Calendar for new event creation
2. Extract event details (title, description, date/time)
3. Create corresponding Asana task with extracted information

## Cloud Usage

1. Initialize your connections (Google Calendar and Asana)

> [!IMPORTANT]
> When setting up the Google Calendar connection, specify the ID of a calendar that you own, to receive notifications about new events.

2. Set the `ASANA_PROJECT_GID` variable in the project settings

> [!TIP]
> You can find the GID in the URL of the Asana project. It is the part after `/0/`. For example, in `https://app.asana.com/0/your_project_gid/list` it's `your_project_gid`.

3. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure both Google Calendar and Asana connections are initialized; otherwise, the workflow will raise a `ConnectionInitError`.

The workflow is triggered automatically when a new event is created in the specified Google Calendar.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
