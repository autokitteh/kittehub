"""Send Slack alerts when AutoKitteh doesn't receive certain Jira events in time.

See the configuration and deployment instructions in the README.md file.
"""

from datetime import datetime, timedelta, UTC
import os

import autokitteh
from autokitteh.slack import slack_client


CONN_NAME = os.getenv("CONN_NAME", "")
EVENT_FILTER = os.getenv("EVENT_FILTER", "")
EVENT_DESCRIPTION = os.getenv("EVENT_DESCRIPTION", "")

TIMEOUT_HOURS = int(os.getenv("TIMEOUT_HOURS", "24"))
PING_HOURS = int(os.getenv("PING_HOURS", "1"))

SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_NAME_OR_ID", "")


def on_monitor_trigger(_):
    """Handle an incoming event from a monitored service."""
    start_time = datetime.now(UTC)
    slack = slack_client(CONN_NAME)

    # Wait for the next conformant event from the monitored service.
    sub = autokitteh.subscribe(CONN_NAME, filter=EVENT_FILTER)
    data = autokitteh.next_event(sub, timeout=timedelta(hours=TIMEOUT_HOURS))
    incident_detected = data is None

    # The monitored service hasn't sent us a conformant event for TIMEOUT_HOURS.
    # Send a Slack alert once every PING_HOURS, until the incident is resolved.
    while data is None:
        description = EVENT_DESCRIPTION or f"`{EVENT_FILTER}` in `{CONN_NAME}`"
        msg = f"Events not received since {start_time} (UTC): {description}"
        slack.chat_postMessage(channel=SLACK_CHANNEL, text=msg)

        data = autokitteh.next_event(sub, timeout=timedelta(hours=PING_HOURS))

    # All clear, the monitored service is sending us events still/again.
    # Note that another "on_monitor_trigger" workflow is starting to run now,
    # in a separate AutoKitteh session, waiting for the next event/incident.
    autokitteh.unsubscribe(sub)
    if incident_detected:
        msg = f":relieved: Event received again now: {description}"
        slack.chat_postMessage(channel=SLACK_CHANNEL, text=msg)
