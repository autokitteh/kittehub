---
title: Jira assignee from Google Calendar
description: Set assignee in Jira ticket to the person currently on-call
integrations: ["jira", "calendar"]
categories: ["DevOps"]
---

# Jira Assignee From Google Calendar

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=jira_google_calendar/assignee_from_schedule)

This project automates the process of assigning Jira issues based on a shared Google Calendar. The workflow checks the current on-call person from the Google Calendar and assigns newly created Jira issues to them.

## How It Works

1. Receive new Jira issue in the designated Jira project
2. Check the shared Google Calendar to identify the current on-call person
3. Assign the newly created Jira issue to the current on-call person

## Cloud Usage (Recommended)

1. Initialize your connections through the UI
2. Edit the `jira_issue_created` trigger, in the "TRIGGERS" tab, under the "Actions" column
3. Replace `JIRA_PROJECT_KEY` with your Jira project key
4. Set the `CALENDAR_ID` project variable to the ID of the shared Google Calendar
5. Deploy the project

> [!IMPORTANT]
> Ensure all connections (Jira, Google Calendar) are properly initialized before the workflow starts running.

## Trigger Workflow

Once deployed, the workflow is triggered by the creation of a new Jira issue, which prompts the assignment to the current on-call person according to the shared Google Calendar.

## Calendar Example

![Calendar Example](./images/calendar_example.png)

The image above illustrates a sample Google Calendar used in this workflow. Each event on the calendar represents an all-day on-call shift for a team member. The workflow checks this calendar to determine the current on-call person, which is then used to automatically assign newly created Jira issues to the person scheduled during that time.

## Self-Hosted Deployment

Follow these [detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
