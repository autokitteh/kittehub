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


def prune_idle_seats():
    seats = find_idle_seats()
    new_idle_seats = []
    for seat in seats:
        new_idle_seats.append(seat)
        autokitteh.start(loc="seats.py:engage_seat", data={"event": {"seat": seat}})
    return new_idle_seats


def find_idle_seats():
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


def engage_seat(seat):
    github_login = seat["assignee"]["login"]

    log(github_login, "engaging")

    slack_id = github_username_to_slack_user_id(github_login, GITHUB_ORG)

    if not slack_id:
        print(f"No slack user found for GitHub user {github_login}")
        return

    _remove_seat(github_login)

    with open("msg.json") as file:
        blocks = json.load(file)
    slack.chat_postMessage(slack_id, blocks=blocks)

    s = autokitteh.subscribe(
        "slack_conn", f'data.type == "block_actions" && data.user.id == "{slack_id}"'
    )

    value = autokitteh.next_event(s)["actions"][0].value

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


def _add_seat(login):
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/selected_users"
    input_data = {"selected_usernames": [login]}
    github.requester.requestJsonAndCheck("POST", url, input_data=input_data)


def _remove_seat(login):
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/selected_users"
    input_data = {"selected_usernames": [login]}
    github.requester.requestJsonAndCheck("DELETE", url, input_data=input_data)


def _get_all_seats():
    # TODO: pagination.
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/copilot/billing/seats"
    _, data = github.requester.requestJsonAndCheck("GET", url)
    return data["seats"]


def log(github_login, msg):
    slack.chat_postMessage(LOG_CHANNEL, f"{github_login}: {msg}")
