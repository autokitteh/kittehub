---
title: Leash - Incident Management & On-Call Escalation
description: Automated incident management system with on-call rotation, escalation workflows, and multi-channel notifications
integrations: ["googlesheets", "slack", "twilio", "gmail"]
categories: ["DevOps"]
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

## Why Build Your Own?

The entire incident management system is ~200 lines of Python. The hardest part - handling long-running workflows that survive restarts - is straightforward with AutoKitteh:

```python
from autokitteh import next_event, subscribe

# Subscribe to dashboard webhook responses
webhook_subscription = subscribe(
    "incident_dashboard_webhook",
    filter=f"data.method == 'POST' && data.url.query.unique_id == '{inc.unique_id}'"
)

# Wait for user action with automatic escalation
while inc.state.is_active:
    # This wait survives restarts. No external queue or state machine needed.
    data = next_event(webhook_subscription, timeout=timedelta(minutes=15))

    if data:
        # User clicked a button - handle it
        inc = handle_action(data.body.form, inc)
    else:
        # Timeout - escalate to next person
        inc = escalate_to_next_assignee(inc)
```

No message queues, no state machines, no orchestration frameworks. The workflow automatically resumes after restarts, preserving all state.

### What AutoKitteh Provides

- Durable workflows that can wait hours or days without consuming resources
- Built-in integrations (Slack, Gmail, Twilio, Google Sheets) with no configuration code
- Webhook endpoints with filtering and routing
- Event subscriptions without polling or queue management
- No infrastructure to set up or maintain

### vs. Commercial Platforms

- No per-user pricing
- Edit schedules directly in Google Sheets instead of navigating UI forms
- Change escalation logic by editing Python code
- See exactly how it works (check `incidents.py:45`)
- Own your data and code
- Deploy changes instantly

## How It Uses AutoKitteh

The system uses 4 AutoKitteh features:

```python
from autokitteh import next_event, subscribe, http_outcome, Event
```

1. **Durable Triggers** (`autokitteh.yaml`): Webhook triggers that create long-running sessions

   ```yaml
   triggers:
     - name: new_incident_webhook
       type: webhook
       call: handlers.py:on_new_incident_webhook
       is_durable: true
   ```

2. **Event Subscriptions** (`incidents.py:48`): Subscribe to filtered events

   ```python
   webhook_response_subscription = subscribe(
       "incident_dashboard_webhook",
       filter=f"data.method == 'POST' && data.url.query.unique_id == '{inc.unique_id}'"
   )
   ```

3. **Durable Waits** (`incidents.py:69`): Wait for events with timeouts

   ```python
   data = next_event(webhook_response_subscription, timeout=timedelta(minutes=15))
   ```

4. **HTTP Responses** (`handlers.py:25`): Return HTTP responses from workflows
   ```python
   http_outcome(status_code=201, json={"incident_id": inc.id})
   ```

The rest is regular Python business logic.

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
