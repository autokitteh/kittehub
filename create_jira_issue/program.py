"""Create Atlassian Jira issues."""

import json
from urllib.parse import parse_qsl

from autokitteh.atlassian import atlassian_jira_client


def on_http_request(event):
    """Webhook for HTTP GET and POST requests."""
    if event.data.method == "GET":
        create_jira_issue(event.data.url.query)
        return

    match event.data.headers.get("Content-Type"):
        case "application/json":
            create_jira_issue(json.loads(event.data.body))
        case "application/x-www-form-urlencoded":
            body = event.data.body.decode("utf-8")
            create_jira_issue(dict(parse_qsl(body)))


def create_jira_issue(fields):
    if isinstance(fields["project"], str):
        fields["project"] = {"key": fields["project"]}
    if isinstance(fields["issuetype"], str):
        fields["issuetype"] = {"name": fields["issuetype"]}

    atlassian_jira_client("jira_connection").issue_create(fields=fields)
