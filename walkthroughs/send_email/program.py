"""Simple workflow for sending emails."""

import base64

from autokitteh.google import gmail_client
from googleapiclient.errors import HttpError


def on_manual_run(event):
    gmail = gmail_client("<INSERT_CONNECTION_NAME>").users()

    msg = f"""From: {event.data.sender}
    To: {event.data.recipient}
    Subject: Meow! {event.data.subject}

    {event.data.body}"""

    msg = msg.replace("\n", "\r\n").replace("    ", "")
    msg = base64.urlsafe_b64encode(msg.encode()).decode()
    try:
        gmail.messages().send(userId="me", body={"raw": msg}).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print("Message sent successfully!")
