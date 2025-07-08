"""Custom Gmail event system that work as a trigger when new emails arrive."""

import autokitteh
from autokitteh.google import gmail_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn")


def poll_new_emails(_):
    """Poll for new emails in the Gmail inbox

    This function acts as a custom event handler for Gmail mailbox changes
    (triggered via Polling method). Due to limitations
    in Gmail's native history ID event handling, this
    function detects and handles incoming emails events.
    """
    response = gmail.users().messages().list(userId="me", labelIds=["INBOX"]).execute()

    if not response.get("messages"):
        print("No messages found in inbox")
        return

    newest_message_id = response["messages"][0]["id"]

    # If this is the first run, store the latest message ID and finish.
    last_known_id = autokitteh.get_value("last_message_id")
    if last_known_id is None:
        autokitteh.set_value("last_message_id", newest_message_id)
        print("First run - storing latest message ID")
        return

    # Collect new message IDs until we reach the previous message ID.
    new_message_ids = []
    found_last_message = False
    current_response = response

    while not found_last_message:
        current_messages = current_response.get("messages", [])

        # Check current batch of messages.
        for msg in current_messages:
            if msg["id"] == last_known_id:
                found_last_message = True
                break
            new_message_ids.append(msg["id"])

        if not found_last_message:
            next_page_token = current_response.get("nextPageToken")
            if not next_page_token:
                break

            current_response = (
                gmail.users()
                .messages()
                .list(userId="me", labelIds=["INBOX"], pageToken=next_page_token)
                .execute()
            )

            if not current_response.get("messages"):
                # No more messages.
                break

    # Process new messages.
    count = len(new_message_ids)
    print(f"New emails: {count}")

    if count > 0:
        for message_id in new_message_ids:
            try:
                full_message = (
                    gmail.users().messages().get(userId="me", id=message_id).execute()
                )
                on_new_message(full_message)
                print("-" * 50)
            except HttpError as e:
                print(f"Error fetching message {message_id}: {e}")

        # Update last_message_id to the newest message.
        autokitteh.set_value("last_message_id", newest_message_id)


# Triggered from the custom event handler function.
def on_new_message(message):
    """Print details of a new message."""
    headers = {
        h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])
    }
    print("New Mail Received:")
    print(f"From: {headers.get('From')}")
    print(f"To: {headers.get('To')}")
    print(f"Subject: {headers.get('Subject')}")
