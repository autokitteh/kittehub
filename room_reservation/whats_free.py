from datetime import UTC, datetime, timedelta

from autokitteh.google import google_calendar_client
from autokitteh.slack import slack_client

import helpers


# Entry point for the /whatsfree slash command
def on_slack_whatsfree_slash_command(event):
    # user_id = event.data['user_id']
    channel_id = event.data["channel_id"]

    slack = slack_client("slack_conn")

    rooms = helpers.get_room_list()

    gcal = google_calendar_client("calendar_conn").events()
    now = datetime.now(UTC)
    in_30_minutes = now + timedelta(minutes=30)

    available = False

    # Iterate through the list of rooms and notify the user if the room is free in the next 30 minutes
    for room in rooms:
        print(f"Checking events in {room}.")

        try:
            events_result = gcal.list(
                calendarId=room,
                timeMin=now.isoformat(),
                timeMax=in_30_minutes.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])

            if not events:
                slack.chat_postMessage(
                    channel=channel_id, text=f"{room} is free for the next 30 minutes"
                )
                available = True

        except Exception as e:
            # TODO: if room in the list if not found as a resource, send a better message to the user
            slack.chat_postMessage(channel=channel_id, text=f"{e}")
            print(f"Error: {e}")

    if not available:
        slack.chat_postMessage(
            channel=channel_id, text="No free rooms found for the next 30 minutes"
        )
