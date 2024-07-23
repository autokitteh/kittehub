import os
from pathlib import Path

from autokitteh.slack import slack_client
import slack_sdk

APPROVER = "michael"


def on_slack_slash_command(event):
    # send user an interactive slack form
    # print(event.data["trigger_id"])
    trigger_id = event.data["trigger_id"]
    request_modal = Path("request_modal.json.txt").read_text()
    slack = slack_client("slack_connection")
    # TODO: remove this try catch block
    try:
        response = slack.views_open(trigger_id=trigger_id, view=request_modal)
    except SlackApiError as e:
        print(f"Error opening modal: {e.response['error']}")
    # blocks = Path("request_form.json.txt").read_text()
    # slack.chat_postMessage(channel=event.data["user_id"], blocks=blocks)
    # print(response)


# TODO: currently this function is only for modal response handling. potentially add filtering later on
def on_form_submit(event):
    print(event.data)
    form_data = event.data["view"]["state"]["values"]
    reason = form_data["block_reason"]["reason"]["value"]
    ticket_id = form_data["block_ticket_id"]["ticket_id"]["value"]
    print(reason)
    print(ticket_id)
    # TODO: send message to approver with link to ticket and the reason for the message
    blocks = Path("approval_message.json.txt").read_text()
    changes = [
        ("Title", "Approval request from " + event.data["user"]["id"]),
        ("Ticket", f"*Ticket*: <{os.getenv("BASE_URL") + ticket_id}|{ticket_id}>"),
        ("Message", "*Reason for request*: " + reason),
        # ("ActionID", event.data.user_id),
    ]
    for old, new in changes:
        blocks = blocks.replace(old, new)

    slack = slack_client("slack_connection")
    slack.chat_postMessage(channel=APPROVER, blocks=blocks)
    # print(form_data)

    # user_selection = event.data["actions"][0]["value"]
    # slack = slack_client("slack_connection")

    # if user_selection == "Approve":
    #     slack.chat_postMessage(channel=event.data["user"]["id"], text="Approved!")
    # else:
    #     # log the rejection
    #     slack.chat_postMessage(channel=event.data["user"]["id"], text="Rejected!")
