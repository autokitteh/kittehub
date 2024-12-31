import json
import os
from datetime import datetime, timezone, timedelta
from typing import Any
import autokitteh
from autokitteh.github import github_client
from autokitteh.slack import slack_client
from helpers import github_username_to_slack_user_id


GITHUB_ORG = os.getenv("GITHUB_ORG")
IDLE_USAGE_THRESHOLD = int(os.getenv("IDLE_USAGE_THRESHOLD"))
LOGINS = os.getenv("LOGINS")
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

logins = LOGINS.split(",") if LOGINS else None
github = github_client("github_conn")
slack = slack_client("slack_conn")

org = github.get_organization(GITHUB_ORG)
copilot = org.get_copilot()


def prune_idle_seats() -> list[dict]:
    """Prunes idle GitHub Copilot users based on their last activity time."""
    seats = find_idle_seats()
    for seat in seats:
        autokitteh.start(loc="seats.py:engage_seat", data=seat)
    return seats


def find_idle_seats() -> list[dict]:
    """Identifies idle GitHub Copilot users based on their last activity time."""
    seats = copilot.get_seats()
    t = datetime.now(timezone.utc)
    idle_seats = []

    for seat in seats:
        if logins and seat.assignee.login not in logins:
            print(f"skipping {seat.assignee.login}")
            continue

        delta = t - seat.last_activity_at
        is_idle = delta >= timedelta(minutes=IDLE_USAGE_THRESHOLD)

        print(
            f"{seat.assignee.login}: {t} - {seat.last_activity_at} = {delta} "
            f"{'>=' if is_idle else '<'} {IDLE_USAGE_THRESHOLD} minutes"
        )

        if is_idle:
            # Convert CopilotSeat object to a dictionary
            seat_dict = {
                "assignee": {"login": seat.assignee.login},
                "last_activity_at": seat.last_activity_at.isoformat(),
            }
            idle_seats.append(seat_dict)

    return idle_seats


def engage_seat(seat: dict[str, Any]) -> None:
    """Engages a GitHub user assigned to a seat by identifying their corresponding Slack user and initiating a workflow.

    Note:
        This is designed to run as a child workflow using:
        autokitteh.start(loc="seats.py:engage_seat", data={"seat": seat})

    Args:
        seat (dict): Contains details about the assigned GitHub user.
    """
    github_login = seat["assignee"]["login"]

    report(github_login, "engaging")

    slack_id = github_username_to_slack_user_id(github_login, GITHUB_ORG)
    if not slack_id:
        print(f"No slack user found for GitHub user {github_login}")
        return

    copilot.remove_seats([github_login])

    # Loads a predefined message (blocks) from a JSON file and posts it to the user's Slack
    with open("msg.json") as file:
        msg = json.load(file)
    slack.chat_postMessage(channel=slack_id, blocks=msg["blocks"])

    # Subscribes to Slack interaction events, waiting for the user's response
    s = autokitteh.subscribe(
        "slack_conn", f'data.type == "block_actions" && data.user.id == "{slack_id}"'
    )

    # Retrieves the value from the user's response in the Slack event
    value = autokitteh.next_event(s)["actions"][0]["value"]

    # Based on the user's response, it either confirms the action or reinstates the seat
    if value == "ok":
        slack.chat_postMessage(channel=slack_id, text="Okey dokey!")
        report(github_login, "ok")
    elif value == "reinstate":
        report(github_login, "reinstate")
        copilot.add_seats([github_login])
        slack.chat_postMessage(
            channel=slack_id, text="You have been reinstated to the Copilot program."
        )
    else:
        report(github_login, f"weird response: {value}")
        slack.chat_postMessage(
            channel=slack_id, text=f"Response: {value} not recognized."
        )


def report(github_login: str, msg: str) -> None:
    slack.chat_postMessage(channel=LOG_CHANNEL, text=f"{github_login}: {msg}")
