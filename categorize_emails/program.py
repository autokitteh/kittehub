"""A real-life workflow that integrates Gmail, ChatGPT, and Slack:

1. Trigger: Detect a new email in Gmail.
2. Categorize: Use ChatGPT to read and categorize the email
   (e.g., technical work, marketing, sales).
3. Notify: Send a message to the corresponding Slack channel based on the category.
4. Label: Add a label to the email in Gmail.
"""

import base64
from datetime import datetime, UTC
import os
import time

import autokitteh
from autokitteh.google import gmail_client
from autokitteh.openai import openai_client
from autokitteh.slack import slack_client


POLL_INTERVAL = float(os.getenv("POLL_INTERVAL"))
SLACK_CHANNELS = ["demos", "engineering", "ui"]


gmail = gmail_client("my_gmail").users()
slack = slack_client("my_slack")
processed_message_ids = set()
start_time = datetime.now(UTC).timestamp()


def on_http_get(event):
    while True:
        _poll_inbox()
        time.sleep(POLL_INTERVAL)


def _poll_inbox():
    current_message_ids = set()
    results = get_new_inbox_messages()
    current_message_ids.update({msg["id"] for msg in results.get("messages", [])})
    new_message_ids = current_message_ids - processed_message_ids

    for message_id in new_message_ids:
        _process_email(message_id, start_time)

    processed_message_ids.update(new_message_ids)


def _process_email(message_id: str, start_time: datetime):
    message = gmail.messages().get(userId="me", id=message_id).execute()
    email_timestamp = float(message["internalDate"]) / 1000

    if email_timestamp < start_time:
        return

    email_content = _parse_email(message)

    if not email_content:
        print("Email content not found.")
        return

    channel = _categorize_email(email_content)

    if not channel:
        print("Could not categorize email.")
        return

    slack.chat_postMessage(channel=channel, text=email_content)

    # Add label to email
    label_id = _get_label_id(channel) or _create_label(channel)
    if not label_id:
        return

    body = {"addLabelIds": [label_id]}
    gmail.messages().modify(userId="me", id=message_id, body=body).execute()


def _parse_email(message: dict):
    payload = message["payload"]
    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            email_body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
            return email_body
    return None


def _create_label(label_name: str) -> str:
    """Create a new label in the user's gmail account.

    https://developers.google.com/gmail/api/reference/rest/v1/users.labels#Label
    """
    label = {
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "name": label_name,
    }
    created_label = gmail.labels().create(userId="me", body=label).execute()
    return created_label.get("id", None)


def _get_label_id(label_name: str) -> str:
    labels_response = gmail.labels().list(userId="me").execute()
    labels = labels_response.get("labels", [])
    for label in labels:
        if label["name"] == label_name:
            return label["id"]
    return None


def get_new_inbox_messages():
    query = "in:inbox -in:drafts"
    return gmail.messages().list(userId="me", q=query, maxResults=10).execute()


@autokitteh.activity
def _categorize_email(email_content: str) -> str:
    """Prompt ChatGPT to categorize an email based on its content.

    Returns:
        The name of the Slack channel to send a message to as a string.
        If the channel is not in the provided list, returns None.
    """
    client = openai_client("my_chatgpt")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": (
                    "Categorize the following email based on its topic and suggest a "
                    "channel to post it in from the provided list. The output should "
                    "be one of the channels in {SLACK_CHANNELS} and nothing else, "
                    "for example: {SLACK_CHANNELS[0]}\n\nEmail content: {email_content}"
                ),
            },
        ],
    )
    channel = response.choices[0].message.content
    return channel if channel in SLACK_CHANNELS else None
