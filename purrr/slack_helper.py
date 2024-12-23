"""Thin layer of logic on top of the Slack API."""

import os
import re
import traceback

from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError


_DEBUG_CHANNEL = os.getenv("SLACK_DEBUG_CHANNEL")
# PR channel names in Slack: "<prefix>_<number>_<title>".
_CHANNEL_PREFIX = os.getenv("SLACK_CHANNEL_PREFIX", "_pr")
# Visibility of PR channels in Slack: "public" (default) or "private".
_IS_PRIVATE = os.getenv("SLACK_CHANNEL_VISIBILITY") or ""

shared_client = slack_client("slack_conn")


def create_channel(name: str) -> str:
    """Create a public or private Slack channel.

    If the name is already taken, add a numeric suffix to it.

    Args:
        name: Desired (and valid) name of the channel.

    Returns:
        Channel ID, or an empty string in case of an error.
    """
    is_private = _IS_PRIVATE.lower().strip() == "private"
    visibility = "private" if is_private else "public"
    suffix = 0

    while True:
        suffix += 1
        n = _CHANNEL_PREFIX + "_" + name if suffix == 1 else f"{name}_{suffix}"
        try:
            resp = shared_client.conversations_create(name=n, is_private=is_private)
            channel_id = resp["channel"]["id"]
            print(f"Created {visibility} Slack channel {n!r} ({channel_id})")
            return channel_id
        except SlackApiError as e:
            if e.response["error"] != "name_taken":
                error = f"Failed to create {visibility} Slack channel `{n}`"
                debug(f"{error}: `{e.response["error"]}`")
                return ""


def debug(msg: str) -> None:
    """Post a debug message to a predefined Slack channel, if defined.

    Also post a filtered traceback, as replies to the message.

    Args:
        msg: Message to post.
    """
    if not _DEBUG_CHANNEL or not msg:
        return

    print("DEBUG:", msg)
    c = _DEBUG_CHANNEL
    try:
        resp = shared_client.chat_postMessage(channel=c, text=msg)
        ts = resp["ts"]

        for file, line, func, text in traceback.extract_stack():
            # Log only frame summaries relating to this project, up to this function.
            if "/ak-user-" not in file or func == "debug":
                continue
            # Display shorter and cleaner paths.
            file = re.sub(r'[^"]+/ak-user-.+?/', "", file)
            msg = f"```File: {file}, line {line}\nFunc: {func}\n{text}```"
            shared_client.chat_postMessage(channel=c, thread_ts=ts, text=msg)

    except SlackApiError as e:
        print(f"DEBUG ERROR: {e}")


def normalize_channel_name(name: str) -> str:
    """Convert arbitrary text into a valid Slack channel name.

    Args:
        name: Desired name for a Slack channel.

    Returns:
        Valid Slack channel name.
    """
    if name == "":
        return name

    name = name.lower().strip()
    name = re.sub(r"['\"]", "", name)  # Remove quotes.
    name = re.sub(r"[^a-z0-9_-]", "-", name)  # Replace invalid characters.
    name = re.sub(r"[_-]{2,}", "-", name)  # Remove repeating separators.

    # Slack channel names are limited to 80 characters, but that's
    # too long for comfort, so we use 50 instead. Plus, we need to
    # leave room for a PR number prefix and a uniqueness suffix.
    name = name[:50]

    # Cosmetic tweak: remove leading and trailing hyphens.
    if name[0] == "-":
        name = name[1:]
    if name[-1] == "-":
        name = name[:-1]

    return name
