<!--
Template Instructions:
- Remove these comment blocks after using
- Replace all {PLACEHOLDERS} with your content
- Delete any optional sections you don't need
- Keep the formatting (---, #, ##, etc.)
- Suggested formats and examples are provided for guidance.
-->

---

title: {PROJECT_NAME} <!-- Provide a short, descriptive name for your project -->
description: {ONE_LINE_DESCRIPTION} <!-- One-line summary of what the workflow does, avoid filler words -->
integrations: {LIST_OF_INTEGRATIONS} <!-- e.g., ["jira", "calendar"] -->
categories: {LIST_OF_CATEGORIES} <!-- e.g., ["DevOps"] -->
tags: {LIST_OF_TAGS} <!-- e.g., ["webhook_handling", "data_processing"] -->

---

# {PROJECT_NAME} <!-- Same as the title above, but capitalized -->

<!-- Replace with 2-3 sentences describing what your workflow does -->

This project automates {PRIMARY_AUTOMATION_TASK} by integrating {LIST_OF_INTEGRATIONS_PROSE} <!-- Write a sentence or two about the integrations used (e.g., "integrating Jira and Google Calendar for seamless task management"). -->

<!-- Optional section - Include only if API documentation is relevant -->

API documentation:

- {API_DOCUMENTATION} <!-- e.g., "Atlassian Jira: https://docs.autokitteh.com/integrations/atlassian/jira" -->

## How It Works

<!-- List 2-5 main steps of your workflow -->
<!-- Use action verbs to clearly describe each step -->

1. {STEP_1} <!-- e.g., "Detect new Jira issues" -->
2. {STEP_2} <!-- e.g., "Create corresponding Google Calendar events" -->
3. {STEP_3} <!-- Add more steps as needed -->

## Cloud Usage

1. Initialize your connections ({LIST_OF_INTEGRATIONS_PROSE})
2. {CONFIGURATION_STEP} <!-- e.g., "Edit the trigger settings" -->
<!-- If using a webhook trigger, add this as an additional step:
3. Copy the webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
   -->
4. {CONFIGURATION_STEP} <!-- Add more steps as needed -->
5. <!-- If the trigger is simple and differs from the Self-Hosted Deployment section, it can be included here. -->
6. Deploy project

<!-- Use ### if the trigger workflow differs from the Self-Hosted Deployment section or if the trigger instructions are complex -->

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections ({LIST_OF_INTEGRATIONS_PROSE}) are initialized; otherwise, the workflow will raise a `ConnectionInitError`.

<!-- Option 1: List of steps -->

1. {TRIGGER_STEP_1} <!-- e.g., "Navigate to your Jira project settings" -->
2. {TRIGGER_STEP_2} <!-- e.g., "Set up a webhook with the following URL: ..." -->
3. {TRIGGER_STEP_3} <!-- e.g., "Configure the webhook to trigger on issue updates" -->

<!-- OR Option 2: Simple description -->

{TRIGGER_DESCRIPTION} <!-- e.g., "Triggered via a webhook from Jira when an issue is updated." -->

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

<!-- Optional section - include only if self-hosted triggering differs from the section under Cloud Usage -->

### Trigger Workflow

<!-- Optional section -->

## Known Limitations

- {LIMITATION_1} <!-- e.g., "Does not support Socket Mode." -->
- {LIMITATION_2} <!-- e.g., "The polling mechanism is basic." -->

<!-- Optional section -->

## Visual Example

![Example Image](./images/{IMAGE_NAME})
{IMAGE_DESCRIPTION} <!-- Briefly describe the image, e.g., "A flowchart showing the integration process." -->
