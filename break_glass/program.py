import os
from pathlib import Path

import autokitteh
from autokitteh.atlassian import atlassian_jira_client
from autokitteh.slack import slack_client


APPROVER = "michael"
jira = atlassian_jira_client("jira_connection")
slack = slack_client("slack_connection")


def on_slack_slash_command(event):
    """Sends a form to request approval for a ticket."""
    trigger_id = event.data["trigger_id"]
    request_modal = Path("request_modal.json.txt").read_text()
    slack.views_open(trigger_id=trigger_id, view=request_modal)


@autokitteh.activity
def on_form_submit(event):
    form_data = event.data["view"]["state"]["values"]
    reason = form_data["block_reason"]["reason"]["value"]
    issue_key = form_data["block_issue_key"]["issue_key"]["value"]
    base_url = os.getenv("jira_connection__AccessURL")
    # TODO: get the requester's name by doing a slack lookup
    requester_id = event.data["user"]["id"]
    requester_name = slack.users_info(user=requester_id)["user"]["name"]
    print(requester_name)

    if not check_issue_exists(issue_key):
        message = f"Ticket {issue_key} does not exist. Please try again."
        slack.chat_postMessage(channel=requester_id, text=message)
        return

    email = slack.users_info(user=requester_id)["user"]["profile"]["email"]
    if not validate_requester(issue_key, email):
        message = f"You are not the assignee for ticket {issue_key}. Please try again."
        slack.chat_postMessage(channel=requester_id, text=message)
        return

    blocks = Path("approval_message.json.txt").read_text()
    changes = [
        ("Title", "Approval request from " + f"<@{requester_name}>"),
        ("Ticket", f"*Ticket*: <{base_url}/browse/{issue_key}|{issue_key}>"),
        ("Message", "*Reason for request*: " + reason),
        ("ActionID", requester_id),
    ]
    for old, new in changes:
        blocks = blocks.replace(old, new)
    slack.chat_postMessage(channel=APPROVER, blocks=blocks)


@autokitteh.activity
def on_approve_deny(event):
    # print(event.data)
    action_id = event.data["actions"][0]["action_id"]
    params = action_id.split(" ")
    approver = event.data["user"]["id"]
    # TODO: get the approver's name/slack tag? by doing a slack lookup

    if event.data["actions"][0]["value"] == "Approve":
        # TODO: can't combine the two lines below because of node error
        requester = params[1]
        # TODO: Add a message to the ticket. Request to break glass was approved by:
        issue_key = params[2]
        print(f"Issue key: {issue_key}")
        # jira.issue_add_comment(issue_key, f"Request approved by: {approver}")
    else:
        requester = action_id.split(" ")[1]
        slack.chat_postMessage(channel=requester, text=f"Request denied by: {approver}")


def check_issue_exists(issue_key):
    try:
        jira.issue(issue_key)
        return True
    # TODO: Add a more specific exception?
    except Exception as e:
        print(f"Error retrieving issue: {e}")
        return False


def validate_requester(issue_key, requester):
    issue = jira.issue(issue_key)
    assignee = issue["fields"]["assignee"]
    if not assignee:
        # TODO: Potentially different error case? This is when the assignee is not set.
        return False
    assignee = issue["fields"]["assignee"]["emailAddress"]
    return assignee == requester
