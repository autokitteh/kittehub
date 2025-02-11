import json
import os
from pathlib import Path

import autokitteh
from autokitteh.openai import openai_client
from autokitteh.slack import slack_client
from helpers import append_row_to_sheet
from helpers import format_messages_for_slack
from helpers import get_sheets_data
from repo_scanner import find_unanswered_comments


chatgpt = openai_client("chatgpt_conn")
slack = slack_client("slack_conn")

REPO_NAME = os.getenv("REPO_NAME")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SYSTEM_PROMPT = Path("prompt.txt").read_text()


def on_activate(_):
    """Entrypoint for the AI chatbot assistant."""
    while True:
        print("Waiting for a message...")
        subs = [autokitteh.subscribe("slack_conn", "event_type == 'message'")]
        data = autokitteh.next_event(subs)
        if data:
            on_slack_message(data)


def on_slack_message(data):
    """Handle a message from Slack. This function determines the action to take.

    Args:
        data: The data from the Slack event.
    """
    user, user_text = data["user"], data["text"]
    response = get_chatgpt_response(user_text)

    # Always send initial response
    slack.chat_postMessage(channel=user, text=response["message"])

    match response["action"]:
        case "list":
            rows = get_sheets_data(SHEET_NAME)
            message = format_messages_for_slack(rows)
            slack.chat_postMessage(channel=user, text=message)
        case "scan":
            comments = find_unanswered_comments(REPO_NAME, user)
            append_row_to_sheet(SHEET_NAME, comments)
            rows = get_sheets_data(SHEET_NAME)
            message = format_messages_for_slack(rows)
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
