"""User-related helper functions across GitHub and Slack."""

from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError

import debug
import data_helper
import github_helper


github = github_helper.shared_client
slack = slack_client("slack_conn")


def _email_to_slack_user_id(email: str) -> str:
    """Convert an email address to a Slack user ID.

    Args:
        email: Email address.

    Returns:
        Slack user ID, or "" if not found.
    """
    try:
        resp = slack.users_lookupByEmail(email=email)
        return resp.get("user", {}).get("id", "")
    except SlackApiError as e:
        error = f"Failed to look-up Slack user by email {email}"
        debug.log(f"{error}: `{e.response['error']}`")
        return ""


def github_username_to_slack_user(github_username: str) -> dict | None:
    """Convert a GitHub username into Slack user data.

    Args:
        github_username: GitHub username.

    Returns:
        Slack user data, or None if not found.
    """
    slack_user_id = github_username_to_slack_user_id(github_username)
    if not slack_user_id:
        return None
    try:
        resp = slack.users_info(user=slack_user_id)
        return resp.get("user")
    except SlackApiError as e:
        error = f"Failed to get Slack user info for <@{slack_user_id}>"
        debug.log(f"{error}: `{e.response['error']}`")
        return None


def github_username_to_slack_user_id(github_username: str) -> str:
    """Convert a GitHub username to a Slack user ID.

    This function tries to match the email address first, and then
    falls back to matching the user's full name (case-insensitive).

    This function also caches both successful and failed results for
    a day, to reduce the amount of API calls, especially to Slack.

    Args:
        github_username: GitHub username.

    Returns:
        Slack user ID, or "" if not found.
    """
    # Optimization: if we already have it cached, no need to look it up.
    slack_user_id = data_helper.cached_slack_user_id(github_username)
    if slack_user_id in ("bot", "not found"):
        return ""
    elif slack_user_id:
        return slack_user_id

    user = github.get_user(github_username)
    gh_user_link = f"<{user.html_url}|{github_username}>"

    # Special case: GitHub bots can't have Slack identities.
    if user.type == "Bot":
        data_helper.cache_slack_user_id(github_username, "bot")
        return ""

    # Try to match by the email address first.
    if not user.email:
        debug.log(f"GitHub user {gh_user_link}: email address not found")
    else:
        slack_user_id = _email_to_slack_user_id(user.email)
        if slack_user_id:
            data_helper.cache_slack_user_id(github_username, slack_user_id)
            return slack_user_id

    # Otherwise, try to match by the user's full name.
    github_name = (user.name or "").lower()
    if not github_name:
        debug.log(f"GitHub user {gh_user_link}: full name not found")
        return ""

    for user in _slack_users():
        profile = user.get("profile", {})
        slack_names = (
            profile.get("real_name", "").lower(),
            profile.get("real_name_normalized", "").lower(),
        )
        if github_name in slack_names:
            data_helper.cache_slack_user_id(github_username, user.id)
            return user.id

    # Optimization: cache unsuccessful results too (i.e. external users).
    debug.log(f"GitHub user {gh_user_link}: email & name not found in Slack")
    data_helper.cache_slack_user_id(github_username, "not found")
    return ""


def resolve_github_user(github_user) -> str:
    """Convert a GitHub user to a linkified user reference in Slack.

    Args:
        github_user: GitHub user object.

    Returns:
        Slack user reference, or GitHub profile link.
        Used for mentioning users in Slack messages.
    """
    slack_user_id = github_username_to_slack_user_id(github_user.login)
    if slack_user_id:
        # Mention the user by their Slack ID, if possible.
        return f"<@{slack_user_id}>"
    else:
        # Otherwise, fall-back to their GitHub profile link.
        return f"<{github_user.html_url}|{github_user.login}>"


def _slack_users() -> list[dict]:
    """Return a list of all Slack users in the workspace."""
    users = []
    next_cursor = None
    while next_cursor != "":
        try:
            resp = slack.users_list(cursor=next_cursor, limit=100)
            users += resp.get("members", [])
            next_cursor = resp.get("response_metadata", {}).get("next_cursor", "")
        except SlackApiError as e:
            debug.log(f"Failed to list Slack users: `{e.response['error']}`")
            next_cursor = ""

    return users
