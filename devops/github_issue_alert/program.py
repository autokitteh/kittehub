"""Monitors GitHub issue creation and comment activity."""

import os

from autokitteh.slack import slack_client


SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_NAME_OR_ID", "")

slack = slack_client("slack_conn")


def on_issue_comment(event):
    """Processes a GitHub issue comment event and sends a message to Slack.

    Supported actions: created, edited, deleted

    For more details on the payload structure, visit:
    https://docs.github.com/en/webhooks/webhook-events-and-payloads#issue_comment
    """
    comment_url = event.data.comment.html_url
    comment_body = event.data.comment.body
    comment_action = event.data.action
    comment_author = event.data.comment.user.login or "Unknown user"
    issue_title = event.data.issue.title

    text = (
        f"{comment_author} {comment_action} a comment on issue '{issue_title}': "
        f"{comment_body}\n. "
    )
    text += f"View the comment here: {comment_url}."

    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)


def on_issue_event(event):
    """Processes a GitHub issue event and sends a message to Slack.

    Supported actions: opened, reopened, closed

    For more details on the payload structure, visit:
    https://docs.github.com/en/webhooks/webhook-events-and-payloads#issues
    """
    issue_title = event.data.issue.title
    issue_author = event.data.issue.user.login
    issue_action = event.data.action
    issue_url = event.data.issue.html_url

    text = f"{issue_author} {issue_action} an issue: '{issue_title}', "
    text += f"View the issue here: {issue_url}."

    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)
