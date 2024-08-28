"""Reserve a specific room for the next half hour."""

from datetime import UTC, datetime, timedelta

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client

import google_sheets


def on_slack_slash_command(event):
    """Entry point for the "/reserveroom <room> <title>" Slack slash command."""
    slack = slack_client("slack_conn")
    channel_id = event.data.channel_id

    cmd_text = event.data.text.split(maxsplit=1)
    if len(cmd_text) < 2:
        error = "Error: please use the following format: `/reserveroom <room> <title>`"
        slack.chat_postMessage(channel=channel_id, text=error)
        return

    room, title = cmd_text
    if room not in google_sheets.get_room_list():
        error = f"Error: `{room}` not found in the list of rooms"
        slack.chat_postMessage(channel=channel_id, text=error)
        return

    user = event.data.user_id  # TODO: Convert to name.

    now = datetime.now(UTC)
    in_5_minutes = now + timedelta(minutes=5)
    in_30_minutes = now + timedelta(minutes=30)

    event = {
        "summary": title,
        "description": f"Reserved via Slack by {user}",
        "start": {"dateTime": in_5_minutes.isoformat()},
        "end": {"dateTime": in_30_minutes.isoformat()},
        "reminders": {"useDefault": False},
        # TODO: Add the requester.
        # "attendees": [
        #     {"email": "auto@example.com"},
        #     {"email": "kitteh@example.com"},
        # ],
    }

    # TODO: Handle errors.
    _create_calendar_event(room, event)
    slack.chat_postMessage(channel=channel_id, text=f"Scheduled meeting in `{room}`")


# It's better to mark this as a single activity, to minimize the creation of
# multiple overly-granular activities during this Google Calendar API call.
@autokitteh.activity
def _create_calendar_event(room, event):
    gcal = google_calendar_client("calendar_conn").events()
    return gcal.insert(calendarId=room, body=event).execute()
