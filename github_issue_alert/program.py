"""Monitors GitHub issue creation and comment activity.

Sending the notifications to Slack to keep teams updated.
"""

import os

from autokitteh.slack import slack_client


SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "")

slack = slack_client("slack_conn")


def on_issue_comment(event):
    comment_body = event["data"]["comment"]["body"]
    comment_action = event["data"]["action"]
    comment_author = event["data"]["comment"]["user"]["login"] or "Unknown user"
    issue_title = event["data"]["issue"]["title"]

    text = (
        f"{comment_author} {comment_action} a comment: '{comment_body}' "
        f"on issue '{issue_title}'"
    )
    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)


def on_issue_created(event):
    issue_title = event["data"]["issue"]["title"]
    issue_author = event["data"]["issue"]["user"]["login"]
    issue_body = event["data"]["issue"]["body"] or "No description provided"

    text = (
        f"{issue_author} created an issue: '{issue_title}' "
        f"with description: '{issue_body}'"
    )
    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)
