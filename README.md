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
| [Copy Auth0 Users to HubSpot](./auth0_to_hubspot/) | Periodically add new Auth0 users to HubSpot as contacts | auth0, hubspot |
| [AWS Health to Slack](./aws_health_to_slack/) | Monitor AWS health events | aws, slack, sheets |
| [Manage emergency AWS access requests via Slack](./break_glass/) | Submit emergency AWS access requests via Slack, which are then approved or denied based on a set of predefined conditions | aws, slack |
| [Slack notify on categorized email](./categorize_emails/) | Categorizes incoming emails and notifies relevant Slack channels by integrating Gmail, ChatGPT, and Slack | gmail, slack, chatgpt |
| [Slack notify on Confluence page created](./confluence_to_slack/) | When Confluence page is created the user will be notified on Slack | confluence, slack |
| [Parse a file in S3 and insert to database](./data_pipeline/) | Triggered by a new GPX file on an S3 bucket, the pipeline code will parse the GPX file and insert it into a database. | aws, http, sqlite3 |
| [Github Actions](./github_actions/) | GitHub workflows that interact across multiple repositories | github |
| [Cancel GitHub Copilot access for inactive users](./github_copilot_seats/) | If Copilot was not used in a preceding period by users, unsubscribe and notify them in Slack. Users can ask for their subscription to be reinstated. | githubcopilot, slack |
| [Google Calendar To Asana](./google_cal_to_asana/) | Creates Asana tasks based on Google Calendar events | calendar, asana |
| [Create Jira ticket from Google form](./google_forms_to_jira/) | Trigger by HTTP request, continue polling Google forms, and create Jira ticket based on the form's data | forms, http, jira |
| [Hacker News Alerts in Slack ](./hackernews/) | Track Hacker News articles by topic and send updates to Slack | slack |
| [JIRA Assignee From Google Calendar Workflow](./jira_google_calendar/assignee_from_schedule/) | Set Assignee in Jira ticket to the person currently on-call | jira, calendar |
| [Create calendar due date event for Jira ticket](./jira_google_calendar/deadline_to_event/) | When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline | calendar, jira |
| [Pull Request Review Reminder (Purrr)](./purrr/) | Streamline code reviews and cut down turnaround time to merge pull requests | GitHub, Google Sheets, Slack |
| [Quickstart](./quickstart/) | Sample for quickstart | http |
| [Alert on missing Jira events](./reliability/alert_on_missing_events/) | Send Slack alerts when AutoKitteh doesn't receive certain Jira events in time | Jira, Slack |
| [Alert on session errors](./reliability/alert_on_session_errors/) | Send Slack alerts when AutoKitteh sessions end due to errors | Slack |
| [Monitor PR until completion in Slack](./reviewkitteh/) | Create a Slack channel for each PR, update team leads until completion | slack, github, sheets |
| [Ad-hoc room reservation via Slack](./room_reservation/) | Ad-hoc room reservation via Slack slash commands | slack, calendar |
| [Asana](./samples/asana/) | Simple usage of the Asana API | asana |
| [Jira](./samples/atlassian/jira/) | Samples using Jira APIs | jira |
| [GitHub](./samples/github/) | Samples using GitHub APIs | github |
| [Google Calendar](./samples/google/calendar/) | Samples using Google Calendar APIs | calendar |
| [Google Forms](./samples/google/forms/) | Samples using Google Forms APIs | forms |
| [Gemini](./samples/google/gemini/) | Simple usage of the Gemini API | gemini |
| [Gmail](./samples/google/gmail/) | Samples using Gmail APIs | gmail |
| [Google Sheets](./samples/google/sheets/) | Samples using Google Sheets APIs | sheets |
| [HTTP](./samples/http/) | Samples using HTTP requests and webhooks | http |
| [HubSpot](./samples/hubspot/) | Simple usage of the HubSpot API | hubspot |
| [OpenAI ChatGPT](./samples/openai_chatgpt/) | Samples using chatGPT APIs | chatgpt |
| [Runtime Events](./samples/runtime_events/) | Samples using events in AutoKitteh - subscribe(), next_event(), unsubscribe() | autokitteh |
| [Scheduler](./samples/scheduler/) | Samples using cron scheduler for workflows | scheduler |
| [Slack](./samples/slack/) | Samples using Slack APIs | slack |
| [Twilio](./samples/twilio/) | Samples using Twilio APIs | twilio |
| [Slack bot for assistance requests with AI categorization](./slack_support/) | Slack bot request for assistance is inferred using Google's Gemini AI. The appropriate person is mentioned according to a predetermined table of expertise in a Google Doc. The person can then `!take` the request and later `!resolve` it. | slack, googlegemini |
| [Fault tolerant workflow with manual Slack approvals](./task_chain/single_workflow/basic/) | Runs a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure. | slack |
| [Create Jira Ticket from a Webhook data](./webhook_to_jira/) | Create Jira Ticket from a Webhook data | jira, http |
<!-- END-TABLE -->

<img width="451" alt="image" src="https://github.com/user-attachments/assets/f556279f-40a4-4df2-93ef-e1838fcb9861">
