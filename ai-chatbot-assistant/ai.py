import json
import os
from pathlib import Path

import autokitteh
from autokitteh.google import google_sheets_client
from autokitteh.openai import openai_client
from autokitteh.slack import slack_client

from github_poller import find_unanswered_comments
from helpers import append_row_to_sheet
from helpers import format_messages_for_slack
from helpers import get_sheets_data


chatgpt = openai_client("chatgpt_conn")
sheets = google_sheets_client("googlesheets_conn")
slack = slack_client("slack_conn")

SHEET_ID = os.getenv("SHEET_ID")
REPO_NAME = os.getenv("REPO_NAME")
SYSTEM_PROMPT = Path("prompt.txt").read_text()


def on_activate(_):
    while True:
        print("Waiting for a message...")
        subs = [autokitteh.subscribe("slack_conn", "event_type == 'message'")]
        data = autokitteh.next_event(subs)
        if data:
            on_slack_message(data)


def on_slack_message(data):
    user, user_text = data["user"], data["text"]
    response = get_chatgpt_response(user_text)

    match response["action"]:
        case "list":
            list_messages("Sheet1", user)
        case "poll":
            comments = find_unanswered_comments(REPO_NAME, user)
            append_row_to_sheet("Sheet1", comments)
            message = str(comments)
        case _:
            message = response["message"]

    slack.chat_postMessage(channel=user, text=message)


def get_chatgpt_response(user_text):
    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    return json.loads(response.choices[0].message.content)


@autokitteh.activity
def list_messages(sheet_name: str, user: str):
    rows = get_sheets_data(sheet_name)
    if "values" not in rows:
        slack.chat_postMessage(
            channel=user,
            text="No unanswered messages found",
        )
        return

    final_message = format_messages_for_slack(rows)

    slack.chat_postMessage(
        channel=user,
        text=final_message,
        parse="mrkdwn",
    )


# TODO: when sheet is updated, send a message to the user. But how do I
# differentiate between an update event and the initial polling?
def on_new_row(event):
    pass
