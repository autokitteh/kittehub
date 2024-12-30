from autokitteh.github import github_client
from autokitteh.slack import slack_client

github = github_client("github_conn")
slack = slack_client("slack_conn")


def _email_to_slack_user_id(email: str) -> str:
    """Fetch Slack user ID based on email address."""
    resp = slack.users_lookupByEmail(email=email)
    return resp["user"]["id"] if resp.get("ok", False) else None


def github_username_to_slack_user_id(username: str, owner_org: str) -> str:
    """Map a GitHub username to a Slack user ID."""
    resp = github.get_user(username)

    if resp.type == "Bot":
        return None

    # Match by email address first.
    if resp.email:
        slack_user_id = _email_to_slack_user_id(resp.email)
        if slack_user_id:
            return slack_user_id

    # Match by the user's full name if email doesn't work.
    gh_full_name = resp.name.lower() if resp.name else None
    if not gh_full_name:
        return None

    slack_users = _slack_users()

    # Normalize the names for comparison.
    for user in slack_users:
        real_name = user.profile.real_name.lower()
        normalized_name = user.profile.real_name_normalized.lower()

        if gh_full_name in (real_name, normalized_name):
            return user.id

    return None


def _slack_users(cursor="") -> list:
    """Retrieve all Slack users, handling pagination."""
    resp = slack.users_list(cursor, limit=100)
    if not resp.get("ok", False):
        return []

    users = resp["members"]
    next_cursor = resp.get("response_metadata", {}).get("next_cursor")
    return users + _slack_users(next_cursor) if next_cursor else users
