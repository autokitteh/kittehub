---
title: Bi-Weekly Release Notes Generator
description: Automated workflow that generates professional release notes from JIRA tickets and publishes them to Confluence with email notifications
integrations: ["jira", "confluence", "chatgpt", "gmail"]
categories: ["DevOps", "AI"]
tags: ["data_processing", "notifications", "ai_summaries", "automation"]
---

# Bi-Weekly Release Notes Generator

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=bi-weekly_release_notes)

This project automates the generation of professional release notes by fetching JIRA tickets, using ChatGPT to generate summaries, and publishing formatted pages to Confluence with optional email notifications.

## API Documentation

- [Atlassian Jira API](https://docs.autokitteh.com/integrations/atlassian/jira/python)
- [Atlassian Confluence API](https://docs.autokitteh.com/integrations/atlassian/confluence/python)
- [OpenAI ChatGPT API](https://docs.autokitteh.com/integrations/openai)
- [Gmail API](https://docs.autokitteh.com/integrations/google/gmail/python)

## How It Works

1. Fetch tickets from a specified JIRA filter (e.g., "Last Two Weeks Deliveries")
2. Categorize tickets into features/deliverables and bug fixes based on issue type
3. Generate AI-powered 2-3 sentence summaries for each ticket using ChatGPT
4. Create a formatted Confluence page with:
   - Organized sections for features and bug fixes
   - Ticket links and AI-generated descriptions
   - Timestamp and metadata
5. Send email notification with the release notes link to configured recipients

## Cloud Usage

1. Initialize your connections (Jira, Confluence, ChatGPT, and Gmail)

2. Set these project variables:

   - `JIRA_FILTER_ID`: Name or numeric ID of your JIRA filter (default: "Last Two Weeks Deliveries")
   - `CONFLUENCE_SPACE_KEY`: Confluence space key (default: "PRODUCT")
   - `CONFLUENCE_PARENT_PAGE_ID`: (Optional) Parent page ID for nested pages
   - `NOTIFICATION_EMAIL`: (Optional) Email address to receive notifications

3. Deploy the project

> [!IMPORTANT]
> Ensure all connections (Jira, Confluence, ChatGPT, Gmail) are properly initialized before the workflow starts running.

## Trigger Workflow

Deploy the project and the scheduled trigger will run it automatically (e.g., bi-weekly).

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI.

## Release Notes Format

The generated Confluence page includes:

```
Release Notes - [Month] - [Day] - [Year] - [Time]

🚀 New Features & Deliverables
• [TICKET-123]: Summary
  AI-generated description...

🐛 Bug Fixes
• [TICKET-456]: Summary
  AI-generated description...

---
Generated on [timestamp]
```

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- Maximum 100 tickets per JIRA filter request
- AI summaries are limited to 150 tokens
- Requires JIRA filter to be pre-configured
- Email notifications require Gmail connection
