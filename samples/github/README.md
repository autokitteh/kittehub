# GitHub

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?name=samples/github)

There are various AutoKitteh projects in the Kittehub repository that demonstrate different aspects of integration with [GitHub](https://github.com).

## General Documentation

- [AutoKitteh](https://docs.autokitteh.com/integrations/github)
- [GitHub webhook events and payloads](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
- [PyGithub](https://pygithub.readthedocs.io/en/stable/)

## GitHub Workflows

Project: [GitHub workflows](/devops/github_workflows/)

- Orchestrate GitHub workflows using advanced scenarios across multiple repositories
- Receive [`workflow_run`](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run) webhook events
- Send [`create_dispatch`](https://pygithub.readthedocs.io/en/stable/github_objects/Workflow.html) API calls

## Pull Requests

Project: [ReviewKitteh](/devops/reviewkitteh/)

- Monitor a GitHub PR in Slack until it's closed
- Receive [`pull_request`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request) webhook events (`"opened"` and `"reopened"` actions, `"closed"` and `"merged"` states)

Project: [Pull Request Review Reminder (Purrr)](/devops/purrr/)

- Streamline code reviews and cut down turnaround time to merge pull requests
- Manage the entire lifecycle of a PR review process by receiving and parsing these webhook events:
  - [`pull_request`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request)
  - [`pull_request_review`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review)
  - [`pull_request_review_comment`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review_comment)
  - [`pull_request_review_thread`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#pull_request_review_thread)
  - [`issue_comment`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#issue_comment)
- Send various PyGithub API calls
- Parse [GitHub markdown](/devops/purrr/text_utils.py) text

## GitHub Marketplace Webhooks

Project: [GitHub Marketplace to Slack](/github_marketplace_to_slack/)

- Forward GitHub Marketplace notifications to Slack
- Instructions for configuring GitHub Marketplace webhooks for GitHub apps
- Receive [`marketplace_purchase`](https://docs.github.com/en/webhooks/webhook-events-and-payloads#marketplace_purchase) notifications
- Verify the signature authenticity of incoming notifications
