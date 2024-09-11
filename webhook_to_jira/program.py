"""Create Jira issues based on HTTP GET/POST requests.

Atlassian Jira API documentation:
- https://docs.autokitteh.com/integrations/atlassian/jira/python

HTTP API documentation:
- https://docs.autokitteh.com/integrations/http/events
"""

import json
from urllib.parse import parse_qsl

from autokitteh.atlassian import jira_client


def on_http_request(event):
    """Webhook for HTTP GET and POST requests."""
    if event.data.method == "GET":
        _create_jira_issue(event.data.url.query)
        return

    match event.data.headers.get("Content-Type"):
        case "application/json":
            _create_jira_issue(json.loads(event.data.body))
        case "application/x-www-form-urlencoded":
            body = event.data.body.decode("utf-8")
            _create_jira_issue(dict(parse_qsl(body)))


def _create_jira_issue(fields):
    if isinstance(fields["project"], str):
        fields["project"] = {"key": fields["project"]}
    if isinstance(fields["issuetype"], str):
        fields["issuetype"] = {"name": fields["issuetype"]}

    issue = jira_client("jira_conn").issue_create(fields=fields)
    print("Created Jira issue:", issue["key"])
