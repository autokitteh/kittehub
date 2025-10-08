"""Notification delivery system for incident alerts.

This module handles sending notifications to contacts through multiple channels
including email (Gmail), SMS (Twilio), and Slack messages. It initializes
connections to these services and provides a unified interface for notifying
contacts about incidents.
"""

import base64

from autokitteh.errors import ConnectionInitError
from autokitteh.google import gmail_client
from autokitteh.slack import slack_client
from autokitteh.twilio import twilio_client
from googleapiclient.errors import HttpError
from model import Contact
from slack_sdk.web.client import WebClient as SlackWebClient
from twilio.base.exceptions import TwilioRestException

import config
from slack_sdk.errors import SlackApiError
from twilio.rest import Client as TwilioClient


try:
    twilio: TwilioClient | None = twilio_client("twilio")
except ConnectionInitError:
    twilio = None
    print("WARN: twilio connection not initialized.")

try:
    slack: SlackWebClient | None = slack_client("slack")
except ConnectionInitError:
    slack = None
    print("WARN: slack connection not initialized.")

try:
    gmail = gmail_client("gmail")
except ConnectionInitError:
    gmail = None
    print("WARN: gmail connection not initialized.")


def notify(contact: Contact, subject: str, message: str) -> None:
    print(f"notifying {contact}: {subject}...")

    any_sent = False

    if contact.phone:
        any_sent |= _send_twilio_message(contact.phone, subject, message)

    if contact.email:
        any_sent |= _send_email(contact.email, subject, message)

    if contact.email:
        any_sent |= _send_slack_message(contact.email, subject, message)

    if not any_sent:
        print(f"WARN: no notification sent to {contact.name}.")


def _send_email(email: str, subject: str, message: str) -> bool:
    if not gmail:
        return False

    print(f"sending email to {email}...")

    users = gmail.users()
    profile = users.getProfile(userId="me").execute()

    msg = f"""From: {profile["emailAddress"]}
To: {email}
Subject: {subject}

{message}""".replace("\n", "\r\n")

    msg = base64.urlsafe_b64encode(msg.encode()).decode()

    try:
        msg = users.messages().send(userId="me", body={"raw": msg}).execute()
        print(f"sent message {msg['id']}.")
        return True
    except HttpError as e:
        print(f"ERROR: `{e.reason}`")
        return False


def _send_twilio_message(phone: str, subject: str, message: str) -> bool:
    if not twilio:
        return False

    print(f"sending text to {phone}...")

    try:
        msg = twilio.messages.create(
            from_=config.TWILIO_PHONE_NUMBER,
            to=phone,
            body=f"{subject}\n\n{message}",
        )

        print(f"sent message {msg.sid}.")

        return True
    except TwilioRestException as e:
        print(f"ERROR: `{e}`")
        return False


def _send_slack_message(email: str, subject: str, message: str) -> bool:
    if not slack:
        return False

    print(f"sending slack message to {email}...")

    try:
        user_id = slack.users_lookupByEmail(email=email)["user"]["id"]
    except SlackApiError as e:
        print(f"error: {e}")
        return False

    try:
        msg = slack.chat_postMessage(
            channel=user_id,
            text=f"*{subject}*\n\n{message}",
        )
        print(f"sent message {msg['ts']}.")
        return True
    except SlackApiError as e:
        print(f"ERROR: `{e.response['error']}`")
        return False
