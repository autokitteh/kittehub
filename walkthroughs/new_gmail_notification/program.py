"""Custom Gmail event system that works as a trigger when new emails arrive."""

from datetime import datetime, UTC
import os

import autokitteh
from autokitteh.google import gmail_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn")
TIME_LIMIT_MINUTES = int(os.getenv("TIME_LIMIT_MINUTES") or "16")


def poll_new_emails(_):
    """Poll for new emails in the Gmail inbox."""
    messages = (
        gmail.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"])
        .execute()
        .get("messages", [])
    )
    if not messages:
        print("No messages found in inbox")
        return

    latest_msg_id = messages[0]["id"]
    last_msg_id = autokitteh.get_value("last_msg_id")

    # First run: store latest message ID.
    if last_msg_id is None:
        autokitteh.set_value("last_msg_id", latest_msg_id)
        print("First run - storing latest message ID")
        return

    new_msg_ids = collect_new_messages(last_msg_id)

    if new_msg_ids:
        print(f"New emails: {len(new_msg_ids)}")
        for msg_id in new_msg_ids:
            process_message(msg_id)

    autokitteh.set_value("last_msg_id", latest_msg_id)


def collect_new_messages(last_msg_id):
    """Collect new message IDs until reaching last processed message or time limit."""
    new_msg_ids = []
    current_time = datetime.now(UTC)
    next_page_token = None

    while True:
        params = {"userId": "me", "labelIds": ["INBOX"]}
        if next_page_token:
            params["pageToken"] = next_page_token

        response = gmail.users().messages().list(**params).execute()
        messages = response.get("messages", [])

        if not messages:
            break

        for msg in messages:
            if msg["id"] == last_msg_id:
                return new_msg_ids

            if is_message_too_old(msg["id"], current_time):
                return new_msg_ids

            new_msg_ids.append(msg["id"])

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return new_msg_ids


def process_message(msg_id):
    """Process a single message."""
    try:
        full_message = gmail.users().messages().get(userId="me", id=msg_id).execute()
        headers = {
            h["name"]: h["value"]
            for h in full_message.get("payload", {}).get("headers", [])
        }

        print("New Mail Received:")
        print(f"From: {headers.get('From')}")
        print(f"To: {headers.get('To')}")
        print(f"Subject: {headers.get('Subject')}")
        print("-" * 50)

    except HttpError as e:
        print(f"Error fetching message {msg_id}: {e}")


def is_message_too_old(msg_id, current_time):
    """Check if a message is older than the time limit."""
    try:
        msg_details = (
            gmail.users()
            .messages()
            .get(userId="me", id=msg_id, fields="internalDate")
            .execute()
        )
        email_timestamp = int(msg_details.get("internalDate", 0)) / 1000
        email_datetime = datetime.fromtimestamp(email_timestamp, UTC)
        time_diff_minutes = (current_time - email_datetime).total_seconds() / 60

        if time_diff_minutes > TIME_LIMIT_MINUTES:
            print(f"Stopped processing emails older than {TIME_LIMIT_MINUTES} minutes.")
            return True

        return False

    except HttpError as e:
        print(f"Error checking timestamp for message {msg_id}: {e}")
        return False
