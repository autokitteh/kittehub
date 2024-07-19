"""This program polls a Google Form for new responses and creates a Jira issue for each new response.

Workflow:
1. Trigger: HTTP GET request.
2. Poll Forms: Poll the Google Form for new responses.
3. Create Jira Issue: For each new response, create a Jira issue with the response data.
"""

import json
import os
import time

import autokitteh
from autokitteh import google
from autokitteh.atlassian import atlassian_jira_client


POLL_INTERVAL = os.getenv("POLL_INTERVAL")


def on_http_get(event):
    form_id = os.getenv("FORM_ID")
    form_data = _get_form_data(form_id)
    total_responses = None
    while True:
        total_responses = _poll_forms(form_data, form_id, total_responses)
        time.sleep(float(POLL_INTERVAL))


@autokitteh.activity
def _poll_forms(form_data, form_id, prev_total):
    google_forms = google.google_forms_client("google_forms_connection")
    result = google_forms.forms().responses().list(formId=form_id).execute()
    responses = result.get("responses", [])
    curr_total = len(responses)
    if prev_total and curr_total > prev_total:
        new_responses = curr_total - prev_total
        for response in responses[-new_responses:]:
            _create_jira_issue(form_data["info"]["title"], response)
    return curr_total


def _create_jira_issue(title, response):
    jira = atlassian_jira_client("jira_connection")
    answers = json.dumps(response["answers"], indent=2)
    fields = {
        "project": {"key": os.getenv("JIRA_PROJECT_KEY")},
        "summary": "New Google Form Response for form: " + title,
        "description": f"{{code:|language=python}} {answers} {{code}}",
        "issuetype": {"name": "Task"},
    }
    new_issue = jira.create_issue(fields=fields)
    print(f"Created Jira issue: {new_issue["key"]}")


@autokitteh.activity
def _get_form_data(form_id):
    google_forms = google.google_forms_client("google_forms_connection")
    return google_forms.forms().get(formId=form_id).execute()
