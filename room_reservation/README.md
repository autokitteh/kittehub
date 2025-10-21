---
title: Ad-hoc room reservation via Slack
description: Ad-hoc room reservation via Slack slash commands
integrations: ["slack", "googlecalendar"]
categories: ["Productivity"]
tags: ["user_interactions", "webhook_handling", "data_processing", "error_handling"]
---

# Room Reservarion

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=room_reservation)

This project automates the process of room reservations through Slack by integrating Google Calendar, Google Sheets, and Slack. It is not meant to be a 100% complete project, but rather a solid starting point.

## How It Works

1. Receive room reservation requests from Slack commands
2. Query Google Calendar for room availability
3. Create calendar events for approved reservations
4. Update room status in Google Sheets

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Set the `GOOGLE_SHEET_ID` project variable, in the "VARIABLES" tab, to point to your Google Sheet
3. Deploy the project

## Trigger Workflow

The workflow is triggered with a Slack slash command.

### Available Commands

- `/autokitteh availablerooms` - list all the available rooms
- `/autokitteh roomstatus <room>` - check the status of a specific room
- `/autokitteh reserveroom <room> <title>` - reserve a specific room

> [!IMPORTANT]
> For self-hosted, replace `/autokitteh` with your app's name (e.g., `/yourapp availablerooms`).

> [!NOTE]
> Separate slash commands are not configured in Slack. Instead, the /autokitteh command is used, and the text that follows it is parsed to determine the desired action.

## Configuration

The list of meeting rooms is stored in a Google Sheet with the following format:

|     |          A          |
| :-: | :-----------------: |
|  1  | `room1@example.com` |
|  2  | `room2@example.com` |
|  3  | `room3@example.com` |

> [!TIP]
> This project can be extended to support additional features like adding participants, custom time slots, and room aliases.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
