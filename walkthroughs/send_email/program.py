"""Simple workflow for sending emails."""

import base64

from autokitteh.google import gmail_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn").users()


def on_manual_run(_):
    profile = gmail.getProfile(userId="me").execute()

    msg = f"""From: {profile["emailAddress"]}
    To: {profile["emailAddress"]}
    Subject: Test from AutoKitteh

    Meow! Just wanted to let you know that your cat overlords are pleased with your
    service today. Keep up the good work with the treats and belly rubs!"""

    msg = msg.replace("\n", "\r\n").replace("    ", "")
    msg = base64.urlsafe_b64encode(msg.encode()).decode()
    try:
        gmail.messages().send(userId="me", body={"raw": msg}).execute()
    except HttpError as e:
        print(f"Error: `{e.reason}`")
        return

    print("Message sent successfully!")
