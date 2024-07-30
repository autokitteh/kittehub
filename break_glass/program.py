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
    5. The SRE team reviews the request and makes a decision to approve or deny the request.
    6. AutoKitteh sends a message to the developer with the decision, notifying them
       whether the request was approved or denied.

The program integrates with Jira to verify ticket existence and ensure that the requester
is the assignee of the ticket. It also uses Slack for communication and notifications
throughout the process.
"""

from collections import namedtuple
from datetime import datetime
import os
from pathlib import Path
import time

import autokitteh
from autokitteh.aws import boto3_client

from autokitteh.slack import slack_client
from requests.exceptions import HTTPError


APPROVAL_CHANNEL = os.getenv("APPROVAL_CHANNEL")



def on_slack_slash_command(event):
    slack = slack_client("slack_connection")
    """Sends a form to request approval for a ticket."""
    trigger_id = event.data["trigger_id"]
    request_modal = Path("request_modal.json.txt").read_text()

    s = autokitteh.subscribe("slack_connection", 'data.type == "view_submission"')

    slack.views_open(trigger_id=trigger_id, view=request_modal)

    e = autokitteh.next_event(s)
    
    autokitteh.unsubscribe(s)

    reason, issue_key, requester_id = parse_event_data(e) 

    slack.chat_postMessage(channel=requester_id, text=f"Request sent for approval. reason {reason}")


def parse_event_data(event):
    form_data = event["view"]["state"]["values"]
    reason = form_data["block_reason"]["reason"]["value"]
    issue_key = form_data["block_issue_key"]["issue_key"]["value"]
    requester_id = event["user"]["id"]
    return reason, issue_key, requester_id
    

# def on_form_submit(event):
#     reason, issue_key, base_url, requester_id = parse_event_data(event)

#     if not check_issue_exists(issue_key):
#         message = f"Ticket `{issue_key}` does not exist. Please try again."
#         slack.chat_postMessage(channel=requester_id, text=message)
#         return

#     email = slack.users_info(user=requester_id)["user"]["profile"]["email"]
#     if not validate_requester(issue_key, email):
#         issue_link = f"<{base_url}/browse/{issue_key}|{issue_key}>"
#         message = f"You are not the assignee in ticket {issue_link}. Please try again."
#         slack.chat_postMessage(channel=requester_id, text=message)
#         return

#     send_approval_request(reason, issue_key, base_url, requester_id)
#     slack.chat_postMessage(channel=requester_id, text="Request sent for approval.")


# def on_approve_deny(event):
#     """Processes the approval/denial of the request and notifies the requester."""
#     action_id = event.data["actions"][0]["action_id"]
#     _, requester, issue_key = action_id.split(" ")
#     approver_id = event.data["user"]["id"]
#     approver_info = slack.users_info(user=approver_id)

#     if event.data["actions"][0]["value"] != "Approve":
#         message = f"Request denied by: <@{approver_info["user"]["name"]}>"
#         slack.chat_postMessage(channel=requester, text=message)
#         return

#     approver_email = approver_info["user"]["profile"]["email"]
#     jira.issue_add_comment(issue_key, f"Request approved by: {approver_email}")
#     message = f"Request approved by: <@{approver_info['user']['name']}>"
#     slack.chat_postMessage(channel=requester, text=message)

#     # TODO: get user from google sheets
#     aws_user = "break-glass-test-user"
#     set_permissions(aws_user)
#     monitor_and_remove_permissions(aws_user, requester)


# def send_approval_request(reason, issue_key, base_url, requester_id):
#     blocks = Path("approval_message.json.txt").read_text()
#     changes = [
#         ("RequestFromMessage", f"*Request from*: <@{requester_id}>"),
#         ("Ticket", f"*Ticket*: <{base_url}/browse/{issue_key}|{issue_key}>"),
#         ("Reason", "*Reason for request*: " + reason),
#         ("RequesterId", requester_id),
#         ("IssueKey", issue_key),
#     ]
#     for old, new in changes:
#         blocks = blocks.replace(old, new)
#     slack.chat_postMessage(channel=APPROVAL_CHANNEL, blocks=blocks)


# def monitor_and_remove_permissions(aws_user, slack_user):
#     while True:
#         timestamp = get_user_timestamp(aws_user)
#         if not timestamp:
#             return
#         if float(timestamp) < time.time():
#             break
#         time.sleep(10)
#     expire_permissions(aws_user)
#     slack.chat_postMessage(channel=slack_user, text="Your permissions have expired.")




# def validate_requester(issue_key, requester):
#     issue = jira.issue(issue_key)
#     assignee = issue.get("fields", {}).get("assignee", {}).get("emailAddress", "")
#     return assignee == requester


# @autokitteh.activity
# def check_issue_exists(issue_key):
#     try:
#         jira.issue(issue_key)
#         return True
#     # TODO: issue exists or a more specific error code 404 etc
#     except HTTPError as e:
#         print(f"Error retrieving issue: {e}")
#         return False


# @autokitteh.activity
# def set_permissions(user_name):
#     aws.add_user_to_group(GroupName="break-glass-admin", UserName=user_name)
#     redis.set(user_name, time.time() + os.getenv("PERMISSION_EXPIRY"))


# @autokitteh.activity
# def expire_permissions(user_name):
#     aws.remove_user_from_group(GroupName="break-glass-admin", UserName=user_name)
#     redis.delete(user_name)


# @autokitteh.activity
# def get_user_timestamp(user_name):
#     return redis.get(user_name)
