# Kittehub

This is a central repository of [AutoKitteh](https://github.com/autokitteh/autokitteh)
projects for:

- Full-fledged, ready-to-use solutions for real-life use cases
- Composable templates for interoperability between common services
- Demonstrations of advanced system capabilities and features

In addition, the [samples](./samples/) directory contains projects that
demonstrate basic system features, integration APIs, and best practices.

| Name                                                                             | Description                                                                              | Integrations                                |
| :------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- | :------------------------------------------ |
| 🐍 [AWS Health to Slack](./aws_health_to_slack/)                                 | Announce cloud health events based on a resource ownership mapping                       | AWS (Health), Google Sheets, Slack          |
| 🐍 [Break-glass](./break_glass/)                                                 | Manage break-glass requests and approvals for temporary elevated permissions             | Slack &rarr; AWS (IAM), Jira                |
| 🐍 [Categorize emails](./categorize_emails/)                                     | Categorize new emails and notify the appropriate channels based on the content           | Gmail &rarr; ChatGPT &rarr; Slack           |
| 🐍 [Confluence to Slack](./confluence_to_slack/)                                 | Notify when a new page with a specific label is created                                  | Confluence &rarr; Slack                     |
| 🐍 [Data pipeline](./data_pipeline/)                                             | Process and store data from new S3 files in a database                                   | AWS (SNS, S3) &rarr; SQLite                 |
| 🐍 [Discord to Spreadsheet](./discord_to_spreadsheet/)                           | Log Discord message events using AutoKitteh's event system for simple event handling     | Discord &rarr; Google Sheets                |
| ⭐ [GitHub Copilot seats](./github_copilot/)                                     | Automate daily GitHub Copilot user pruning and report changes                            | GitHub &harr; Slack                         |
| 🐍 [Google Calendar to Asana](./google_cal_to_asana/)                            | Create an Asana task whenever a new event is added to Google Calendar                    | Google Calendar &rarr; Asana                |
| 🐍 [Google Forms to Jira](./google_forms_to_jira/)                               | Create Jira issues based on Google Forms responses                                       | Google Forms &rarr; Jira                    |
| 🐍 [Jira assignee from schedule](./jira_google_calendar/assignee_from_schedule/) | Assign new Jira issues to the current on-caller based on a schedule in a shared calendar | Jira &harr; Google Calendar                 |
| 🐍 [Jira deadline to event](./jira_google_calendar/deadline_to_event/)           | Create/update calendar events based on the deadlines of Jira issues                      | Jira &harr; Google Calendar                 |
| ⭐ [Pull Request Review Reminder (Purrr)](./purrr/)                              | Streamline code reviews and cut down turnaround time to merge pull requests              | GitHub &harr; Slack                         |
| 🐍 [Quickstart](./quickstart/)                                                   | Basic workflow for tutorials                                                             | HTTP                                        |
| ⭐ [ReviewKitteh](./reviewkitteh/)                                               | Monitor pull requests, and meow at random people                                         | GitHub, Google Sheets, Slack                |
| 🐍 [Room reservation](./room_reservation/)                                       | Manage via Slack ad-hoc room reservations in Google Calendar                             | Slack &harr; Google Calendar, Google Sheets |
| 🐍 [Slack Discord sync](./slack_discord_sync)                                    | Sync Slack and Discord messages in real-time                                             | Slack &harr; Discord                        |
| 🐍 [Slack support](./slack_support/)                                             | Categorize Slack support requests using AI, and route them to the appropiate people      | Slack &harr; Gemini, Google Sheets          |
| 🐍 [Task chain](./task_chain/)                                                   | Run a sequence of tasks with fault tolerance                                             | Slack                                       |
| 🐍 [Webhook to Jira](./webhook_to_jira/)                                         | Create Jira issues based on HTTP GET/POST requests                                       | HTTP &rarr; Jira                            |

> [!NOTE]
> 🐍 = Python implementation, ⭐ = Starlark implementation.


<img width="451" alt="image" src="https://github.com/user-attachments/assets/f556279f-40a4-4df2-93ef-e1838fcb9861">
