"""Reserve a specific room for the next half hour."""

from datetime import UTC, datetime, timedelta

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client

import google_sheets


# event.data['text'] contains the text of the slash command.
def on_slack_slash_command(event):
    """Entry point for the "/reserveroom <room> <title>" Slack slash command."""
    slack = slack_client("slack_conn")

    channel_id = event.data["channel_id"]
    rooms = google_sheets.get_room_list()

    txt = event.data["text"]
    words = txt.split(maxsplit=1)
    if len(words) != 2:
        slack.chat_postMessage(
            channel=channel_id,
            text="Bad input. Please use the following format: /createmeeting <room> <event>",
        )
        return
    if words[0] not in rooms:
        slack.chat_postMessage(channel=channel_id, text=f"Room {words[0]} not found")
        return

    now = datetime.now(UTC)
    in_5_minutes = now + timedelta(minutes=5)
    in_30_minutes = now + timedelta(minutes=30)

    event = {
        "summary": words[1],
        "description": words[1],
        "start": {"dateTime": in_5_minutes.isoformat()},
        "end": {"dateTime": in_30_minutes.isoformat()},
        "reminders": {"useDefault": False},
        # "attendees": [
        #     {"email": "auto@example.com"},
        #     {"email": "kitteh@example.com"},
        # ],
    }
    res = _create_calendar_event(words[0], event)

    slack.chat_postMessage(
        channel=channel_id, text=f"Meeting request to {words[0]} was sent"
    )


# It better to have this as activity to save the creation of multiple activities when creating a insert event
@autokitteh.activity
def _create_calendar_event(calendarId, event):
    gcal = google_calendar_client("calendar_conn").events()
    event = gcal.insert(calendarId=calendarId, body=event).execute()
    return event
