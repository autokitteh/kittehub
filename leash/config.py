"""Configuration management for the Leash incident management system.

This module loads and manages configuration settings from environment variables,
including escalation delays, timezone settings, notification preferences, and
integration endpoints.
"""

from datetime import timedelta
from os import getenv
from zoneinfo import ZoneInfo

from autokitteh import get_webhook_url


def _get(key: str, default):
    """Get a configuration value."""
    return type(default)(getenv(key, default))


ESCALATION_DELAY = timedelta(minutes=_get("ESCALATION_DELAY_MINUTES", 15))

REMIND_BEFORE_ONCALL_DURATION = timedelta(
    minutes=_get("REMIND_BEFORE_ONCALL_MINUTES", 10)
)

TZ = ZoneInfo(_get("TZ", "UTC"))

FAIL_ON_NO_ASSIGNEE = _get("FAIL_ON_NO_ASSIGNEE", "1").lower() in (
    "1",
    "true",
    "yes",
)

TS_FORMAT = _get("TS_FORMAT", "%m-%d-%Y %H:%M")

TWILIO_PHONE_NUMBER = _get("TWILIO_PHONE_NUMBER", "")

INCIDENT_DASHBOARD_WEBHOOK_URL = get_webhook_url("incident_dashboard_webhook")
