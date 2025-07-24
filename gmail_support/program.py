"""Gmail Support Email Workflow.

This program monitors for new emails from a specific sender,
analyzes them using ChatGPT to determine if they're support-related,
and takes appropriate actions for support emails.
"""

import base64
from datetime import datetime, UTC
import os

import autokitteh
from autokitteh.google import gmail_client
from autokitteh.openai import openai_client
from autokitteh.slack import slack_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn").users()
chatgpt = openai_client("chatgpt_conn")
slack = slack_client("slack_conn")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
if not SENDER_EMAIL:
    raise ValueError("The environment variable 'SENDER_EMAIL' is not set or is empty.")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#support-notifications")
AUTO_REPLY = "Thank you for your email. We will get back to you within 2 hours"


def on_new_email(event):
    """Handle Gmail mailbox change events.

    This function processes Gmail mailbox changes, identifies new emails
    from the specified sender, and processes them accordingly.
    """
    try:
        history_id = event.data.get("history_id")
        if not history_id:
            return

        current_history_id = int(history_id)
        last_processed_id = int(
            autokitteh.get_value("last_processed_id") or (current_history_id - 100)
        )

        history = (
            gmail.history()
            .list(userId="me", startHistoryId=str(last_processed_id))
            .execute()
        )

        if "history" in history:
            for history_record in history["history"]:
                record_id = int(history_record["id"])

                if record_id <= last_processed_id:
                    continue

                if "messagesAdded" in history_record:
                    for message_entry in history_record["messagesAdded"]:
                        message_id = message_entry["message"]["id"]
                        process_message(message_id)

        if current_history_id > last_processed_id:
            autokitteh.set_value("last_processed_id", str(current_history_id))

    except HttpError as e:
        print(f"Error processing mailbox change: {e}")


@autokitteh.activity
def process_message(message_id):
    """Process a single email message.

    Args:
        message_id: The Gmail message ID to process.
    """
    try:
        message = (
            gmail.messages().get(userId="me", id=message_id, format="full").execute()
        )

        headers = {
            h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])
        }

        from_email = headers.get("From", "")
        subject = headers.get("Subject", "")

        if SENDER_EMAIL not in from_email:
            print(f"Skipping email from {from_email} - not from target sender")
            return

        print(f"Processing email from {from_email} with subject: {subject}")

        email_body = extract_email_body(message)

        is_support = analyze_with_chatgpt(subject, email_body)

        if is_support:
            print("Email identified as support-related")
            send_reply(message_id, headers)
            send_slack_notification(from_email, subject, email_body)
        else:
            print("Email not identified as support-related")

    except HttpError as e:
        print(f"Error processing message {message_id}: {e.reason}")


@autokitteh.activity
def extract_email_body(message):
    """Extract the text body from a Gmail message.

    Args:
        message: The Gmail message object.

    Returns:
        str: The extracted email body text.
    """
    parts = []

    def extract_parts(payload):
        if "parts" in payload:
            for part in payload["parts"]:
                extract_parts(part)
        elif payload.get("mimeType") == "text/plain":
            if "data" in payload.get("body", {}):
                encoded_data = payload["body"]["data"]
                decoded_data = base64.urlsafe_b64decode(encoded_data).decode("utf-8")
                parts.append(decoded_data)

    extract_parts(message.get("payload", {}))

    if not parts and "body" in message.get("payload", {}):
        # Handle single-part messages
        if "data" in message["payload"]["body"]:
            encoded_data = message["payload"]["body"]["data"]
            decoded_data = base64.urlsafe_b64decode(encoded_data).decode("utf-8")
            parts.append(decoded_data)

    return "\n".join(parts)


@autokitteh.activity
def analyze_with_chatgpt(subject, body):
    """Analyze email content with ChatGPT to determine if it's support-related."""
    prompt = (
        f"\n"
        "Analyze the following email and determine if it's related to customer support "
        "or technical assistance.\n\n"
        f"Subject: {subject}\n\n"
        "Body:\n"
        f"{body}\n\n"
        "Is this email related to customer support or technical assistance?\n"
        "Answer with only 'yes' or 'no'.\n"
    )

    response = chatgpt.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an email classifier that determines if emails are "
                    "support-related."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=10,
    )

    answer = response.choices[0].message.content.strip().lower()
    return "yes" in answer


@autokitteh.activity
def send_reply(message_id, headers):
    """Send an auto-reply to a support email."""
    try:
        to_email = headers.get("From")
        if not to_email:
            print("Cannot send reply: From header missing")
            return

        profile = gmail.getProfile(userId="me").execute()
        from_email = profile["emailAddress"]

        original_message = (
            gmail.messages().get(userId="me", id=message_id, format="full").execute()
        )
        thread_id = original_message.get("threadId")

        if not thread_id:
            print("Cannot send reply: Thread ID not found")
            return

        original_message_id = headers.get("Message-ID", "")

        subject = headers.get("Subject", "")
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"

        message_headers = [
            f"From: {from_email}",
            f"To: {to_email}",
            f"Subject: {subject}",
            "Content-Type: text/plain; charset=UTF-8",
        ]

        if original_message_id:
            message_headers.extend(
                [
                    f"In-Reply-To: {original_message_id}",
                    f"References: {original_message_id}",
                ]
            )

        message_content = (
            "\n".join(message_headers)
            + f"\n\n{AUTO_REPLY}\n\nBest regards,\nThe Support Team\n"
        )

        encoded_message = base64.urlsafe_b64encode(message_content.encode()).decode()

        gmail.messages().send(
            userId="me", body={"raw": encoded_message, "threadId": thread_id}
        ).execute()

        print(f"Auto-reply sent to {to_email}")

    except HttpError as e:
        print(f"Error sending reply: {e.reason}")
        print(f"Error details: {e}")


@autokitteh.activity
def send_slack_notification(from_email, subject, body):
    """Send a notification to Slack about a new support email.

    Args:
        from_email: The sender's email address.
        subject: The email subject.
        body: The email body.
    """
    if len(body) > 500:
        body = body[:497] + "..."

    # Format the message.
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    message = f"""
:email: *New Support Email Received*
*From:* {from_email}
*Subject:* {subject}
*Time:* {now}

*Email Content:*
```
{body}
```
"""

    slack.chat_postMessage(
        channel=SLACK_CHANNEL, text=message, unfurl_links=False, unfurl_media=False
    )

    print(f"Slack notification sent to {SLACK_CHANNEL}")
