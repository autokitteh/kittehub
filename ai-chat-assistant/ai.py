"""This module provides the main functionality for the AI chatbot assistant.

It integrates with Slack and uses OpenAI's GPT model to generate responses based
on user messages. It also interacts with Google Sheets to store and retrieve data.
"""

import json
import os
from pathlib import Path

import autokitteh
from autokitteh.openai import openai_client
from autokitteh.slack import slack_client

import helpers
from repo_scanner import find_unanswered_comments


REPO_NAME = os.getenv("REPO_NAME")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SYSTEM_PROMPT = Path("prompt.txt").read_text()

chatgpt = openai_client("chatgpt_conn")
slack = slack_client("slack_conn")


def on_activate(_):
    """Entrypoint for the AI chatbot assistant."""
    while True:
        print("Waiting for a message...")
        subs = autokitteh.subscribe("slack_conn", "event_type == 'message'")
        data = autokitteh.next_event(subs)
        if data:
            on_slack_message(data)


def on_slack_message(data):
    """Determine the action to take based on an incoming Slack message.

    Args:
        data: The data from the Slack event.
    """
    user, user_text = data["user"], data["text"]
    response = get_chatgpt_response(user_text)

    # Always send initial response.
    slack.chat_postMessage(channel=user, text=response["message"])

    match response["action"]:
        case "list":
            rows = helpers.get_sheets_data(SHEET_NAME)
            message = helpers.format_messages_for_slack(rows)
            slack.chat_postMessage(channel=user, text=message)
        case "scan":
            comments = find_unanswered_comments(REPO_NAME, user)
            helpers.append_row_to_sheet(SHEET_NAME, comments)
            rows = helpers.get_sheets_data(SHEET_NAME)
            message = helpers.format_messages_for_slack(rows)
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
