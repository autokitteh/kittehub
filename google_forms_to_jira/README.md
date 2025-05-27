---
title: Create Jira ticket from Google form
description: Create and update Jira tickets automatically from Google Forms responses
integrations: ["forms", "jira"]
categories: ["DevOps"]
---

# Create Jira ticket from Google form

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=google_forms_to_jira)

This project automates ticket creation and updates in Jira based on Google Forms responses, enabling seamless integration between form submissions and issue tracking.

## API Documentation

- Google Forms: https://docs.autokitteh.com/integrations/google/forms/events
- Atlassian Jira: https://docs.autokitteh.com/integrations/atlassian/jira/python

## How It Works

1. Monitor Google Forms for new or edited responses
2. Extract and format response data into a structured summary
3. Create new Jira issues for new responses or update existing issues for edited responses

## Cloud Usage

1. Initialize your connections (Google Forms and Jira)

> [!IMPORTANT]
> When setting up the Google Forms connection, specify the ID of a form that you own, to receive notifications about new responses.

2. Set the `JIRA_PROJECT_KEY` project variable

> [!TIP]
> You can find the project key in the URL of the Jira project. It is the part after `/projects/`. For example, in `https://<your-domain>.atlassian.net/jira/software/projects/<PROJECT_KEY>/boards/<board-id>` it's `PROJECT_KEY`.

3. Deploy project

## Trigger Workflow

1. Submit a response to your configured Google Form
2. The workflow automatically creates a new Jira issue in your specified project
3. If form editing is enabled, editing a response updates the corresponding Jira issue

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.
