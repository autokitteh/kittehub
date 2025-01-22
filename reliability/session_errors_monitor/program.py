"""Send Slack alerts when AutoKitteh sessions end due to errors.

See the configuration and deployment instructions in the README.md file.
"""

from datetime import datetime, timedelta, UTC
import json
import os
from urllib.parse import urljoin

from autokitteh.slack import slack_client
import requests
from requests import exceptions


API_BASE_URL = os.getenv("AUTOKITTEH_API_BASE_URL", "")
UI_BASE_URL = os.getenv("AUTOKITTEH_UI_BASE_URL", "")
JWT = os.getenv("AUTOKITTEH_AUTH_TOKEN", "")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_NAME_OR_ID", "")

slack = slack_client("slack_conn")


def on_monitor_schedule(_):
    """Triggered at the beginning of every minute, so it covers the previous one."""
    end_time = datetime.now(UTC).replace(second=0, microsecond=0)
    # Remove the unit suffix ("m") and parse as an integer.
    interval = int((os.getenv("TRIGGER_INTERVAL", "1m"))[:-1])
    start_time = end_time - timedelta(minutes=interval)

    count = 0
    for session in reversed(_list_sessions_with_errors()):
        session_updated = datetime.fromisoformat(session["updatedAt"])
        if start_time <= session_updated < end_time:
            count += 1
            _log_error(session)

    print(f"Found {count} sessions with new errors")


def _list_sessions_with_errors():
    url = urljoin(API_BASE_URL, "autokitteh.sessions.v1.SessionsService/List")
    headers = {"Content-Type": "application/json"}
    if JWT:  # Servers in dev mode don't require auth.
        headers["Authorization"] = "Bearer " + JWT

    resp = requests.post(url, headers=headers, json={"stateType": 3}, timeout=10)
    print(f"API call's Round Trip Time: {resp.elapsed}")
    resp.raise_for_status()

    try:
        return resp.json().get("sessions", [])
    except exceptions.JSONDecodeError:
        print(f"Response headers: {resp.headers}")
        print(f"Response text: {resp.text}")
        raise


def _log_error(session):
    data = json.dumps(session, indent=4)
    print(data)

    pid, did = session["projectId"], session["deploymentId"]
    path = f"/projects/{pid}/deployments/{did}/sessions/{session['sessionId']}"
    msg = f"Error in AutoKitteh session: {urljoin(UI_BASE_URL, path)}\n```{data}```"
    slack.chat_postMessage(channel=SLACK_CHANNEL, text=msg)
