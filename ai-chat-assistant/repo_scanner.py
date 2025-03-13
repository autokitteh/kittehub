"""Find unanswered GitHub PR comments older than 24 hours.

It tracks processed comments with Google Sheets,
and retrieves user information from Slack.
"""

import datetime
import os

from autokitteh import github, google
from autokitteh.slack import slack_client

import helpers


g = github.github_client("github_conn")
slack = slack_client("slack_conn")
sheets = google.google_sheets_client("sheets_conn")


SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")


def find_unanswered_comments(
    repo_name: str, user: str
) -> list[tuple[str, str, str, str]]:
    """Entrypoint for finding unanswered comments."""
    print("Finding unanswered messages...")
    sheets_data = helpers.get_sheets_data(SHEET_NAME)
    comment_ids_set = set()
    if "values" in sheets_data:
        for row in sheets_data["values"]:
            comment_ids_set.add(int(row[0]))
    return get_github_comments(comment_ids_set, repo_name, user)


def get_github_comments(
    comment_ids_set: set,
    repo_name: str,
    user: str,
) -> list[tuple[str, str, str, str]]:
    """Get all comments from GitHub that haven't been responded to in over 24 hours."""
    repo = g.get_repo(repo_name)
    pulls = repo.get_pulls(state="open")

    user_email = get_email_by_slack_user_id(user)
    github_user_id = get_github_user_id_by_email(user_email)

    unresponded = []

    # Process each pull request.
    for pr in pulls:
        # Combine issue and inline comments.
        issue_comments = list(pr.get_issue_comments())
        inline_comments = list(pr.get_comments())
        for comments, is_inline in [(issue_comments, False), (inline_comments, True)]:
            process_comments(
                comments,
                comment_ids_set,
                unresponded,
                github_user_id,
                is_inline=is_inline,
            )

    return unresponded


def process_comments(
    comments: list,
    comment_ids_set: set,
    unresponded: list,
    github_user_id: str,
    is_inline: bool = False,
):
    """Process either issue comments (PR discussion) or inline review comments."""
    for comment in comments:
        if should_skip_comment(comment, github_user_id):
            continue

        if has_been_responded_to(comment, comments, is_inline, github_user_id):
            continue

        if comment.id not in comment_ids_set:
            unresponded.append(
                (comment.id, comment.user.login, comment.body, comment.html_url)
            )
            comment_ids_set.add(comment.id)


def has_been_responded_to(
    target_comment, potential_responses, is_inline, github_user_id
):
    # Skip if comment is less than 24 hours old.
    now = datetime.datetime.now(datetime.UTC)
    if now - target_comment.created_at < datetime.timedelta(hours=24):
        return True

    # Check for emoji reactions.
    for reaction in target_comment.get_reactions():
        if reaction.user.login == github_user_id:
            return True

    # Check for comment responses.
    for response in potential_responses:
        if (
            response.created_at > target_comment.created_at
            and response.user.login == github_user_id
        ):
            if is_inline:
                return True

            # For issue comments, check for @ mentions or quotes.
            if has_mention_or_quote(response, target_comment):
                return True

    return False


def should_skip_comment(comment, github_user_id: str):
    return comment.user.login == github_user_id or github_user_id not in comment.body


def has_mention_or_quote(response, original_comment):
    if "@" + original_comment.user.login in response.body:
        return True

    # Check for quote.
    for line in response.body.splitlines():
        if line.strip().startswith(">") and original_comment.body[:30] in line:
            return True

    return False


def get_email_by_slack_user_id(user_id: str):
    return (
        slack.users_info(user=user_id)
        .get("user", {})
        .get("profile", {})
        .get("email", "")
    )


def get_github_user_id_by_email(email: str):
    return g.search_users(query=email)[0].login
