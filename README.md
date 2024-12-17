# Kittehub

This is a central repository of [AutoKitteh](https://github.com/autokitteh/autokitteh)
projects for:

- Full-fledged, ready-to-use solutions for real-life use cases
- Composable templates for interoperability between common services
- Demonstrations of advanced system capabilities and features

In addition, the [samples](./samples/) directory contains projects that
demonstrate basic system features, integration APIs, and best practices.

<!-- START-TABLE -->
| Name | Description | Integration |
| :--- | :---------- | :---------- |
| [Parse a file in S3 and insert to database](./data_pipeline/) | Triggered by a new GPX file on an S3 bucket, the pipeline code will parse the GPX file and insert it into a database. | aws, http, sqlite3 |
| [AWS Health to Slack](./aws_health_to_slack/) | Monitor AWS health events | aws, slack, sheets |
| [Quickstart](./quickstart/) | Sample for quickstart | http |
| [Create Jira Ticket from a Webhook data](./webhook_to_jira/) | Create Jira Ticket from a Webhook data | jira, http |
| [Slack notify on Confluence page created](./confluence_to_slack/) | When Confluence page is created the user will be notified on Slack | confluence, slack |
| [OpenAI ChatGPT](./samples/openai_chatgpt/) | Samples using chatGPT APIs | chatgpt |
| [Discord Client](./samples/discord/discord_client/) | Samples using Discord APIs | discord |
| [Discord Events](./samples/discord/events/) | Samples using Discord events | discord |
| [Google Calendar](./samples/google/calendar/) | Samples using Google Calendar APIs | calendar |
| [Google Sheets](./samples/google/sheets/) | Samples using Google Sheets APIs | sheets |
| [Google Forms](./samples/google/forms/) | Samples using Google Forms APIs | forms |
| [Gmail](./samples/google/gmail/) | Samples using Gmail APIs | gmail |
| [Scheduler](./samples/scheduler/) | Samples using cron scheduler for workflows | scheduler |
| [Runtime Events](./samples/runtime_events/) | Samples using events in AutoKitteh - subscribe(), next_event(), unsubscribe() | autokitteh |
| [GitHub](./samples/github/) | Samples using GitHub APIs | github |
| [Jira](./samples/atlassian/jira/) | Samples using Jira APIs | jira |
| [HTTP](./samples/http/) | Samples using HTTP requests and webhooks | http |
| [Slack](./samples/slack/) | Samples using Slack APIs | slack |
| [Twilio](./samples/twilio/) | Samples using Twilio APIs | twilio |
| [Manage emergency AWS access requests via Slack](./break_glass/) | Submit emergency AWS access requests via Slack, which are then approved or denied based on a set of predefined conditions | aws, slack |
| [Github Actions](./github_actions/) | GitHub workflows that interact across multiple repositories | github |
| [Monitor PR until completion in Slack](./reviewkitteh/) | Create a Slack channel for each PR, update team leads until completion | slack, github, sheets |
| [Create Jira ticket from Google form](./google_forms_to_jira/) | Trigger by HTTP request, continue polling Google forms, and create Jira ticket based on the form's data | forms, http, jira |
| [Log Discord messages to Sheets](./discord_to_spreadsheet/) | Logging Discord messages to a Google Sheets document | discord, sheets |
| [Fault tolerant workflow with manual Slack approvals](./task_chain/single_workflow/basic/) | Runs a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure. | slack |
| [Slack bot for assistance requests with AI categorization](./slack_support/) | Slack bot request for assistance is inferred using Google's Gemini AI. The appropriate person is mentioned according to a predetermined table of expertise in a Google Doc. The person can then `!take` the request and later `!resolve` it. | slack, googlegemini |
| [Pull Request Review Reminder (Purrr)](./purrr/) | Purrr integrates GitHub and Slack efficiently, to streamline code reviews and cut down the turnaround time to merge pull requests. | github, slack |
| [JIRA Assignee From Google Calendar Workflow](./jira_google_calendar/assignee_from_schedule/) | Set Assignee in Jira ticket to the person currently on-call | jira, calendar |
| [Create calendar due date event for Jira ticket](./jira_google_calendar/deadline_to_event/) | When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline | calendar, jira |
| [Slack Discord Sync](./slack_discord_sync/) | Sync Discord and Slack channel | slack, discord |
| [Slack notify on important Email](./categorize_emails/) | Categorizing incoming emails and notifying relevant Slack channels by integrating Gmail, ChatGPT, and Slack | gmail, slack, chatgpt |
| [Unregister non active users from Copilot](./github_copilot_seats/) | If Copilot was not used in a preceding period by users, the workflow automatically unregisters and notifies them. Users can ask for their subscription to be reinstated. | githubcopilot, slack |
| [Google Calendar To Asana](./google_cal_to_asana/) | Creates Asana tasks based on Google Calendar events | calendar, asana |
| [Ad-hoc room reservation via Slack](./room_reservation/) | Ad-hoc room reservation via Slack slash commands | slack, calendar |
<!-- END-TABLE -->

<img width="451" alt="image" src="https://github.com/user-attachments/assets/f556279f-40a4-4df2-93ef-e1838fcb9861">
