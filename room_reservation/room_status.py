"""Check the status of a specific room for the next hour."""

from datetime import UTC, datetime, timedelta

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client
from googleapiclient.errors import HttpError

import google_sheets


def on_slack_slash_command(event):
    """Entry point for the "/roomstatus <room>" Slack slash command."""
    slack = slack_client("slack_conn")
    channel_id = event.data.user_id  # event.data.channel_id

    room = event.data.text
    if room not in google_sheets.get_room_list():
        err = f"Error: `{room}` not found in the list of rooms"
        slack.chat_postMessage(channel=channel_id, text=err)

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
        ).execute()

        events = events.get("items", [])
        # Ignore non-blocking events where the room is marked as "free".
        events = [e for e in events if e.get("transparency", "") != "transparent"]

        if not events:
            msg += " none found for the next half hour"

        for event in events:
            event = autokitteh.AttrDict(event)
            start = event.start.get("dateTime") or event.start.get("date")
            msg += f"\n{start} - {event.summary}"

    except HttpError as e:
        msg += f" error '{e.reason}'"
        print(f"Error when listing events for room `{room}`: {e}")

    slack.chat_postMessage(channel=channel_id, text=msg)
