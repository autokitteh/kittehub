"""Check the status of a specific room for the next hour."""

from datetime import UTC, datetime, timedelta

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client

import google_sheets


def on_slack_slash_command(event):
    """Entry point for the "/roomstatus <room>" Slack slash command."""
    slack = slack_client("slack_conn")
    channel_id = event.data.channel_id

    room = event.data.text
    if room not in google_sheets.get_room_list():
        error = f"Error: `{room}` not found in the list of rooms"
        slack.chat_postMessage(channel=channel_id, text=error)

    gcal = google_calendar_client("calendar_conn").events()
    now = datetime.now(UTC)
    in_1_hour = now + timedelta(hours=1)

    msg = f"Events in the room `{room}`:"
    try:
        events = gcal.list(
            calendarId=room,
            timeMin=now.isoformat(),
            timeMax=in_1_hour.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        events = events.execute().get("items", [])

        if not events:
            msg += " no upcoming events found"

        for event in events:
            event = autokitteh.AttrDict(event)
            start = event.start.get("dateTime") or event.start.get("date")
            msg += f"\n{start} - {event.summary}"
    except Exception as e:
        msg = f"Error: {e}"
        print(msg)

    slack.chat_postMessage(channel=channel_id, text=msg)
