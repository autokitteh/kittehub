"""List all the available rooms for the next half hour."""

from datetime import datetime, timedelta, UTC

from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client
from googleapiclient.errors import HttpError

import util


def on_slack_slash_command(event):
    """Entry point for the "/<app-name> availablerooms" Slack slash command."""
    slack = slack_client("slack_conn")
    channel_id = event.data.user_id  # event.data.channel_id

    now = datetime.now(UTC)
    in_30_minutes = now + timedelta(minutes=30)
    gcal = google_calendar_client("calendar_conn").events()

    # Iterate over the list of rooms, notify the user about
    # each room which is available in the next half hour.
    available = False
    for room in sorted(util.get_room_list()):
        print(f"Checking upcoming events in: {room}")
        try:
            events = gcal.list(
                calendarId=room,
                timeMin=now.isoformat(),
                timeMax=in_30_minutes.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = events.get("items", [])
            # Ignore non-blocking events where the room is marked as "free".
            events = [e for e in events if e.get("transparency", "") != "transparent"]

            if not events:
                msg = f"The room `{room}` is available for the next half hour"
                slack.chat_postMessage(channel=channel_id, text=msg)
                available = True

        except HttpError as e:
            err = f"Error for the room `{room}`: '{e.reason}'"
            slack.chat_postMessage(channel=channel_id, text=err)
            print(f"Error when listing events for room `{room}`: {e}")

    if not available:
        msg = "No available rooms found for the next half hour"
        slack.chat_postMessage(channel=channel_id, text=msg)
