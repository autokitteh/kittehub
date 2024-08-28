"""List all the available rooms for the next half hour."""

from datetime import UTC, datetime, timedelta

from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client

import google_sheets


def on_slack_slash_command(event):
    """Entry point for the "/availablerooms" Slack slash command."""
    slack = slack_client("slack_conn")
    channel_id = event.data["channel_id"]

    now = datetime.now(UTC)
    in_30_minutes = now + timedelta(minutes=30)
    gcal = google_calendar_client("calendar_conn").events()

    # Iterate over the list of rooms, notify the user about
    # each room which is available in the next half hour.
    available = False
    for room in sorted(google_sheets.get_room_list()):
        print(f"Checking upcoming events in: {room}")
        try:
            events = gcal.list(
                calendarId=room,
                timeMin=now.isoformat(),
                timeMax=in_30_minutes.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            if not events.get("items"):
                msg = f"The room `{room}` is available for the next half hour"
                slack.chat_postMessage(channel=channel_id, text=msg)
                available = True

        except Exception as e:
            # TODO: Send a better error message if room isn't found as a resource.
            slack.chat_postMessage(channel=channel_id, text=f"{e}")
            print(f"Error: {e}")

    if not available:
        msg = "No available rooms found for the next half hour"
        slack.chat_postMessage(channel=channel_id, text=msg)
