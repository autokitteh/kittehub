"""Simple utility function for debugging and reporting errors.

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

    Args:
        msg: Message to post.
    """
    if not _DEBUG_CHANNEL or not msg:
        return

    print("DEBUG:", msg)
    c = _DEBUG_CHANNEL
    try:
        resp = slack.chat_postMessage(channel=c, text=msg)
        ts = resp["ts"]

        for file, line, func, text in traceback.extract_stack():
            # Log only frame summaries relating to this project, up to this function.
            if "/ak-user-" not in file or func == "debug":
                continue
            # Display shorter and cleaner paths.
            file = re.sub(r"^.+/ak-user-.+?/", "", file)
            msg = f"```File: {file}, line {line}\nFunc: {func}\n{text}```"
            slack.chat_postMessage(channel=c, thread_ts=ts, text=msg)

    except SlackApiError as e:
        print(f"DEBUG ERROR: {e}")
