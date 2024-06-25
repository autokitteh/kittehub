"""
Code Review Request:

Scenario: 
    A developer completes a feature and needs a code review.
Workflow: 
    The developer creates a new Jira ticket for the code review. 
    AutoKitteh automatically generates a Google Calendar event with a 
    deadline for the review completion, ensuring that the review happens
    promptly.
"""

from datetime import datetime, timedelta

import autokitteh
from autokitteh.google import google_calendar_client


def on_jira_issue_created(data):
    issue = data["data"]["issue"]
    issue_details = _extract_issue_details(issue)
    cal = google_calendar_client("my_googlecalendar")
    _create_calendar_event(cal, issue_details)


def _extract_issue_details(issue):
    jira_domain = "https://autokitteh.atlassian.net"
    issue_key = issue["key"]
    issue_details = {
        # TODO: add "assignee"
        "description": issue["fields"]["description"],
        "duedate": issue["fields"]["duedate"],
        "link": f"{jira_domain}/browse/{issue_key}",
        # TODO: add "reporter"
        "summary": issue["fields"]["summary"],
    }
    return issue_details


@autokitteh.activity
def _create_calendar_event(cal, issue_details):
    now = datetime.now()
    # start_time = now.isoformat()
    # end_time = (now + timedelta(hours=2, minutes=30)).isoformat()
    # Calculate start time (2 hours from now)
    start_time = now.replace(hour=(now.hour + 2) % 24)

    # Calculate end time (30 minutes after start time)
    end_minute = start_time.minute + 30
    end_hour = start_time.hour

    if end_minute >= 60:
        end_minute -= 60
        end_hour = (end_hour + 1) % 24

    end_time = start_time.replace(hour=end_hour, minute=end_minute)

    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": start_time_iso,
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": end_time_iso,
            "timeZone": "America/Los_Angeles",
        },
        "attendees": [
            {"email": "lpage@example.com"},
            {"email": "sbrin@example.com"},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    event = cal.events().insert(calendarId="primary", body=event).execute()
    print("Event created: %s" % (event.get("htmlLink")))
