# Projects Overview

| Title | Description | Integrations |
|-------|-------------|--------------|
| Parse a file in S3 and insert to database | Triggered by a new GPX file on an S3 bucket, the pipeline code will parse the GPX file and insert it into a database. | aws, http, sqlite3 |
| AWS Health to Slack | Monitor AWS health events | aws, slack, sheets |
| Quickstart | Sample for quickstart | http |
| Create Jira Ticket from a Webhook data | Create Jira Ticket from a Webhook data | jira, http |
| Slack notify on Confluence page created | When Confluence page is created the user will be notified on Slack | confluence, slack |
| OpenAI ChatGPT | Samples using chatGPT APIs | chatgpt |
| Discord Client | Samples using Discord APIs | discord |
| Discord Events | Samples using Discord events | discord |
| Google Calendar | Samples using Google Calendar APIs | calendar |
| Google Sheets | Samples using Google Sheets APIs | sheets |
| Google Forms | Samples using Google Forms APIs | forms |
| Gmail | Samples using Gmail APIs | gmail |
| Scheduler | Samples using cron scheduler for workflows | scheduler |
| Runtime Events | Samples using events in AutoKitteh - subscribe(), next_event(), unsubscribe() | autokitteh |
| GitHub | Samples using GitHub APIs | github |
| Jira | Samples using Jira APIs | jira |
| HTTP | Samples using HTTP requests and webhooks | http |
| Slack | Samples using Slack APIs | slack |
| Twilio | Samples using Twilio APIs | twilio |
| Manage emergency AWS access requests via Slack | Submit emergency AWS access requests via Slack, which are then approved or denied based on a set of predefined conditions | aws, slack |
| Github Actions | GitHub workflows that interact across multiple repositories | github |
| Monitor PR until completion in Slack | Create a Slack channel for each PR, update team leads until completion | slack, github, sheets |
| Create Jira ticket from Google form | Trigger by HTTP request, continue polling Google forms, and create Jira ticket based on the form's data | forms, http, jira |
| Log Discord messages to Sheets | Logging Discord messages to a Google Sheets document | discord, sheets |
| Fault tolerant workflow with manual Slack approvals | Runs a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure. | slack |
| Slack bot for assistance requests with AI categorization | Slack bot request for assistance is inferred using Google's Gemini AI. The appropriate person is mentioned according to a predetermined table of expertise in a Google Doc. The person can then `!take` the request and later `!resolve` it. | slack, googlegemini |
| Pull Request Review Reminder (Purrr) | Purrr integrates GitHub and Slack efficiently, to streamline code reviews and cut down the turnaround time to merge pull requests. | github, slack |
| JIRA Assignee From Google Calendar Workflow | Set Assignee in Jira ticket to the person currently on-call | jira, calendar |
| Create calendar due date event for Jira ticket | When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline | calendar, jira |
| Slack Discord Sync | Sync Discord and Slack channel | slack, discord |
| Slack notify on important Email | Categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack | gmail, slack, chatgpt |
| Unregister non active users from Copilot | If Copilot was not used in a preceding period by users, the workflow automatically unregisters and notifies them. Users can ask for their subscription to be reinstated. | githubcopilot, slack |
| Google Calendar To Asana | Creates Asana tasks based on Google Calendar events | calendar, asana |
| Ad-hoc room reservation via Slack | Ad-hoc room reservation via Slack slash commands | slack, calendar |
