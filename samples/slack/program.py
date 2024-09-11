"""This program demonstrates AutoKitteh's 2-way Slack integration.

This program implements multiple entry-point functions that are triggered
by incoming Slack events, as defined in the "autokitteh-python.yaml"
manifest file. These functions also execute various Slack API calls.

Events that this program responds to:
- Mentions of the Slack app in messages (e.g. "Hi @autokitteh")
- Slash commands registered by the Slack app (`/autokitteh <channel name or ID>`)
- New and edited messages and replies
- New emoji reactions

Slack API documentation:
- Python client API: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html
- Events API reference: https://api.slack.com/events?filter=Events

This program isn't meant to cover all available functions and events.
It merely showcases a few illustrative, annotated, reusable examples.
"""

from pathlib import Path
import time

import autokitteh
from autokitteh.slack import slack_client


def on_slack_app_mention(event):
    """https://api.slack.com/events/app_mention

    Args:
        event: Slack event data.
    """
    slack = slack_client("slack_conn")

    # Send messages in response to the event:
    # - DM to the user who triggered the event (channel ID = user ID)
    # - Two messages to the channel "#slack-test"
    # See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient.chat_postMessage
    text = f"You mentioned me in <#{event.data.channel}> and wrote: `{event.data.text}`"
    slack.chat_postMessage(channel=event.data.user, text=text)

    text = text.replace("You", f"<@{event.data.user}>")
    slack.chat_postMessage(channel="#slack-test", text=text)

    text = "Before update :crying_cat_face:"
    resp = slack.chat_postMessage(channel="#slack-test", text=text)

    # Encountered an error? Print debugging information
    # in the AutoKitteh session's log, and finish.
    resp.validate()

    # Update the last sent message, after a few seconds.
    # See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient.chat_update
    time.sleep(10)
    resp = autokitteh.AttrDict(resp.data)
    text = "After update :smiley_cat:"
    resp = slack.chat_update(channel=resp.channel, ts=resp.ts, text=text)
    resp = autokitteh.AttrDict(resp.data)

    # Reply to the message's thread, after a few seconds.
    time.sleep(5)
    text = "Reply before update :crying_cat_face:"
    resp = slack.chat_postMessage(channel=resp.channel, text=text, thread_ts=resp.ts)
    resp = autokitteh.AttrDict(resp.data)

    # Update the threaded reply message, after a few seconds.
    time.sleep(5)
    text = "Reply after update :smiley_cat:"
    slack.chat_update(channel=resp.channel, ts=resp.ts, text=text)

    # Add a reaction to the threaded reply message.
    # See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient.reactions_add
    slack.reactions_add(channel=resp.channel, name="blob-clap", timestamp=resp.ts)

    # Retrieve all the replies.
    # See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient.conversations_replies
    resp = slack.conversations_replies(channel=resp.channel, ts=resp.ts)

    # For educational purposes, print all the replies in the AutoKitteh session's log.
    resp.validate()
    for text in resp.get("messages", default=[]):
        print(text)


def on_slack_message(event):
    """https://api.slack.com/events/message

    Args:
        event: Slack event data.
    """
    slack = slack_client("slack_conn")

    if not event.data.subtype:
        user = f"<@{event.data.user}>"
        if not event.data.thread_ts:
            _on_slack_new_message(slack, event.data, user)
        else:
            # https://api.slack.com/events/message/message_replied
            _on_slack_reply_message(slack, event.data, user)
    elif event.data.subtype == "message_changed":
        user = f"<@{event.data.message.user}>"  # Not the same as above!
        _on_slack_message_changed(slack, event.data, user)


def _on_slack_new_message(slack, data, user):
    """Someone wrote a new message."""
    text = f":point_up: {user} wrote: `{data.text}`"
    slack.chat_postMessage(channel=data.channel, text=text)


def _on_slack_reply_message(slack, data, user):
    """Someone wrote a reply in a thread."""
    text = f":point_up: {user} wrote a reply to <@{data.parent_user_id}>: `{data.text}`"
    ts = data.thread_ts
    slack.chat_postMessage(channel=data.channel, text=text, thread_ts=ts)


def _on_slack_message_changed(slack, data, user):
    """Someone edited a message."""
    old, new = data.previous_message.text, data.message.text
    text = f":point_up: {user} edited a message from `{old}` to `{new}`"

    # Thread TS may or may not be empty, depending on the edited message.
    thread = data.message.thread_ts

    slack.chat_postMessage(channel=data.channel, text=text, thread_ts=thread)


def on_slack_reaction_added(event):
    """https://api.slack.com/events/reaction_added

    Args:
        event: Slack event data.
    """
    # For educational purposes, print the event data in the AutoKitteh session's log.
    print(event.data.user)
    print(event.data.reaction)
    print(event.data.item)


def on_slack_slash_command(event):
    """https://api.slack.com/interactivity/slash-commands

    See also: https://api.slack.com/interactivity/handling#message_responses

    The text after the slash command is expected to be a valid target for a
    Slack message (https://api.slack.com/methods/chat.postMessage#channels):
    Slack user ID ("U"), user DM ID ("D"), multi-person/group DM ID ("G"),
    channel ID ("C"), or channel name (with or without the "#" prefix).

    Note that all targets except "U", "D" and public channels require
    the Slack app to be added in advance.

    Args:
        event: Slack event data.
    """
    slack = slack_client("slack_conn")

    # Retrieve the profile information of the user who triggered this event.
    # See: https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/client.html#slack_sdk.web.client.WebClient.users_info
    user_info = slack.users_info(user=event.data.user_id)

    # Encountered an error? Print debugging information
    # in the AutoKitteh session's log, and finish.
    user_info.validate()

    profile = autokitteh.AttrDict(user_info.data).user.profile
    text = f"Slack mention: <@{event.data.user_id}>"
    slack.chat_postMessage(channel=event.data.user_id, text=text)
    text = "Full name: " + profile.real_name
    slack.chat_postMessage(channel=event.data.user_id, text=text)
    text = "Email: " + profile.email
    slack.chat_postMessage(channel=event.data.user_id, text=text)

    # Treat the text of the user's slash command as a message target (e.g.
    # channel or user), and send an interactive message to that target.
    blocks = Path("approval_message.json.txt").read_text()
    changes = [
        ("Title", "Question From " + profile.real_name),
        ("Message", "Please select one of these options... :smiley_cat:"),
        ("ActionID", event.data.user_id),
    ]
    for old, new in changes:
        blocks = blocks.replace(old, new)

    slack.chat_postMessage(channel=event.data.text, blocks=blocks)


def on_slack_interaction(event):
    """https://api.slack.com/reference/interaction-payloads/block-actions

    Args:
        event: Slack event data.
    """
    # The Slack ID of the user who sent the question
    # (we stored this in the buttons' action IDs).
    action = autokitteh.AttrDict(event.data.actions[0])
    origin = action.action_id.split()[-1]

    # User selection = action value = button text
    # (our convention, not Slack's, alternatives: action style/text).
    text = f"<@{event.data.user.id}> clicked the `{action.value}` button"
    if action.style == "primary":  # Green button.
        text += " :+1:"
    elif action.style == "danger":  # Red button.
        text += " :-1:"

    slack = slack_client("slack_conn")
    slack.chat_postMessage(channel=origin, text=text)
