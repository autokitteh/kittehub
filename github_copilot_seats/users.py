"""User-related helper functions across GitHub and Slack.

Based on: https://github.com/autokitteh/kittehub/blob/main/purrr/users.py
"""

from autokitteh.github import github_client
from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError


github = github_client("github_conn")
slack = slack_client("slack_conn")


def github_username_to_slack_user_id(github_username: str) -> str:
    """Convert a GitHub username to a Slack user ID, or "" if not found.

    This function tries to match the email address first, and then
    falls back to matching the user's full name (case-insensitive).
    """
    user = github.get_user(github_username)

    # Special case: GitHub bots can't have Slack identities.
    if user.type == "Bot":
        return ""

    # Try to match by the email address first.
    if user.email:
        slack_user_id = _email_to_slack_user_id(user.email)
        if slack_user_id:
            return slack_user_id

    # Otherwise, try to match by the user's full name.
    github_name = (user.name or "").lower()
    if not github_name:
        return ""

    for user in _slack_users():
        profile = user.get("profile", {})
        real_name = profile.get("real_name", "").lower()
        normalized_name = profile.get("real_name_normalized", "").lower()
        if github_name in (real_name, normalized_name):
            return user.get("id", "")

    return ""


def _email_to_slack_user_id(email: str) -> str:
    """Convert an email address to a Slack user ID, or "" if not found."""
    try:
        resp = slack.users_lookupByEmail(email=email)
        return resp.get("user", {}).get("id", "")
    except SlackApiError:
        return ""


def _slack_users() -> list[dict]:
    """Return a list of all Slack users in the workspace."""
    users = []
    next_cursor = None
    while next_cursor != "":
        try:
            resp = slack.users_list(cursor=next_cursor, limit=100)
            users += resp.get("members", [])
            next_cursor = resp.get("response_metadata", {}).get("next_cursor", "")
        except SlackApiError:
            next_cursor = ""

    return users
