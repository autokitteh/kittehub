from collections import namedtuple
from datetime import datetime
import os
from pathlib import Path
import time

import autokitteh
from autokitteh.aws import boto3_client
from autokitteh.slack import slack_client
from requests.exceptions import HTTPError

APPROVAL_CHANNEL = "C06C0EJEVB5"
AWS_ADMIN_GROUP = os.getenv("AWS_ADMIN_GROUP")
PERMISTIONS_DURATION = 20

slack = slack_client("slack_connection")
aws = boto3_client("aws_connection", "iam")


def on_slack_slash_command(event):
    
    """Sends a form to request approval for a ticket."""
    trigger_id = event.data["trigger_id"]
    request_modal = Path("request_modal.json.txt").read_text()

    #TODO: filter the event to make sure it is the right one
    s = autokitteh.subscribe("slack_connection", 'data.type == "view_submission"')

    slack.views_open(trigger_id=trigger_id, view=request_modal)

    e = autokitteh.next_event(s)
    autokitteh.unsubscribe(s)
    
    print(e)
    
    reason, issue_key, requester_id = parse_event_data(e) 
    blocks = Path("approval_message.json.txt").read_text()

    #TODO: filter the event to make sure it is the right one
    s = autokitteh.subscribe("slack_connection", 'type == "interaction"')

    slack.chat_postMessage(channel=APPROVAL_CHANNEL, blocks=blocks)
    slack.chat_postMessage(channel=requester_id, text=f"Request sent for approval. reason {reason}")

    event = autokitteh.next_event(s)
    autokitteh.unsubscribe(s)

    print(event)
    
    action_id = event["actions"][0]["action_id"]
    #_, requester, issue_key = action_id.split(" ")
    approver_id = event["user"]["id"]
    approver_info = slack.users_info(user=approver_id)

    if event["actions"][0]["value"] != "Approve":
        message = f"Request denied by: <@{approver_info["user"]["name"]}>"
        slack.chat_postMessage(channel=requester_id, text=message)
        return

    message = f"Request approved by: <@{approver_info['user']['name']}>"
    slack.chat_postMessage(channel=requester_id, text=message)

    # TODO: get user from google sheets
    aws_user = "break-glass-test-user"
    set_permissions(aws_user)
    time.sleep(PERMISTIONS_DURATION)

    expire_permissions(aws_user)
    slack.chat_postMessage(channel=requester_id, text="Your permissions have expired.")
    #monitor_and_remove_permissions(aws_user, requester_id)


def parse_event_data(event):
    form_data = event["view"]["state"]["values"]
    reason = form_data["block_reason"]["reason"]["value"]
    issue_key = form_data["block_issue_key"]["issue_key"]["value"]
    requester_id = event["user"]["id"]
    return reason, issue_key, requester_id
    
@autokitteh.activity
def set_permissions(user_name):
    aws.add_user_to_group(GroupName="break-glass-admin", UserName=user_name)


@autokitteh.activity
def expire_permissions(user_name):
    aws.remove_user_from_group(GroupName="break-glass-admin", UserName=user_name)
