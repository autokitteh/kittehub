# Kittehub

This is a central repository of [AutoKitteh](https://github.com/autokitteh/autokitteh)
projects for:

- Full-fledged, ready-to-use solutions for real-life use cases
- Composable templates for interoperability between common services
- Demonstrations of system capabilities and features

| Name                                                          | Description                                                                     | Integrations                      |
| :------------------------------------------------------------ | :------------------------------------------------------------------------------ | :-------------------------------- |
| 🐍 [AWS Health to Slack](./aws_health_to_slack/)                 | Notify about AWS Health events based on resource ownership mapping              | AWS (Health) &rarr; Slack         |
| 🐍 [Break-Glass](./break_glass/)                                 | Orchestrate break glass requests and approvals for elevated permissions         | Slack &rarr; AWS (IAM), Jira      |
| 🐍 [Categorize Emails](./categorize_emails/)                     | Categorize new emails and notify the appropriate channels based on the content  | Gmail &rarr; ChatGPT &rarr; Slack |
| 🐍 [Confluence to Slack](./confluence_to_slack/)                 | Notify when a new page with a specific label is created                         | Confluence &rarr; Slack           |
| 🐍 [Create Jira Issue](./create_jira_issue/)                     | Create Jira issues from webhook requests                                        | HTTP &rarr; Jira                  |
| 🐍 [Data Pipeline](./data_pipeline/)                             | Process new S3 files: parse and store data in a database pipeline               | AWS (SNS, S3) &rarr; SQLite       |
| ⭐ [GitHub Copilot Seats](./github_copilot/)                     | Automate daily GitHub Copilot user pruning and notify users of changes          | GitHub &harr; Slack               |
| 🐍 [Google Forms to Jira](./google_forms_to_jira/)               | Poll a form for responses and create an issue for each new entry                | Google Forms &rarr; Jira          |
| 🐍 [Jira Assignee From Calendar](./jira_assignee_from_calendar/) | Assign Jira issues based on the current on-call person from a shared calendar   | Jira &harr; Google Calendar       |
| 🐍 [Jira to Google Calendar](./jira_to_google_calendar/)         | Create calendar events from Jira issues to schedule and track reviews           | Jira &rarr; Google Calendar       |
| ⭐ [Pull Request Review Reminder (Purrr)](./purrr/)              | Streamline code reviews and cut down the turnaround time to merge pull requests | GitHub &harr; Slack               |
| ⭐ [ReviewKitteh](./reviewkitteh/)                               | Monitor pull requests, and meow at random people                                | GitHub, Google Sheets, Slack      |
| 🐍 [Task Chain](./task_chain/)                                   | Run a sequence of tasks with fault tolerance                                    | Slack                             |

> [!NOTE]
> **Legend**: ⭐ Starlark implementation, 🐍 Python implementation
