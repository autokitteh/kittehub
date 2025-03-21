"""Announce AWS Health events in Slack, based on resource ownership in a Google Sheet.

API documentation:
- https://docs.aws.amazon.com/health/
- https://aws.amazon.com/blogs/mt/tag/aws-health-api/

See the configuration and deployment instructions in the README.md file.
"""

from datetime import datetime, timedelta, UTC
import json
import os

import autokitteh
from autokitteh.aws import boto3_client
from autokitteh.google import google_id, google_sheets_client
from autokitteh.slack import slack_client
from hubspot.crm.contacts.exceptions import ApiException


OWNERSHIP_DATA = os.getenv("GOOGLE_SHEET_URL", "")

slack = slack_client("slack_conn")


def on_schedule(_):
    """Workflow's entry-point, triggered at the beginning of every minute."""
    slack_channels = _read_google_sheet()
    events = _aws_health_events()

    if not events:
        print("No AWS Health events found.")
        return

    events_by_arn = {event["arn"]: event for event in events}
    for entity in _affected_aws_entities(events):
        project = entity.get("tags", {}).get("project")
        if not project:
            print(f"Error: AWS entity without project tag: {entity}")
            continue

        channel = slack_channels.get(project)
        affecting_events = [events_by_arn[arn] for arn in entity["eventArns"]]
        _post_slack_message(project, channel, entity, affecting_events)


@autokitteh.activity
def _read_google_sheet() -> dict[str, str]:
    """Read mapping of project tags to Slack channels from Google Sheet."""
    sheets = google_sheets_client("google_sheets_conn").spreadsheets().values()
    rows = sheets.get(spreadsheetId=google_id(OWNERSHIP_DATA), range="A:B").execute()
    return {row[0].strip(): row[1].strip() for row in rows.get("values", [])}


@autokitteh.activity
def _aws_health_events() -> list[dict]:
    """List all recent AWS Health events.

    This function currently fetches events for a single AWS account:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events.html

    With a bit more code, you can also fetch events for multiple ones:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_events_for_organization.html
    """
    # Remove the unit suffix ("m") and parse as an integer.
    interval = int((os.getenv("TRIGGER_INTERVAL", "1m"))[:-1])
    try:
        end_time = datetime.now(UTC).replace(second=0, microsecond=0)
        start_time = end_time - timedelta(minutes=interval)
        filter = {"lastUpdatedTimes": [{"from": start_time, "to": end_time}]}

        aws = boto3_client("aws_conn", "health")
        resp = aws.describe_events(filter=filter)
        events = resp.get("events", [])

        next_token = resp.get("nextToken")
        while next_token:
            resp = aws.describe_events(filter=filter, nextToken=next_token)
            events += resp.get("events", [])
            next_token = resp.get("nextToken")

        return events

    except ApiException as e:
        print(f"Boto3 error: {e}")
        return []


@autokitteh.activity
def _affected_aws_entities(events: list[dict]) -> list[dict]:
    """List all AWS entities affected by the given AWS Health events.

    API reference:
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health/client/describe_affected_entities.html
    """
    try:
        aws = boto3_client("aws_conn", "health")
        arns = [event["arn"] for event in events]

        filter = {"eventArns": arns}
        # Possible alternative: describe_affected_entities_for_organization.
        resp = aws.describe_affected_entities(filter=filter)
        entities = resp.get("entities", [])

        next_token = resp.get("nextToken")
        while next_token:
            resp = aws.describe_affected_entities(filter=filter, nextToken=next_token)
            entities += resp.get("entities", [])
            next_token = resp.get("nextToken")

        return entities
    except ApiException as e:
        print(f"Boto3 error: {e}")
        return []


def _post_slack_message(
    channel: str, project: str, entity: dict, affecting_events: list[dict]
):
    if not channel:
        print(f"Error: project tag {project!r} not found in {OWNERSHIP_DATA}")

    text = f"This AWS resource:\n```\n{json.dumps(entity, indent=4)}\n```"
    text += "\nis affected by these AWS Health events:"
    for i, event in enumerate(affecting_events, 1):
        text += f"\n{i}.\n```\n{json.dumps(event, indent=4)}\n```"

    print(f"Posting in Slack channel: {channel}")
    slack.chat_postMessage(channel=channel, text=text)
