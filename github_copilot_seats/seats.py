"""Manage GitHub Copilot seat assignments within an organization.

It identifies inactive users and prunes their seats,
but allow the users to get them back via Slack.
"""

from datetime import datetime, timedelta, UTC
import json
import os
from pathlib import Path

import autokitteh
from autokitteh.github import github_client
from autokitteh.slack import slack_client

from users import github_username_to_slack_user_id


GITHUB_ORG_NAME = os.getenv("github_conn__target_name", "")
IDLE_HOURS_THRESHOLD = int(os.getenv("IDLE_HOURS_THRESHOLD", "72"))
MANAGED_LOGINS = os.getenv("MANAGED_LOGINS")

github = github_client("github_conn")
org = github.get_organization(GITHUB_ORG_NAME)
copilot = org.get_copilot()

slack = slack_client("slack_conn")


def find_idle_seats(*, prune: bool = False) -> list[dict[str, str]]:
    """Identifies idle GitHub Copilot users based on their last activity time.

    If `prune` is set to `True`, it also cancels their seat assignments and
    interacts with the users asynchronously to confirm this action.
    """
    idle_seats = []
    for seat in copilot.get_seats():
        # If the project is limited to specific org users, ignore the rest.
        managed_logins = MANAGED_LOGINS.split(",") if MANAGED_LOGINS else []
        if managed_logins and seat.assignee.login not in managed_logins:
            print(f"Skipping unmanaged user: {seat.assignee.login}")
            continue

        # Was the assigned seat being used recently?
        now = datetime.now(UTC)
        delta = now - seat.last_activity_at
        is_active = delta < timedelta(hours=IDLE_HOURS_THRESHOLD)

        comparison = "<" if is_active else ">="
        status = f"{seat.assignee.login}: {now} - {seat.last_activity_at} = "
        status += f"{delta} {comparison} {IDLE_HOURS_THRESHOLD} hours"
        print(status)

        if is_active:
            continue

        # Convert the non-serializable "CopilotSeat" object into a simple dictionary.
        simple_seat = {
            "assignee_login": seat.assignee.login,
            "last_activity_at": seat.last_activity_at.isoformat(),
        }
        idle_seats.append(simple_seat)

        # Interact with the user asynchronously in a child workflow.
        if prune:
            autokitteh.start(loc="seats.py:prune_idle_seat", data=simple_seat)

    return idle_seats


def prune_idle_seat(seat: dict[str, str]) -> None:
    """Interacts via Slack with a GitHub user assigned to an idle Copilot seat.

    Note:
        This function is designed to run as a child workflow, by calling:
        autokitteh.start(loc="seats.py:prune_idle_seat", data={...})

    Args:
        seat: Username and last activity timestamp of the GitHub user to which
            the Copilot seat is assigned.
    """
    github_login = seat.data["assignee_login"]
    report(github_login, "removing seat")
    copilot.remove_seats([github_login])

    slack_id = github_username_to_slack_user_id(github_login)
    if not slack_id:
        print(f"No Slack user found for GitHub user {github_login}")
        return

    report(github_login, "notifying user")

    # Load a blocks-based interactive message template
    # from a JSON file and post it to the user's Slack.
    blocks = json.loads(Path("message.json").read_text())["blocks"]
    slack.chat_postMessage(channel=slack_id, blocks=blocks)

    # Subscribe to Slack interaction events, waiting for the user's response.
    filter = f"event_type == 'interaction' && data.user.id == '{slack_id}'"
    subscription = autokitteh.subscribe("slack_conn", filter)

    # Retrieve the value from the user's response in the Slack event.
    value = autokitteh.next_event(subscription)["actions"][0]["value"]

    # The user's response either confirms the action or reinstates the seat.
    match value:
        case "ok":
            report(github_login, "ok")
            msg = "Okey dokey!"
        case "reinstate":
            report(github_login, "reinstate")
            copilot.add_seats([github_login])
            msg = "You have been reinstated to the Copilot program."
        case _:
            report(github_login, f"weird response: {value}")
            msg = f"Response: `{value}` not recognized."

    slack.chat_postMessage(channel=slack_id, text=msg)


def report(github_login: str, msg: str) -> None:
    channel = os.getenv("SLACK_LOG_CHANNEL")
    if channel:
        slack.chat_postMessage(channel=channel, text=f"{github_login}: {msg}")
