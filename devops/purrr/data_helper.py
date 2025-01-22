"""Thin wrapper over the Google Sheets API for data management and caching.

Redis/Valkey would be a better choice, but are not available at this time.
"""

from datetime import datetime


# Some read functions wait up to 5 seconds for data to exist,
# because GitHub events are asynchronous. For example: when a
# PR review is submitted with file/line comments, some "child"
# comment events may arrive before the "parent" review event.
_GET_TIMEOUT = 5

# Cache user lookup results for a day, to reduce the amount
# of API calls (especially to Slack), to avoid throttling.
_USER_CACHE_TTL = "24h"


def cache_github_reference(slack_user_id: str, github_ref: str) -> None:
    """Map a Slack user ID to a GitHub user reference/name, for a day.

    This helps reduce the amount of lookup API calls, to avoid throttling.
    """
    return  # TODO: Implement this function.


def cached_github_reference(slack_user_id: str) -> str:
    """Return the GitHub user reference/name mapped to a Slack user ID, or "".

    This helps reduce the amount of lookup API calls, to avoid throttling.
    """
    return ""  # TODO: Implement this function.


def cache_slack_user_id(github_username: str, slack_user_id: str) -> None:
    """Map a GitHub username to a Slack user ID, for a day.

    This helps reduce the amount of Slack lookup API calls, to avoid throttling.
    """
    return  # TODO: Implement this function.


def cached_slack_user_id(github_username: str) -> str:
    """Return the Slack user ID mapped to a GitHub user, or "" if not cached yet.

    This helps reduce the amount of Slack lookup API calls, to avoid throttling.
    """
    return ""  # TODO: Implement this function.


def lookup_github_link_details(github_link: str) -> str | None:
    """Return the Slack message thread timestamp mapped to a GitHub PR link, or None.

    This function waits up to a few seconds for the mapping to exist, because
    GitHub events are asynchronous. For example: when a PR review is submitted
    with file/line comments, some "child" comment events may arrive before the
    "parent" review event.
    """
    if not github_link:
        return None

    return None  # TODO: Implement this function (with "wait=True").


def slack_opt_in(user_id: str) -> None:
    """Delete the opt-out timestamp for a Slack user."""
    return  # TODO: Implement this function.


def slack_opt_out(user_id: str) -> None:
    """Return the opt-out timestamp for a Slack user, or None if they're opted-in."""
    return  # TODO: Implement this function.


def slack_opted_out(user_id: str) -> datetime | None:
    """Return the opt-out timestamp for a Slack user, or None if they're opted-in."""
    return None  # TODO: Implement this function.
