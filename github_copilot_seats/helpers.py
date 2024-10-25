from autokitteh.github import github_client
from autokitteh.slack import slack_client

github = github_client("github_conn")
slack = slack_client("slack_conn")


def _email_to_slack_user_id(email):
    """Fetch Slack user ID based on email address."""
    resp = slack.users_lookup_by_email(email)
    return resp.user.id if resp.ok else ""


def github_username_to_slack_user_id(github_username, github_owner_org):
    """Map a GitHub username to a Slack user ID."""
    resp = github.get_user(github_username, owner=github_owner_org)

    if resp.type == "Bot":
        return ""

    # Match by email address first.
    if resp.email:
        slack_user_id = _email_to_slack_user_id(resp.email)
        if slack_user_id:
            return slack_user_id

    # Match by the user's full name if email doesn't work.
    gh_full_name = resp.name.lower() if resp.name else None
    if not gh_full_name:
        return ""

    return next(
        (
            user.id
            for user in _slack_users()
            if gh_full_name
            in (
                user.profile.real_name.lower(),
                user.profile.real_name_normalized.lower(),
            )
        ),
        "",
    )


def _slack_users(cursor=""):
    """Retrieve all Slack users, handling pagination."""
    resp = slack.users_list(cursor, limit=100)
    if not resp.ok:
        return []

    users = resp.members
    next_cursor = resp.response_metadata.next_cursor
    return users + _slack_users(next_cursor) if next_cursor else users
