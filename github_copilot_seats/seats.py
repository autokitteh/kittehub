import json
import os
from datetime import datetime

import autokitteh
from autokitteh.github import github_client
from autokitteh.slack import slack_client
from helpers import github_username_to_slack_user_id

GITHUB_ORG = os.getenv("GITHUB_ORG")
IDLE_USAGE_THRESHOLD = int(os.getenv("IDLE_USAGE_THRESHOLD"))
LOGINS = os.getenv("LOGINS")
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

logins = LOGINS.split(",")
github = github_client("github_conn")
slack = slack_client("slack_conn")


def prune_idle_seats() -> list:
    """Prunes idle GitHub Copilot users based on their last activity time."""
    seats = find_idle_seats()
    new_idle_seats = []
    for seat in seats:
        new_idle_seats.append(seat)
        autokitteh.start(loc="seats.py:engage_seat", data={"event": {"seat": seat}})
    return new_idle_seats


def find_idle_seats() -> list:
    """Identifies idle GitHub Copilot users based on their last activity time."""
    seats = _get_all_seats()
    t = datetime.now()
    idle_seats = []

    for seat in seats:
        assignee_login = seat["assignee"]["login"]
        last_activity_time = seat["last_activity_at"]

        if logins and assignee_login not in logins:
            print(f"skipping {assignee_login}")
            continue

        delta = t - last_activity_time
        is_idle = delta >= IDLE_USAGE_THRESHOLD

        print(
            f"{assignee_login}: {t} - {last_activity_time} = {delta} "
            f"{'>=' if is_idle else '<'} {IDLE_USAGE_THRESHOLD}"
        )

        if is_idle:
            idle_seats.append(seat)

    return idle_seats


def engage_seat(seat: dict) -> None:
    """Engages a GitHub user assigned to a seat by identifying their corresponding Slack user and initiating a workflow.

    Args:
        seat (dict): Contains details about the assigned GitHub user.
    """
    github_login = seat["assignee"]["login"]

    log(github_login, "engaging")

    slack_id = github_username_to_slack_user_id(github_login, GITHUB_ORG)

    if not slack_id:
        print(f"No slack user found for GitHub user {github_login}")
        return

    _remove_seat(github_login)

    # Loads a predefined message (blocks) from a JSON file and posts it to the user's Slack
    with open("msg.json") as file:
        blocks = json.load(file)
    slack.chat_postMessage(slack_id, blocks=blocks)

    # Subscribes to Slack interaction events, waiting for the user's response
    s = autokitteh.subscribe(
        "slack_conn", f'data.type == "block_actions" && data.user.id == "{slack_id}"'
    )

    # Retrieves the value from the user's response in the Slack event
    value = autokitteh.next_event(s)["actions"][0].value

    # Based on the user's response, it either confirms the action or reinstates the seat
    if value == "ok":
        slack.chat_postMessage(slack_id, "Okey dokey!")
        log(github_login, "ok")
    elif value == "reinstate":
        log(github_login, "reinstate")
        _add_seat(github_login)
        msg = "You have been reinstated to the Copilot program."
        slack.chat_postMessage(slack_id, msg)
    else:
        log(github_login, f"weird response: {value}")


def _add_seat(login: str) -> None:
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/selected_users"
    input_data = {"selected_usernames": [login]}
    github.requester.requestJsonAndCheck("POST", url, input_data=input_data)


def _remove_seat(login: str) -> None:
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/selected_users"
    input_data = {"selected_usernames": [login]}
    github.requester.requestJsonAndCheck("DELETE", url, input_data=input_data)


def _get_all_seats() -> list:
    # TODO: pagination.
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/seats"
    _, data = github.requester.requestJsonAndCheck("GET", url)
    return data["seats"]


def log(github_login: str, msg: str) -> None:
    slack.chat_postMessage(LOG_CHANNEL, f"{github_login}: {msg}")
