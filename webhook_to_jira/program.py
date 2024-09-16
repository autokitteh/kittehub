"""Create Jira issues based on HTTP GET/POST requests.

Atlassian Jira API documentation:
- https://docs.autokitteh.com/integrations/atlassian/jira/python

HTTP API documentation:
- https://docs.autokitteh.com/integrations/http/events
"""

from autokitteh.atlassian import jira_client


def on_http_request(event):
    """Webhook for HTTP GET and POST requests."""
    if event.data.method == "GET":
        _create_jira_issue(event.data.url.query)
        return

    match event.data.headers.get("Content-Type"):
        case "application/json":
            json_body = event.data.body.json  # Or: json.loads(event.data.body.bytes)
            _create_jira_issue(json_body)
        case "application/x-www-form-urlencoded":
            form_body = event.data.body.form  # Or: dict(urllib.parse.parse_qsl(body))
            _create_jira_issue(form_body)


def _create_jira_issue(fields):
    if isinstance(fields["project"], str):
        fields["project"] = {"key": fields["project"]}
    if isinstance(fields["issuetype"], str):
        fields["issuetype"] = {"name": fields["issuetype"]}

    issue = jira_client("jira_conn").issue_create(fields=fields)
    print("Created Jira issue:", issue["key"])
