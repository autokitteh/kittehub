# Kittehub

This is a central repository of [AutoKitteh](https://github.com/autokitteh/autokitteh)
projects for:

- Full-fledged, ready-to-use solutions for real-life use cases
- Composable templates for interoperability between common services
- Demonstrations of system capabilities and features

| Name                                                          | Description                                                                     | Integrations                      |
| :------------------------------------------------------------ | :------------------------------------------------------------------------------ | :-------------------------------- |
| [AWS Health to Slack](./aws_health_to_slack/)                 |                                                                                 | AWS (Health) &rarr; Slack         |
| [Break-Glass](./break_glass/)                                 |                                                                                 | Slack &rarr; AWS (IAM), Jira      |
| [Categorize Emails](./categorize_emails/)                     |                                                                                 | Gmail &rarr; ChatGPT &rarr; Slack |
| [Confluence to Slack](./confluence_to_slack/)                 |                                                                                 | Confluence &rarr; Slack           |
| [Create Jira Issue](./create_jira_issue/)                     |                                                                                 | HTTP &rarr; Jira                  |
| [Data Pipeline](./data_pipeline/)                             |                                                                                 | AWS (SNS, S3) &rarr; SQLite       |
| [GitHub Copilot Seats](./github_copilot/)                     | ... (implemented in Starlark)                                                   | GitHub &harr; Slack               |
| [Google Forms to Jira](./google_forms_to_jira/)               |                                                                                 | Google Forms &rarr; Jira          |
| [Jira Assignee From Calendar](./jira_assignee_from_calendar/) |                                                                                 | Jira &harr; Google Calendar       |
| [Jira to Google Calendar](./jira_to_google_calendar/)         |                                                                                 | Jira &rarr; Google Calendar        |
| [Pull Request Review Reminder (Purrr)](./purrr/)              | Streamline code reviews and cut down the turnaround time to merge pull requests | GitHub &harr; Slack               |
| [ReviewKitteh](./reviewkitteh/)                               | Monitor pull requests, and meow at random people                                | GitHub, Google Sheets, Slack      |
| [Task Chain](./task_chain/)                                   | Run a sequence of tasks with fault tolerance                                    | Slack                             |
