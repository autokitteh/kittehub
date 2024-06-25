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
from autokitteh.google import google_calendar_client

def on_jira_issue_created(data):
    issue = data["data"]["issue"]
    issue_details = extract_issue_details(issue)
    # TODO: connect to Google calendar
    cal = google_calendar_client("my_google_calendar")


def extract_issue_details(issue):
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
