"""This program orchestrates the request and approval process for break glass scenarios.

Break glass scenarios occur when a developer needs to access sensitive data or perform
a critical operation that requires elevated permissions beyond their usual access.

Workflow:
    1. A developer initiates the process by using a Slack slash command to request
       break glass approval.
    2. AutoKitteh sends a form to the developer, requesting details about the reason
       for the elevated access.
    3. The developer fills out and submits the form, providing the necessary information
       and justification for the request.
    4. AutoKitteh sends a notification to the SRE (Site Reliability Engineering) team
       with an approve/deny message, including the details of the request.
    5. The SRE team reviews the request and makes a decision to approve or deny the
       request.
    6. AutoKitteh sends a message to the developer with the decision, notifying them
       whether the request was approved or denied.

The program integrates with Jira to verify ticket existence and ensure the requester
is the assignee of the ticket. It also uses Slack for communication and notifications
throughout the process.
"""

import os
from pathlib import Path

import autokitteh
from autokitteh.atlassian import get_base_url, jira_client
from autokitteh.slack import slack_client
from requests.exceptions import HTTPError


APPROVAL_CHANNEL = os.getenv("APPROVAL_CHANNEL")
jira = jira_client("jira_connection")
slack = slack_client("slack_connection")


def on_slack_slash_command(event):
    """Sends a form to request approval for a ticket."""
    trigger_id = event.data["trigger_id"]
    request_modal = Path("request_modal.json.txt").read_text()
    slack.views_open(trigger_id=trigger_id, view=request_modal)


@autokitteh.activity
def on_form_submit(event):
    reason, issue_key, base_url, requester_id = parse_event_data(event)

    if not check_issue_exists(issue_key):
        message = f"Ticket `{issue_key}` does not exist. Please try again."
        slack.chat_postMessage(channel=requester_id, text=message)
        return

    email = slack.users_info(user=requester_id)["user"]["profile"]["email"]
    if not validate_requester(issue_key, email):
        issue_link = f"<{base_url}/browse/{issue_key}|{issue_key}>"
        message = f"You are not the assignee in ticket {issue_link}. Please try again."
        slack.chat_postMessage(channel=requester_id, text=message)
        return

    send_approval_request(reason, issue_key, base_url, requester_id)
    slack.chat_postMessage(channel=requester_id, text="Request sent for approval.")


@autokitteh.activity
def on_approve_deny(event):
    action_id = event.data["actions"][0]["action_id"]
    _, requester, issue_key = action_id.split(" ")
    approver_id = event.data["user"]["id"]
    approver_info = slack.users_info(user=approver_id)

    if event.data["actions"][0]["value"] == "Approve":
        approver_email = approver_info["user"]["profile"]["email"]
        jira.issue_add_comment(issue_key, f"Request approved by: {approver_email}")
        message = f"Request approved by: <@{approver_info['user']['name']}>"
        slack.chat_postMessage(channel=requester, text=message)
    else:
        print(f"Requester: {requester}")
        message = f"Request denied by: <@{approver_info['user']['name']}>"
        slack.chat_postMessage(channel=requester, text=message)


def send_approval_request(reason, issue_key, base_url, requester_id):
    blocks = Path("approval_message.json.txt").read_text()
    changes = [
        ("RequestFromMessage", f"*Request from*: <@{requester_id}>"),
        ("Ticket", f"*Ticket*: <{base_url}/browse/{issue_key}|{issue_key}>"),
        ("Reason", "*Reason for request*: " + reason),
        ("RequesterId", requester_id),
        ("IssueKey", issue_key),
    ]
    for old, new in changes:
        blocks = blocks.replace(old, new)
    slack.chat_postMessage(channel=APPROVAL_CHANNEL, blocks=blocks)


def parse_event_data(event):
    form_data = event.data["view"]["state"]["values"]
    reason = form_data["block_reason"]["reason"]["value"]
    issue_key = form_data["block_issue_key"]["issue_key"]["value"]
    base_url = get_base_url("jira_connection")
    requester_id = event.data["user"]["id"]
    return reason, issue_key, base_url, requester_id


def check_issue_exists(issue_key):
    try:
        jira.issue(issue_key)
        return True
    except HTTPError as e:
        print(f"Error retrieving issue: {e}")
        return False


def validate_requester(issue_key, requester):
    issue = jira.issue(issue_key)
    assignee = issue.get("fields", {}).get("assignee") or {}
    assignee = assignee.get("emailAddress")
    return assignee == requester
