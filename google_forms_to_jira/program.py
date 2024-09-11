"""Create Jira issues based on Google Forms responses.

Atlassian Jira API documentation:
- https://docs.autokitteh.com/integrations/atlassian/jira/python

Google Forms API documentation:
- https://docs.autokitteh.com/integrations/google/forms/events
"""

import os

from autokitteh import google
from autokitteh.atlassian import jira_client


JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

jira = jira_client("jira_conn")


def on_form_response(event):
    print("Form response submitted:", event.data)
    response_id = event.data.response.response_id

    forms = google.google_forms_client("forms_conn").forms()
    questions = forms.get(formId=event.data.form_id).execute().get("items", [])

    answers = _summarize_form_response(event.data.response.answers, questions)

    # Check if a Jira issue already exists for this response (i.e. response edited).
    query = f"project = {JIRA_PROJECT_KEY} AND description ~ {response_id}"
    issues = jira.jql(query + " ORDER BY created DESC")
    if issues.get("total", 0) == 0:
        _create_jira_issue(answers, response_id)
    else:
        _update_jira_issue(issues["issues"][0], answers, response_id)


def _summarize_form_response(answers, questions):
    """Extract answers from response, and match with form questions."""
    summary = []
    for i, question in enumerate(questions, start=1):
        question_id = question["questionItem"]["question"]["questionId"]
        title = question.get("title", "Untitled question")

        if question_id not in answers:
            summary.append(f"{i}. {title}:\nNot answered")
        else:
            answer = answers[question_id]["text_answers"]["answers"][0]["value"]
            summary.append(f"{i}. {title}:\n{answer}")

    return summary


def _create_jira_issue(answers, response_id):
    fields = {
        "project": {"key": JIRA_PROJECT_KEY},
        "issuetype": {"name": "Task"},
        "summary": "Response to Google Form",
        "description": "\n\n".join(answers) + f"\n\n(Response ID: {response_id})",
    }
    issue = jira.create_issue(fields=fields)
    print("Created Jira issue:", issue["key"])


def _update_jira_issue(issue, answers, response_id):
    description = "\n\n".join(answers) + f"\n\n(Response ID: {response_id})"
    jira.update_issue_field(issue["key"], fields={"description": description})
    print("Updated Jira issue:", issue["key"])
