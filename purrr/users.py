"""User-related helper functions across GitHub and Slack."""

from autokitteh.slack import slack_client
from github import GithubException
from github import NamedUser
from slack_sdk.errors import SlackApiError

import data_helper
import debug
import github_helper


gh = github_helper.shared_client
slack = slack_client("slack_conn")


def _email_to_github_user_id(email: str) -> str:
    """Convert an email address to a GitHub user ID, or "" if not found."""
    users = gh.search_users(email + " in:email")
    if users.totalCount == 1:
        return users[0].login
    else:
        error = f"GitHub user search results: {users.totalCount} users"
        debug.log(f"{error} with the email address `{email}`")
        return ""


def _email_to_slack_user_id(email: str) -> str:
    """Convert an email address to a Slack user ID, or "" if not found."""
    try:
        resp = slack.users_lookupByEmail(email=email)
        return resp.get("user", {}).get("id", "")
    except SlackApiError as e:
        error = f"Failed to look-up Slack user by email {email}"
        debug.log(f"{error}: `{e.response['error']}`")
        return ""


def format_github_user_for_slack(github_user) -> str:
    """Convert a GitHub user or team to a linkified reference in Slack.

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
        return f"<{github_user.html_url}|@{github_user.login}>"


def format_slack_user_for_github(slack_user_id: str) -> str:
    """Convert a Slack user ID to a GitHub user reference/name.

    This function also caches both successful and failed results for
    a day, to reduce the amount of API calls, especially to Slack.

    Args:
        slack_user_id: Slack user ID.

    Returns:
        GitHub user reference, or the Slack user's full name, or "Someone".
        Used for mentioning users in GitHub reviews and comments.
    """
    if not slack_user_id:
        debug.log("Required input not found: Slack user ID")
        return "Someone"

    # Optimization: if we already have it cached, no need to look it up.
    github_ref = data_helper.cached_github_reference(slack_user_id)
    if github_ref:
        return github_ref

    user = _slack_user_info(slack_user_id)
    if not user:
        # This is never OK, don't cache it in order to keep retrying.
        return "Someone"

    profile = user.get("profile", {})

    # Special case: Slack apps/bots can't have GitHub identities.
    if user.get("is_bot"):
        bot_name = profile.get("real_name", "Some Slack app")
        data_helper.cache_github_reference(slack_user_id, bot_name)
        return bot_name

    # Try to match by the email address first.
    email = profile.get("email", "")
    if not email:
        debug.log(f"Email address not set for Slack user <@{slack_user_id}>")
    else:
        github_id = _email_to_github_user_id(email)
        if github_id:
            github_ref = "@" + github_id
            data_helper.cache_github_reference(slack_user_id, github_ref)
            return github_ref

    # Otherwise, try to match by the user's full name.
    slack_name = profile.get("real_name", "").lower()
    if not slack_name:
        debug.log(f"Slack user <@{slack_user_id}>: `real_name` not found in profile")
        return "Someone"

    users = []
    for user in _github_users():
        if user.name and user.name.lower() == slack_name:
            users.append(user)

    if len(users) == 1:
        github_ref = "@" + users[0].login
        data_helper.cache_github_reference(slack_user_id, github_ref)
        return github_ref

    # Optimization: cache unsuccessful results too (i.e. external collaborators).
    error = f"Slack user <@{slack_user_id}>: found {len(users)}"
    debug.log(f"{error} GitHub org members with the same full name")
    data_helper.cache_github_reference(slack_user_id, profile["real_name"])

    # If all else fails, return the Slack user's full name.
    return profile["real_name"]


def _github_users() -> list[NamedUser.NamedUser]:
    """Return a list of all GitHub users in the organization."""
    try:
        return list(gh.get_organization(github_helper.ORG_NAME).get_members())
    except GithubException as e:
        error = "Failed to list GitHub members in the organization"
        debug.log(f"{error} `{github_helper.ORG_NAME}`:\n```{e}```")
        return []


def github_pr_participants(pr) -> list[str]:
    """Return all the participants in the given GitHub PR.

    Args:
        pr: GitHub PR data.

    Returns:
        List of usernames (author/reviewers/assignees),
        guaranteed to be sorted and without repetitions.
    """
    usernames = []

    # Author.
    if pr.user.type == "User":
        usernames.append(pr.user.login)

    # Specific reviewers (not teams) + assignees.
    for user in pr.requested_reviewers + pr.assignees:
        if user.type == "User" and user.login not in usernames:
            usernames.append(user.login)

    return sorted(usernames)


def github_username_to_slack_user(github_username: str) -> dict:
    """Convert a GitHub username to Slack user data (empty in case of errors)."""
    slack_user_id = github_username_to_slack_user_id(github_username)
    return _slack_user_info(slack_user_id) if slack_user_id else {}


def github_username_to_slack_user_id(github_username: str) -> str:
    """Convert a GitHub username to a Slack user ID, or "" if not found.

    This function tries to match the email address first, and then
    falls back to matching the user's full name (case-insensitive).

    This function also caches both successful and failed results for
    a day, to reduce the amount of API calls, especially to Slack.
    """
    # Don't even check GitHub teams, only individual users.
    if "/" in github_username:
        return ""

    # Optimization: if we already have it cached, no need to look it up.
    slack_user_id = data_helper.cached_slack_user_id(github_username)
    if slack_user_id in ("bot", "not found"):
        return ""
    elif slack_user_id:
        return slack_user_id

    user = gh.get_user(github_username)
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
        real_name = profile.get("real_name", "").lower()
        normalized_name = profile.get("real_name_normalized", "").lower()
        if github_name in (real_name, normalized_name):
            slack_user_id = user.get("id", "")
            data_helper.cache_slack_user_id(github_username, slack_user_id)
            return slack_user_id

    # Optimization: cache unsuccessful results too (i.e. external users).
    debug.log(f"GitHub user {gh_user_link}: email & name not found in Slack")
    data_helper.cache_slack_user_id(github_username, "not found")
    return ""


def _slack_user_info(slack_user_id: str) -> dict:
    """Return all the details of a Slack user based on their ID."""
    try:
        resp = slack.users_info(user=slack_user_id)
        return resp.get("user", {})
    except SlackApiError as e:
        error = f"Failed to get Slack user info for <@{slack_user_id}>"
        debug.log(f"{error}: `{e.response['error']}`")
        return {}


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
