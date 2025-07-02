"""This program demonstrates AutoKitteh's 2-way Gmail integration.

API documentation:
- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events
"""

import base64
import json

import autokitteh
from autokitteh.google import gmail_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn").users()


def on_http_get(event):
    """Handle Gmail interaction via HTTP trigger using query params.

    Example URL: "http://localhost:9980/webhooks/<webhook_slug>?cmd=list_drafts"

    Commands:
    - cmd=get_profile
    - cmd=list_drafts&query=optional_query
    - cmd=get_draft&draft_id=<draft_ID>
    - cmd=list_messages&query=optional_query
    - cmd=get_message&message_id=<message_ID>
    - cmd=send_message&text=<message_text>

    Args:
        event: HTTP request event data (contains query parameters).
    """
    params = event.data.url.query
    cmd = params.get("cmd")

    match cmd:
        case "get_profile":
            _get_profile()
        case "list_drafts":
            _drafts_list(params.get("query", ""))
        case "get_draft":
            _drafts_get(params.get("draft_id"))
        case "list_messages":
            _messages_list(params.get("query", ""))
        case "get_message":
            _messages_get(params.get("message_id"))
        case "send_message":
            _messages_send(params.get("text"))
        case _:
            return "Unknown command"


def _get_profile():
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.html#getProfile"""
    resp = gmail.getProfile(userId="me").execute()
    print(resp["emailAddress"])
    print("Total no. of messages:", resp["messagesTotal"])
    print("Total no. of threads:", resp["threadsTotal"])
    print("Current History record ID:", resp["historyId"])


def _drafts_get(id):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#get

    Args:
        id: Required ID of the draft to retrieve.
    """
    try:
        resp = gmail.drafts().get(userId="me", id=id).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print(f"```\n{json.dumps(resp, indent=4)}\n```")


def _drafts_list(query):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#list

    Args:
        query: Optional query, e.g. "is:unread".
    """
    try:
        resp = gmail.drafts().list(userId="me", q=query, maxResults=10).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print(f"Result size estimate: `{resp['resultSizeEstimate']}`")

    for i, d in enumerate(resp.get("drafts", []), start=1):
        print(f"{i}\n```\n{json.dumps(d, indent=4)}\n```")

    next_page_token = resp.get("nextPageToken")
    if next_page_token:
        print(f"Next page token: `{next_page_token}`")


def _messages_get(id):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#get

    Args:
        id: Required ID of the message to retrieve.
    """
    try:
        resp = gmail.messages().get(userId="me", id=id).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print(f"```\n{json.dumps(resp, indent=4)}\n```")


def _messages_list(query):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list

    See also:
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list_next

    Args:
        query: Optional query, e.g. "is:unread".
    """
    try:
        resp = gmail.messages().list(userId="me", q=query, maxResults=10).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print(f"Result size estimate: `{resp['resultSizeEstimate']}`")

    for i, m in enumerate(resp.get("messages", []), start=1):
        print(f"{i}\n```\n{json.dumps(m, indent=4)}\n```")

    next_page_token = resp.get("nextPageToken")
    if next_page_token:
        print(f"Next page token: `{next_page_token}`")


def _messages_send(text):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#send

    See also: https://developers.google.com/gmail/api/guides/sending

    This is the same as Google's send-message snippet, but simpler:
    https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/send_message.py

    Args:
        text: Short message to send to yourself.
    """
    profile = gmail.getProfile(userId="me").execute()

    # Raw text compliant with https://datatracker.ietf.org/doc/html/rfc5322.
    msg = f"""From: {profile["emailAddress"]}
    To: {profile["emailAddress"]}
    Subject: Test from AutoKitteh

    {text}"""

    msg = msg.replace("\n", "\r\n").replace("    ", "")
    msg = base64.urlsafe_b64encode(msg.encode()).decode()
    try:
        gmail.messages().send(userId="me", body={"raw": msg}).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print("Message sent successfully!")


def on_gmail_mailbox_change(event):
    """Gmail Mailbox Change Event Handler.

    This function acts as a custom event handler for Gmail mailbox changes
    (triggered via Pub/Sub webhook events). Due to limitations
    in Gmail's native history ID event handling, this
    function detects and handles incoming emails events.
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

                # Skip already processed records.
                if record_id <= last_processed_id:
                    continue

                if "messagesAdded" in history_record:
                    for message_entry in history_record["messagesAdded"]:
                        message_id = message_entry["message"]["id"]
                        message = (
                            gmail.messages()
                            .get(
                                userId="me",
                                id=message_id,
                                format="metadata",
                                metadataHeaders=["From", "To", "Subject"],
                            )
                            .execute()
                        )

                        # Only process INBOX messages (incoming).
                        labels = message.get("labelIds", [])
                        if "INBOX" in labels and "SENT" not in labels:
                            on_new_message(message)

        # Only update if we processed something new.
        if current_history_id > last_processed_id:
            autokitteh.set_value("last_processed_id", str(current_history_id))

    except HttpError as e:
        print(f"Error: {e.reason}")


def on_new_message(message):
    headers = {
        h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])
    }
    print("New Mail Received:")
    print(f"From: {headers.get('From')}")
    print(f"To: {headers.get('To')}")
    print(f"Subject: {headers.get('Subject')}")
