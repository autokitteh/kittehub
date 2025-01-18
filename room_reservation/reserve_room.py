"""Reserve a specific room for the next half hour."""

from datetime import datetime, timedelta, UTC

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client
from googleapiclient.errors import HttpError

import util


def on_slack_slash_command(event):
    """Entry point for the "reserveroom <room> <title>" Slack slash command."""
    data = event.data

    slack = slack_client("slack_conn")
    channel_id = data.user_id  # DM the user who sent the command.

    cmd_text = data.text.split(maxsplit=2)

    if len(cmd_text) < 3:
        err = f"Error: use this format: `{data.command} reserveroom <room> <title>`"
        slack.chat_postMessage(channel=channel_id, text=err)
        return
    _, room, title = cmd_text

    room = util.get_email_from_slack_command(room)

    if room not in util.get_room_list():
        err = f"Error: `{room}` not found in the list of rooms"
        slack.chat_postMessage(channel=channel_id, text=err)
        return

    user = slack.users_profile_get(user=data.user_id).get("profile", {})

    now = datetime.now(UTC)
    in_5_minutes = now + timedelta(minutes=5)
    in_30_minutes = now + timedelta(minutes=30)

    event = {
        "summary": title,
        "description": f"Reserved via Slack by {user['real_name']}",
        "start": {"dateTime": in_5_minutes.isoformat()},
        "end": {"dateTime": in_30_minutes.isoformat()},
        "reminders": {"useDefault": False},
        "attendees": [
            {"email": user["email"]},
        ],
    }

    result = _create_calendar_event(room, event)
    slack.chat_postMessage(channel=channel_id, text=result)


# It's better to mark this as a single activity, to minimize the creation of
# multiple overly-granular activities during this Google Calendar API call.
@autokitteh.activity
def _create_calendar_event(room, event):
    try:
        gcal = google_calendar_client("calendar_conn").events()
        gcal.insert(calendarId=room, body=event).execute()
        return f"Scheduled a meeting now in the room `{room}`"
    except HttpError as e:
        return f"Error: failed to schedule a meeting ('{e.reason}')"
