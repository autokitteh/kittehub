"""This program listens for new Jira issues and creates a Slack channel for each issue.
It then invites the issue creator to the channel and waits for the user to confirm completion by mentioning the Slack app with @app 'done'.
Once confirmed, it archives the channel, notifies the channel members, and updates the Jira issue status to 'DONE'.
"""

import re

import autokitteh
from autokitteh.atlassian import jira_client
from autokitteh.slack import slack_client


slack = slack_client("slack_conn")
jira = jira_client("jira_conn")


def on_jira_issue_created(event):
    """Entry point for workflow"""
    issue_key = event.data.issue.key
    channel_id = create_slack_channel(event.data.issue, issue_key)

    # Invite the issue creator to the channel
    creator_id = event.data.issue.fields.creator.accountId
    user_id = fetch_slack_user_id_by_jira_account(creator_id)
    slack.conversations_invite(channel=channel_id, users=[user_id])

    wait_for_user_confirmation(channel_id)

    # Archive the channel and notify the channel members
    notify_channel_members(issue_key, channel_id)
    slack.conversations_archive(channel=channel_id)
    print(f"Channel {channel_id} archived successfully.")

    jira.set_issue_status(issue_key, "DONE")


def wait_for_user_confirmation(channel_id):
    """Wait for the user to confirm completion by typing 'done' in the Slack channel."""
    event_filter = "event_type == 'app_mention'"
    sub = autokitteh.subscribe("slack_conn", event_filter)
    while True:
        mention = autokitteh.next_event(sub)
        if mention.channel != channel_id:
            continue
        if "done" in mention.text.lower():
            break
    autokitteh.unsubscribe(sub)


def notify_channel_members(issue_key, channel_id):
    result = slack.conversations_members(channel=channel_id)
    members = result["members"]
    for member_id in members:
        msg = f"Hey <@{member_id}>, the Jira ticket {issue_key} is closed. The channel will be archived shortly."
        slack.chat_postMessage(channel=member_id, text=msg)


def create_slack_channel(issue, issue_key):
    """Create a Slack channel for the given Jira issue."""
    channel_name = f"issue-key-{issue_key}_{issue.fields.summary}"
    channel_name = sanitize_channel_name(channel_name)
    response = slack.conversations_create(name=channel_name, is_private=False)
    channel_id = response["channel"]["id"]
    print(f"Channel created successfully with ID: {channel_id}")
    return channel_id


def fetch_slack_user_id_by_jira_account(account_id):
    """Fetch the Slack user ID associated with a given Jira account ID."""
    jira_user = jira.user(account_id=account_id)
    email = jira_user.get("emailAddress")
    response = slack.users_lookupByEmail(email=email)
    user_id = response["user"]["id"]
    return user_id


def sanitize_channel_name(name):
    """Sanitize the channel name to be Slack-compatible."""
    sanitized_name = re.sub(r"[^a-z0-9_\-]", "-", name.lower())
    return sanitized_name
