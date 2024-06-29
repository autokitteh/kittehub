# TODO: Add description
"""This program listens for Jira events and assigns the issue to the on-call engineer."""

from datetime import datetime, timezone
import os

import autokitteh
from autokitteh.atlassian import atlassian_jira_client
from autokitteh.google import google_calendar_client

# TODO: move all of these constants to .yaml
CALENDAR_CONNECTION_NAME = "my_google_calendar"
JIRA_CONNECTION_NAME = "my_jira"

CALENDAR_ID = "c_38efc2d1983148b0dab1ec069d9bb430419eee9bf30ec43d320d483de2a385e4@group.calendar.google.com"


def on_jira_issue_created(event):
    """Workflow's entry-point, triggered by an incoming Jira event."""
    id = _get_oncall_id()

    # Update issue field
    jira = atlassian_jira_client(JIRA_CONNECTION_NAME)
    fields = {"assignee": {"accountId": id}}
    jira.update_issue_field(event.data.issue.key, fields, notify_users=True)


@autokitteh.activity
def _get_oncall_id():
    cal = google_calendar_client(CALENDAR_CONNECTION_NAME)
    event = (
        cal.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=datetime.now(timezone.utc).isoformat(),
            maxResults=1,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])[0]
        .strip()  # Calendar returns description with whitespace at the front.
    )
    return event["description"]
