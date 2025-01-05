"""This program demonstrates AutoKitteh's 2-way Google Calendar integration.

API documentation:
- https://docs.autokitteh.com/integrations/google/calendar/python
- https://docs.autokitteh.com/integrations/google/calendar/events
"""

from datetime import datetime, UTC

from autokitteh.google import google_calendar_client
from googleapiclient.errors import HttpError


def list_events(event):
    """Get the next 10 events from the primary calendar.

    This is the same as Google's quickstart code sample, but simpler:
    https://github.com/googleworkspace/python-samples/tree/main/calendar
    """
    gcal = google_calendar_client("calendar_conn").events()
    print("Getting the next 10 events")

    try:
        result = gcal.list(
            calendarId="primary",
            timeMin=datetime.now(UTC).isoformat(),
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
    except HttpError as e:
        print(f"An error occurred: {e.reason}")
        return

    events = result.get("items")
    if not events:
        print("No upcoming events found")
        return

    for e in events:
        start = e["start"].get("dateTime") or e["start"].get("date")
        start = datetime.fromisoformat(start)
        print(f"{start} - {e['summary']}")


def on_calendar_event_created(event):
    print("Event created:", event.data)


def on_calendar_event_updated(event):
    print("Event updated:", event.data)


def on_calendar_event_deleted(event):
    print("Event deleted:", event.data)
