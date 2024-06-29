"""
This program listens for Jira events and creates a Google Calendar event.

Scenario:
    Before completing a feature, a developer is blocked and needs to discuss
    something with the team.

Workflow:
    The developer creates a new Jira ticket for the discussion. AutoKitteh
    automatically generates a Google Calendar event with a deadline for the
    completion, ensuring that the review happens promptly.
"""

from datetime import datetime, timedelta
import os

import autokitteh
from autokitteh.google import google_calendar_client
from autokitteh.atlassian import get_url


def on_jira_issue_created(event):
    """Workflow's entry-point, triggered by an incoming Jira event."""

    _create_calendar_event(event.data.issue.fields, event.data.issue.key)


@autokitteh.activity
def _create_calendar_event(issue, key):
    start_time = datetime.strptime(issue.duedate, "%Y-%m-%d")
    end_time = start_time + timedelta(minutes=30)
    url = get_base_url(os.getenv("JIRA_CONNECTION_NAME"))
    link = f"Link to Jira Issue: {url}/browse/{key}\n\n"

    event = {
        "summary": issue.summary,
        "description": link + issue.description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Los_Angeles",
        },
        "attendees": [
            {"email": "auto@example.com"},
            {"email": "kitteh@example.com"},
        ],
        "reminders": {
            "useDefault": True,
        },
    }

    cal = google_calendar_client(os.getenv("CALENDAR_CONNECTION_NAME"))
    event = cal.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s" % (event.get("htmlLink")))
