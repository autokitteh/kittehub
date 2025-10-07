---
title: Leash - Incident Management & On-Call Escalation
description: Automated incident management system with on-call rotation, escalation workflows, and multi-channel notifications
integrations: ["googlesheets", "slack", "twilio", "gmail"]
categories: ["DevOps", "Monitoring"]
tags:
  [
    "webhook_handling",
    "long_running",
    "next_event",
    "subscribe",
    "interactive_workflows",
    "notifications",
    "monitoring",
    "sync_responses",
    "durable",
  ]
---

# Leash - Incident Management System

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=leash)

Leash is an automated incident management system that handles incident creation, assignment, escalation, and resolution. It uses Google Sheets as a storage backend for incidents, schedules, and contacts, and delivers notifications through Slack, email (Gmail), and SMS (Twilio).

## How It Works

1. **Incident Creation**: Incidents are created via webhook (POST request with incident details)
2. **Automatic Assignment**: System finds the current on-call person from the schedule stored in Google Sheets
3. **Notification**: Assigned person is notified via all available channels (Slack, email, SMS)
4. **Interactive Dashboard**: Each incident has a unique dashboard URL for taking actions
5. **Escalation Loop**: If no response within configured delay, incident escalates to the next person in rotation
6. **Resolution**: Incidents can be acknowledged, resolved, escalated, or reassigned through the dashboard

## Features

- **On-Call Rotation**: Define schedules with multiple assignees that rotate automatically
- **Multi-Channel Notifications**: Simultaneously notify via Slack DM, email, and SMS
- **Durable Workflows**: Incident workflows survive restarts and continue from where they left off
- **Interactive Dashboards**: Web-based incident dashboards with one-click actions
- **Automatic Escalation**: Configurable escalation delays with rotation through assignee list
- **Google Sheets Backend**: All data (incidents, schedules, contacts) stored in Google Sheets for easy management

## Usage

### Creating Incidents

Send a POST request to the `new_incident_webhook` URL with incident details:

```bash
curl -X POST https://api.autokitteh.cloud/webhooks/new_incident_webhook \
  -H "Content-Type: text/plain" \
  -d "Production database connection timeout - error rate spiking to 15%"
```

The webhook returns the created incident ID:

```json
{ "incident_id": "1" }
```

### Managing Schedules

Configure on-call schedules in the Google Sheets `schedule` worksheet:

| start_time       | end_time         | assignees                  |
| ---------------- | ---------------- | -------------------------- |
| 01-01-2025 00:00 | 12-31-2025 23:59 | alice@example.com, bob@... |

- Schedule rows define time periods with lists of assignees
- Assignees rotate automatically on each escalation
- Multiple schedules can overlap (first match wins)

### Managing Contacts

Add contacts in the Google Sheets `contacts` worksheet:

| name              | email             | phone       |
| ----------------- | ----------------- | ----------- |
| alice@example.com | alice@example.com | +1234567890 |
| bob@example.com   | bob@example.com   | +1987654321 |

Email and phone are optional, but email at least is recommended. Email is also used to find users in Slack if configured.

### Incident Dashboard Actions

Each incident has a unique dashboard URL sent with notifications. Available actions:

- **Take**: Manually take ownership of the incident (requires authentication)
- **Ack**: Acknowledge the incident and mark as in-progress
- **Resolve**: Mark the incident as resolved and close it
- **Escalate**: Manually escalate to the next person in rotation
- **Notify**: Re-send notifications to the current assignee

## Configuration

Configure the system using project variables in `autokitteh.yaml`:

- `GOOGLE_SPREADSHEET_ID`: ID of the Google Sheet storing all data (required)
- `ESCALATION_DELAY_MINUTES`: Minutes to wait before escalating (default: 15)
- `TZ`: Timezone for schedules (default: UTC)
- `FAIL_ON_NO_ASSIGNEE`: Whether to fail when no assignee found (default: false)
- `TS_FORMAT`: Datetime format for timestamps (default: `%m-%d-%Y %H:%M`)
- `TWILIO_PHONE_NUMBER`: Phone number to send SMS from (if using Twilio)

## Connections

- **gsheets** (required): Google Sheets for data storage
- **slack** (optional): Slack for DM notifications
- **gmail** (optional): Gmail for email notifications
- **twilio** (optional): Twilio for SMS notifications

## Incident States

- **PENDING**: Incident created, waiting for assignment
- **ASSIGNED**: Assigned to someone, waiting for acknowledgment
- **IN_PROGRESS**: Someone acknowledged and is working on it
- **RESOLVED**: Incident resolved and closed
- **ERROR**: Error occurred during processing
