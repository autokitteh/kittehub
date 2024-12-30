"""Simple utility functions for debugging and reporting errors in Slack.

Decoupled from the "slack_helper" module, to avoid circular imports.
"""

import os
import re
import traceback

from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError


_DEBUG_CHANNEL = os.getenv("SLACK_DEBUG_CHANNEL")

slack = slack_client("slack_conn")


def log(msg: str) -> None:
    """Post a debug message to a predefined Slack channel, if defined.

    Also post a filtered traceback, as replies to that message.
    """
    if not _DEBUG_CHANNEL or not msg:
        return

    print("DEBUG:", msg)
    try:
        resp = slack.chat_postMessage(channel=_DEBUG_CHANNEL, text=msg)
        ts = resp["ts"]

        for msg in _stack_messages():
            slack.chat_postMessage(channel=_DEBUG_CHANNEL, thread_ts=ts, text=msg)

    except SlackApiError as e:
        print(f"DEBUG ERROR: {e}")


def _stack_messages() -> list[str]:
    msgs = []
    for file, line, func, text in traceback.extract_stack():
        # Log only frame summaries relating to this project, up to this function.
        if "/ak-user-" not in file:
            continue

        # Display shorter and cleaner paths.
        file = re.sub(r"^.+/ak-user-.+?/", "", file)
        msgs.append(f"```File: {file}, line {line}\nFunc: {func}\n{text}```")

    return msgs[:-2]  # Skip the last 2 frames (i.e. this module).
