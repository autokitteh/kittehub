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

## Why Build Your Own Instead of Using Existing Commercial Solutions?

Unlike off-the-shelf incident management platforms, Leash gives you complete control and simplicity:

- **Much Cheaper**: Avoid expensive per-user pricing. Run on AutoKitteh's infrastructure at a fraction of the cost of enterprise incident management platforms.
- **Simpler Management**: Edit schedules and contacts directly in Google Sheets - no fiddling with complex UI forms, schedule layers, or manual assignment workflows. Just update a spreadsheet cell.
- **Easy Customization**: Need to change escalation logic, notification format, or add custom actions? Just modify the code - no need to navigate complex UI settings or contact support.
- **Transparent Logic**: The entire workflow is visible in straightforward Python code, making it easy to understand, debug, and audit.
- **No Vendor Lock-in**: Own your data and workflows completely. Extend integrations without API limitations or pricing tiers.
- **Lightweight**: Use only what you need. No paying for unused features or dealing with overwhelming enterprise-focused interfaces.
- **Quick Iterations**: Deploy changes instantly without waiting for vendor roadmaps or feature requests.

Perfect for teams that value flexibility and want incident management that adapts to their workflow, not the other way around.

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

### Workflow Durability

Leash uses AutoKitteh's durability feature in the `new_incident` function to ensure incident workflows are reliable and persistent. When an incident is created, the workflow can:

- **Survive restarts**: If the system restarts during an escalation delay, the workflow resumes exactly where it left off
- **Wait indefinitely**: Escalation loops can wait for configured delays (minutes, hours, or days) without blocking resources
- **Maintain state**: All incident context and history is preserved throughout the lifecycle

This means you can confidently deploy updates or handle infrastructure changes without losing track of active incidents or interrupting escalation workflows.

## Usage

### Creating Incidents

Send a POST request to the `new_incident_webhook` URL with incident details:

```bash
curl -X POST https://api.autokitteh.cloud/webhooks/<WEBHOOK_SLUG> \
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

## Initial Setup

### Creating the Google Spreadsheet

Before deploying Leash, you need to create a Google Spreadsheet with three worksheets:

1. **Create a new Google Spreadsheet** in your Google Drive
2. **Create three worksheets** with these exact names:
   - `schedule` - Defines on-call schedules
   - `contacts` - Contains contact information
3. **Set up the `contacts` worksheet** with these column headers:

   ```
   name | email | phone
   ```

   Then add your contacts (see "Managing Contacts" section for details)

4. **Set up the `schedule` worksheet** with these column headers:

   ```
   start_time | end_time | assignees
   ```

   Then add your schedule rows (see "Managing Schedules" section for details)

5. **Copy the Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
   You'll need this ID for the `GOOGLE_SPREADSHEET_ID` configuration variable.

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
- **slack** (optional): Slack for DM notifications. Ignored if not initialized.
- **gmail** (optional): Gmail for email notifications. Ignored if not initialized.
- **twilio** (optional): Twilio for SMS notifications. Ignored if not initialized.

Only the Google Sheets connection is mandatory. All other connections are optional - if not initialized, they will simply not be used for notifications.

## Incident States

- **PENDING**: Incident created, waiting for assignment
- **ASSIGNED**: Assigned to someone, waiting for acknowledgment
- **IN_PROGRESS**: Someone acknowledged and is working on it
- **RESOLVED**: Incident resolved and closed
- **ERROR**: Error occurred during processing

## Development

Just run `make` to test locally.

To deploy to AutoKitteh, either hit the "Start With AutoKitteh" button above, or use the CLI:

1. Install the CLI https://docs.autokitteh.com/get_started/install
2. Authenticate: `ak auth login`
3. Deploy: `make deploy`
4. Login to https://autokitteh.cloud and initialize the connections and variables.
