"""Utility functions for date and time formatting.

This module provides helper functions for working with datetime objects,
including formatting and parsing timestamps according to the configured
timezone and format settings.
"""

from datetime import datetime

import config


def format_ts(t: datetime) -> str:
    """Return a nice ISO format string for a datetime."""
    return t.strftime(config.TS_FORMAT)


def parse_ts(s: str) -> datetime:
    """Parse a datetime from a string in the configured timezone."""
    dt = datetime.strptime(s.replace("/", "-"), config.TS_FORMAT)  # noqa: DTZ007
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=config.TZ)
    return dt
