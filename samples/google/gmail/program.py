"""This program demonstrates AutoKitteh's 2-way Gmail integration.

API documentation:
- https://docs.autokitteh.com/integrations/google/gmail/python
- https://docs.autokitteh.com/integrations/google/gmail/events
"""

import base64
import json

from autokitteh.google import gmail_client
from autokitteh.slack import slack_client
from googleapiclient.errors import HttpError


gmail = gmail_client("gmail_conn").users()
slack = slack_client("slack_conn")


def on_slack_slash_command(event):
    """Use a Slack slash command to interact with a Gmail mailbox.

    See: https://api.slack.com/interactivity/slash-commands, and
    https://api.slack.com/interactivity/handling#message_responses

    In this sample, we expect the slash command's text to be:
    - "gmail get profile"
    - "gmail drafts list [optional query]"
    - "gmail drafts get <draft ID>"
    - "gmail messages list [optional query]"
    - "gmail messages get <message ID>"
    - "gmail messages send <short message to yourself>"

    Args:
        event: Slack event data.
    """
    for cmd, handler in COMMANDS.items():
        if event.data.text.startswith(cmd):
            handler(event.data.user_id, event.data.text[len(cmd) + 1 :])
            return


def _get_profile(slack_channel, _):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.html#getProfile

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
        _: Unused suffix of the user's Slack command, if any.
    """
    resp = gmail.getProfile(userId="me").execute()
    slack.chat_postMessage(channel=slack_channel, text=resp["emailAddress"])
    msg = f"Total no. of messages: `{resp['messagesTotal']}`"
    slack.chat_postMessage(channel=slack_channel, text=msg)
    msg = f"Total no. of threads: `{resp['threadsTotal']}`"
    slack.chat_postMessage(channel=slack_channel, text=msg)
    msg = f"Current History record ID: `{resp['historyId']}`"
    slack.chat_postMessage(channel=slack_channel, text=msg)


def _drafts_get(slack_channel, id):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#get

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
        id: Required ID of the draft to retrieve.
    """
    try:
        resp = gmail.drafts().get(userId="me", id=id).execute()
    except HttpError as e:
        slack.chat_postMessage(channel=slack_channel, text=f"Error: `{e.reason}`")
        return

    msg = f"```\n{json.dumps(resp, indent=2)}\n```"
    slack.chat_postMessage(channel=slack_channel, text=msg)


def _drafts_list(slack_channel, query):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.drafts.html#list

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
        query: Optional query, e.g. "is:unread".
    """
    try:
        resp = gmail.drafts().list(userId="me", q=query, maxResults=10).execute()
    except HttpError as e:
        slack.chat_postMessage(channel=slack_channel, text=f"Error: `{e.reason}`")
        return

    msg = f"Result size estimate: `{resp['resultSizeEstimate']}`"
    slack.chat_postMessage(channel=slack_channel, text=msg)

    for i, d in enumerate(resp.get("drafts", []), start=1):
        msg = f"{i}\n```\n{json.dumps(d, indent=2)}\n```"
        slack.chat_postMessage(channel=slack_channel, text=msg)

    next_page_token = resp.get("nextPageToken")
    if next_page_token:
        msg = f"Next page token: `{next_page_token}`"
        slack.chat_postMessage(channel=slack_channel, text=msg)


def _messages_get(slack_channel, id):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#get

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
        id: Required ID of the message to retrieve.
    """
    try:
        resp = gmail.messages().get(userId="me", id=id).execute()
    except HttpError as e:
        slack.chat_postMessage(channel=slack_channel, text=f"Error: `{e.reason}`")
        return

    msg = f"```\n{json.dumps(resp, indent=2)}\n```"
    slack.chat_postMessage(channel=slack_channel, text=msg)


def _messages_list(slack_channel, query):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list

    See also:
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list_next

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
        query: Optional query, e.g. "is:unread".
    """
    try:
        resp = gmail.messages().list(userId="me", q=query, maxResults=10).execute()
    except HttpError as e:
        slack.chat_postMessage(channel=slack_channel, text=f"Error: `{e.reason}`")
        return

    msg = f"Result size estimate: `{resp['resultSizeEstimate']}`"
    slack.chat_postMessage(channel=slack_channel, text=msg)

    for i, m in enumerate(resp.get("messages", []), start=1):
        msg = f"{i}\n```\n{json.dumps(m, indent=2)}\n```"
        slack.chat_postMessage(channel=slack_channel, text=msg)

    next_page_token = resp.get("nextPageToken")
    if next_page_token:
        msg = f"Next page token: `{next_page_token}`"
        slack.chat_postMessage(channel=slack_channel, text=msg)


def _messages_send(slack_channel, text):
    """https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#send

    See also: https://developers.google.com/gmail/api/guides/sending

    This is the same as Google's send-message snippet, but simpler:
    https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/send_message.py

    Args:
        slack_channel: Slack channel name/ID to post debug messages to.
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
        slack.chat_postMessage(channel=slack_channel, text=f"Error: `{e.reason}`")
        return

    slack.chat_postMessage(channel=slack_channel, text="Sent!")


def on_gmail_mailbox_change(event):
    pass  # TODO(ENG-1524): Implement this function.


COMMANDS = {
    "gmail get profile": _get_profile,
    "gmail drafts get": _drafts_get,
    "gmail drafts list": _drafts_list,
    "gmail messages get": _messages_get,
    "gmail messages list": _messages_list,
    "gmail messages send": _messages_send,
}
