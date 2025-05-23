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
| [AI chat assistant](./ai-chat-assistant/) | A Slack-based automation assistant that leverages ChatGPT to manage and respond to messages by integrating with GitHub and Google Sheets. | chatgpt, github, sheets, slack |
| [LangGraph Bot with Tavily, and Google Sheets](./ai_agents/langgraph_bot/) | Slack bot built with LangGraph and powered by Gemini LLM that can search information and update Google Sheets | slack, sheets |
| [OpenAI Agent Researcher](./ai_agents/openai_agent_researcher/) | A Slack-based research agent workflow. | chatgpt, slack |
| [Anthropic Slack Thread TLDR](./anthropic_slack_thread_tldr/) | Summarizes a Slack thread using Claude | slack |
| [Copy Auth0 Users to HubSpot](./auth0_to_hubspot/) | Periodically add new Auth0 users to HubSpot as contacts | auth0, hubspot |
| [Manage emergency AWS access requests via Slack](./break_glass/) | Submit emergency AWS access requests via Slack, which are then approved or denied based on a set of predefined conditions | aws, slack |
| [Email categorization and notification](./categorize_emails/) | Categorize incoming emails and notify relevant Slack channels | gmail, chatgpt, slack |
| [Slack notify on Confluence page created](./confluence_to_slack/) | When Confluence page is created the user will be notified on Slack | confluence, slack |
| [ETL Pipeline From S3 to SQLite](./data_pipeline/) | Processes GPX files from S3 and inserts them into a SQLite database, creating a data pipeline from cloud to structured data | aws, http, sqlite3 |
| [GitHub issue alert](./devops/github_issue_alert/) | Send GitHub issue comments to Slack | github, slack |
| [GitHub workflow orchestration](./devops/github_workflows/) | Orchestrate GitHub workflows using advanced scenarios across multiple repositories | github |
| [Pull Request Review Reminder (Purrr)](./devops/purrr/) | Streamline code reviews and cut down turnaround time to merge pull requests | github, sheets, slack |
| [ReviewKitteh](./devops/reviewkitteh/) | Monitor a GitHub PR in Slack until it's closed | github, sheets, slack |
| [SFTP demo](./devops/sftp/) | Trigger a file transfer from SFTP to HTTP on webhook call | http |
| [Cancel GitHub Copilot access for inactive users](./github_copilot_seats/) | If Copilot was not used in a preceding period by users, unsubscribe and notify them in Slack. Users can ask for their subscription to be reinstated. | githubcopilot, slack |
| [GitHub Marketplace to Slack](./github_marketplace_to_slack/) | Forward GitHub Marketplace notifications to Slack | github, http, slack |
| [Google Calendar To Asana](./google_cal_to_asana/) | Creates Asana tasks based on Google Calendar events | calendar, asana |
| [Create Jira ticket from Google form](./google_forms_to_jira/) | Create and update Jira tickets automatically from Google Forms responses | forms, jira |
| [Hacker News alerts in Slack](./hackernews/) | Track Hacker News articles by topic and send updates to Slack | slack |
| [Invoice processing system](./invoice_processing/) | Process emails for invoices, extract data, and generate reports | gmail, chatgpt |
| [GitHub and Jenkins workflow](./jenkins_release/) | This ensures that when a commit is pushed to main, a specific Jenkins build is completed. | github |
| [Jira assignee from Google Calendar](./jira_google_calendar/assignee_from_schedule/) | Set assignee in Jira ticket to the person currently on-call | jira, calendar |
| [Create calendar due date event for Jira ticket](./jira_google_calendar/deadline_to_event/) | When a new Jira issue is created, the workflow automatically generates a Google Calendar event with a deadline | calendar, jira |
| [Quickstart](./quickstart/) | Sample for quickstart | http |
| [AWS Health monitor](./reliability/aws_health_monitor/) | Announce AWS Health events in Slack channels, based on resource ownership data in a Google Sheet | aws, slack, sheets |
| [Incident management automation](./reliability/incidenter/) | Connect separate systems to have seamless incident management | slack, zoom, height |
| [Missing Jira events monitor](./reliability/missing_jira_events_monitor/) | Send Slack alerts when AutoKitteh doesn't receive certain Jira events in time | jira, slack |
| [AutoKitteh session errors monitor](./reliability/session_errors_monitor/) | Send Slack alerts when AutoKitteh sessions end due to errors | autokitteh, slack |
| [Ad-hoc room reservation via Slack](./room_reservation/) | Ad-hoc room reservation via Slack slash commands | slack, calendar |
| [Asana sample](./samples/asana/) | Simple usage of the Asana API | asana |
| [Jira sample](./samples/atlassian/jira/) | Samples using Jira APIs | jira |
| [Auth0 sample](./samples/auth0/) | Simple usage of the Auth0 API | auth0 |
| [Google Calendar sample](./samples/google/calendar/) | Samples using Google Calendar APIs | calendar |
| [Google Drive sample](./samples/google/drive/) | Samples using Google Drive APIs | drive |
| [Google Forms sample](./samples/google/forms/) | Samples using Google Forms APIs | forms |
| [Gemini sample](./samples/google/gemini/) | Simple usage of the Gemini API | googlegemini |
| [Gmail sample](./samples/google/gmail/) | Samples using Gmail APIs | gmail |
| [Google Sheets sample](./samples/google/sheets/) | Samples using Google Sheets APIs | sheets |
| [HTTP sample](./samples/http/) | Samples using HTTP requests and webhooks | http |
| [HubSpot sample](./samples/hubspot/) | Simple usage of the HubSpot API | hubspot |
| [OpenAI ChatGPT sample](./samples/openai_chatgpt/) | Samples using chatGPT APIs | chatgpt |
| [Runtime Events sample](./samples/runtime_events/) | Samples using events in AutoKitteh - subscribe(), next_event(), unsubscribe() | autokitteh |
| [Scheduler sample](./samples/scheduler/) | Samples using cron scheduler for workflows | scheduler |
| [Slack sample](./samples/slack/) | Samples using Slack APIs | slack |
| [Twilio sample](./samples/twilio/) | Samples using Twilio APIs | twilio |
| [AI-driven Slack bot for assistance requests](./slack_support/) | Automatically route help requests to the right expert based on topic analysis and expertise matching | slack, sheets, googlegemini |
| [Fault tolerant workflow with manual Slack approvals](./task_chain/single_workflow/basic/) | Runs a sequence of tasks with fault tolerance. In case of failure, user can decide to terminate or retry from the point of failure. | slack |
| [Create Jira ticket from webhook data](./webhook_to_jira/) | Create Jira issues automatically from HTTP webhooks | jira, http |
<!-- END-TABLE -->

<img width="451" alt="image" src="https://github.com/user-attachments/assets/f556279f-40a4-4df2-93ef-e1838fcb9861">
