"""
This program demonstrates a real-life workflow that integrates Gmail, ChatGPT, and Slack.

Workflow:
1. Trigger: Detect a new email in Gmail.
2. Categorize: Use ChatGPT to read and categorize the email (e.g., technical work, marketing, sales).
3. Notify: Send a message to the corresponding Slack channel based on the category.
4. Label: Add a label to the email in Gmail.
"""

import base64
from datetime import datetime, timezone
import os
import time

import autokitteh
from autokitteh import google, openai, slack


POLL_INTERVAL = os.getenv("POLL_INTERVAL")
SLACK_CHANNELS = ["demos", "engineering", "ui"]


gmail = google.gmail_client("my_gmail").users()
processed_message_ids = set()
start_time = datetime.now(timezone.utc).timestamp()


def on_http_get(event):
    while True:
        _poll_inbox()
        time.sleep(float(POLL_INTERVAL))


def _poll_inbox():
    token = None
    current_message_ids = set()

    while True:
        results = get_new_inbox_messages(token)

        current_message_ids.update({msg["id"] for msg in results.get("messages", [])})

        token = results.get("nextPageToken")
        if not token:
            break

    new_message_ids = current_message_ids - processed_message_ids

    for message_id in new_message_ids:
        _process_email(message_id, start_time)

    processed_message_ids.update(new_message_ids)


@autokitteh.activity
def get_new_inbox_messages(token):
    query = "in:inbox -in:drafts"
    if token:
        gmail_list = gmail.messages().list(userId="me", q=query, pageToken=token)
        results = gmail_list.execute()
    else:
        results = gmail.messages().list(userId="me", q=query).execute()
    return results


def _process_email(message_id: str, start_time: datetime):
    message = get_message(message_id)
    email_timestamp = float(message["internalDate"]) / 1000

    if email_timestamp < start_time:
        return

    email_content = _parse_email(message)

    if email_content:
        channel = _categorize_email(email_content)

        if channel:
            client = slack.slack_client("my_slack")
            text = email_content or "Email content not found."
            client.chat_postMessage(channel=channel, text=text)

        # Add label to email
        label_id = _get_label_id(channel) or _create_label(channel)
        if label_id:
            body = {"addLabelIds": [label_id]}
            apply_label_to_message(message_id, body)


@autokitteh.activity
def apply_label_to_message(message_id, body):
    gmail.messages().modify(userId="me", id=message_id, body=body).execute()


@autokitteh.activity
def get_message(message_id):
    message = gmail.messages().get(userId="me", id=message_id).execute()
    return message


def _parse_email(message: dict):
    payload = message["payload"]
    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain":
            email_body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
            return email_body
    return None


@autokitteh.activity
def _create_label(label_name: str) -> str:
    """Create a new label in the user's gmail account.

    https://developers.google.com/gmail/api/reference/rest/v1/users.labels#Label
    """
    label = {
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show",
        "name": label_name,
    }
    try:
        created_label = gmail.labels().create(userId="me", body=label).execute()
    except Exception as e:
        print(f"Error creating label: {e}")
    return created_label["id"] if created_label else None


@autokitteh.activity
def _get_label_id(label_name: str) -> str:
    labels_response = gmail.labels().list(userId="me").execute()
    labels = labels_response.get("labels", [])
    for label in labels:
        if label["name"] == label_name:
            return label["id"]
    return None


@autokitteh.activity
def _categorize_email(email_content: str) -> str:
    """Prompt ChatGPT to categorize an email based on its content.

    Returns:
        The name of the Slack channel to send a message to as a string.
        If the channel is not in the provided list, returns None.
    """
    client = openai.openai_client("my_chatgpt")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"""Categorize the following email based on its
                topic and suggest a channel to post it in from the 
                provided list. The output should be one of the provided 
                channels and nothing else.
                Email Content: {email_content} Channels: {SLACK_CHANNELS}
                Output example: {SLACK_CHANNELS[0]}""",
            },
        ],
    )
    channel = response.choices[0].message.content
    return channel if channel in SLACK_CHANNELS else None
