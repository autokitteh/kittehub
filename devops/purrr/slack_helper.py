"""Thin layer of logic on top of the Slack API."""

import os

from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError

import data_helper
import debug
import users


# PR channel names in Slack: "<prefix>_<number>_<title>".
_CHANNEL_PREFIX = os.getenv("SLACK_CHANNEL_PREFIX", "_pr")

# Visibility of PR channels in Slack: "public" (default) or "private".
_IS_PRIVATE = os.getenv("SLACK_CHANNEL_VISIBILITY", "")

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
                debug.log(f"{error}: `{e.response['error']}`")
                return ""


def rename_channel(channel_id: str, name: str) -> None:
    """Safely rename a Slack channel.

    If the name is already taken, add a numeric suffix to it.

    Args:
        channel_id: Slack channel ID.
        name: Desired (and valid) name of the channel.
    """
    suffix = 0
    while True:
        suffix += 1
        n = _CHANNEL_PREFIX + "_" + name if suffix == 1 else f"{name}_{suffix}"
        try:
            shared_client.conversations_rename(channel=channel_id, name=n)
            print(f"Renamed Slack channel to {n!r} ({channel_id})")
            return
        except SlackApiError as e:
            if e.response["error"] != "name_taken":
                error = f"Failed to rename Slack channel <#{channel_id}> to `{n}`"
                debug.log(f"{error}: `{e.response['error']}`")
                return


def impersonate_in_message(channel_id: str, github_user, msg: str) -> str:
    """Post a message to a Slack channel, on behalf of a GitHub user.

    Similar functions:
    - impersonate_in_reply
    - mention_in_message
    - mention_in_reply

    Args:
        channel_id: ID of the channel to send the message to.
        github_user: GitHub user object of the impersonated user.
        msg: Message to send.

    Returns:
        Message's thread timestamp, or "" in case of an error.
    """
    return impersonate_in_reply(channel_id, "", github_user, msg)


def impersonate_in_reply(
    channel_id: str, comment_url: str, github_user, msg: str
) -> str:
    """Post a reply to a Slack thread, on behalf of a GitHub user.

    Similar functions:
    - impersonate_in_message
    - mention_in_message
    - mention_in_reply

    Args:
        channel_id: ID of the channel to send the message to.
        comment_url: URL of the GitHub PR comment to reply to.
        github_user: GitHub user object of the impersonated user.
        msg: Message to send.

    Returns:
        Message's thread timestamp, or "" in case of an error.
    """
    # TODO: Is this check needed?
    # if not channel_id:
    #     return ""

    user = users.github_username_to_slack_user(github_user.login)
    if not user:
        return ""

    profile = user.get("profile", {})
    icon = profile.get("image_48")
    name = profile.get("real_name")
    ts = _lookup_message(comment_url)

    try:
        resp = shared_client.chat_postMessage(
            channel=channel_id, text=msg, thread_ts=ts, icon_url=icon, username=name
        )
        return resp["ts"]
    except SlackApiError as e:
        error = f"Failed to post {'reply' if ts else 'message'} "
        error += f"as <@{user['id']}> in <#{channel_id}>"
        debug.log(f"{error}: `{e.response['error']}`")
        return ""


def lookup_channel(pr_url: str, action: str) -> str | None:
    """Return the ID of a Slack channel that represents a GitHub PR.

    This function waits up to a few seconds for the PR's Slack message to exist,
    because GitHub events are asynchronous. For example: when a PR is re/opened,
    some "review_requested" events may arrive before the "opened" event.

    Args:
        pr_url: URL of the GitHub PR.
        action: GitHub PR event action.

    Returns:
        Channel ID, or None if not found.
    """
    channel_id = data_helper.lookup_github_link_details(pr_url)
    if not channel_id:
        debug.log(f"{pr_url} is `{action}`, but its Slack channel ID not found")
    return channel_id


def _lookup_message(comment_url: str) -> str | None:
    """Return the ID (timestamp) of a Slack message that represents a GitHub PR review.

    This function waits up to a few seconds for the PR review's Slack message
    to exist, because GitHub events are asynchronous. For example: when a PR
    review is submitted with file and line comments, some "child" comment
    events may arrive before the "parent" review event.

    Args:
        comment_url: URL of the GitHub PR comment to reply to.

    Returns:
        Message's thread timestamp, or None if not found.
    """
    thread_ts = data_helper.lookup_github_link_details(comment_url)
    if not thread_ts:
        debug.log(f"Slack message mapping for {comment_url} not found")
    return thread_ts


def mention_in_message(channel_id: str, github_user, msg: str) -> str:
    """Post a message to a Slack channel, mentioning a GitHub user.

    Similar functions:
    - impersonate_user_in_message
    - impersonate_user_in_reply
    - mention_user_in_reply

    Args:
        channel_id: ID of the channel to send the message to.
        github_user: GitHub user object of the mentioned user.
        msg: Message to send, containing a single "{}" placeholder.

    Returns:
        Message's thread timestamp, or "" in case of an error.
    """
    return mention_in_reply(channel_id, "", github_user, msg)


def mention_in_reply(channel_id: str, comment_url: str, github_user, msg: str) -> str:
    """Post a reply to a Slack thread, mentioning a GitHub user.

    Similar functions:
    - impersonate_user_in_message
    - impersonate_user_in_reply
    - mention_user_in_message

    Args:
        channel_id: ID of the channel to send the message to.
        comment_url: URL of the GitHub PR comment to reply to.
        github_user: GitHub user object of the mentioned user.
        msg: Message to send, containing a single "{}" placeholder.

    Returns:
        Message's thread timestamp, or "" in case of an error.
    """
    # TODO: Is this check needed?
    # if not channel_id:
    #     return ""

    m = msg.format(users.format_github_user_for_slack(github_user))
    ts = _lookup_message(comment_url)

    try:
        resp = shared_client.chat_postMessage(channel=channel_id, text=m, thread_ts=ts)
        return resp["ts"]
    except SlackApiError as e:
        error = f"Failed to post {'reply' if ts else 'message'} in <#{channel_id}>"
        debug.log(f"{error}: `{e.response['error']}`")
        return ""
