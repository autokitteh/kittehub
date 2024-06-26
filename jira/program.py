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


CALENDAR_CONNECTION_NAME = "my_googlecalendar"
JIRA_CONNECTION_NAME = "my_jira"


def on_jira_issue_created(event):
    """This function is triggered by an incoming Jira event.
    It triggers the AutoKitteh workflow to create a Google Calendar event
    """
    issue = event.data.issue
    details = _extract_issue_details(issue)
    cal = google_calendar_client(CALENDAR_CONNECTION_NAME)
    _create_calendar_event(cal, details)


def _extract_issue_details(issue):
    base_url = os.getenv(JIRA_CONNECTION_NAME + "__BaseURL")
    desc = f"Link to Jira Issue: {base_url}/browse/{issue.key}\n\n"
    issue_details = {
        "description": desc + issue.fields.description,
        "duedate": issue.fields.duedate,
        "summary": issue.fields.summary,
    }
    return issue_details


@autokitteh.activity
def _create_calendar_event(cal, issue_details):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=30)

    event = {
        "summary": issue_details["summary"],
        "description": issue_details["description"],
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

    event = cal.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s" % (event.get("htmlLink")))
