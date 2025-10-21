---
title: Create calendar due date event for Jira ticket
description: When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline
integrations: ["googlecalendar", "jira"]
categories: ["DevOps"]
tags: ["webhook_handling", "data_processing", "notifications"]
---

# Jira to Google Calendar Workflow

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=jira_google_calendar/deadline_to_event)

This project automates the process of creating Google Calendar events based on Jira issue creation. When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline to ensure that the required tasks are completed on time.

## How It Works

1. Receive new Jira issue creation
2. Create Google Calendar event using Jira issue details like due date and description
3. Notify attendees when the event is added to Google Calendar

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Edit the `jira_issue_created` trigger, in the "TRIGGERS" tab, under the "Actions" column
3. Replace `JIRA_PROJECT_KEY` with your Jira project key
4. Deploy the project

> [!IMPORTANT]
> Ensure all connections (Jira, Google Calendar) are properly initialized before the workflow starts running.

## Trigger Workflow

The workflow is triggered by the creation of a new Jira issue, which prompts the creation of a Google Calendar event according to the issue's details.

## Known Limitations

- Attendees are hard-coded and arbitrary.
- Error handling is not implemented for demo purposes. For example, if the Jira issue is missing any of the required fields (e.g., `description`, `duedate`), the program will not fail gracefully.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
