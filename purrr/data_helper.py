"""Thin wrapper over the Google Sheets API for data management and caching.

Redis/Valkey would be a better choice, but are not available at this time.
"""

from datetime import datetime


# Cache user lookup results for a day, to reduce the amount
# of API calls (especially to Slack), to avoid throttling.
_USER_CACHE_TTL = "24h"


def cache_slack_user_id(github_username: str, slack_user_id: str) -> None:
    """Map a GitHub username to a Slack user ID, for a day.

    This helps reduce the amount of Slack lookup API calls, to avoid throttling.
    """
    return  # TODO: Implement this function.


def cached_slack_user_id(github_username: str) -> str:
    """Return the Slack user ID mapped to a GitHub user, if it's already cached.

    This helps reduce the amount of Slack lookup API calls, to avoid throttling.

    Args:
        github_username: GitHub username to look-up.

    Returns:
        Slack user ID, or "" if not found.
    """
    return ""  # TODO: Implement this function.


def slack_opt_in(user_id: str) -> None:
    """Delete the opt-out timestamp for a Slack user."""
    return  # TODO: Implement this function.


def slack_opt_out(user_id: str) -> None:
    """Return the opt-out timestamp for a Slack user, or None if they're opted-in."""
    return  # TODO: Implement this function.


def slack_opted_out(user_id: str) -> datetime | None:
    """Return the opt-out timestamp for a Slack user, or None if they're opted-in."""
    return None  # TODO: Implement this function.
