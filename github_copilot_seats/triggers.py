"""Manage scheduled tasks and Slack commands for idle seat management."""

from autokitteh.slack import slack_client

import seats


def on_schedule() -> None:
    for seat in seats.find_idle_seats(prune=True):
        print(seat)


def on_slack_slash_command(event) -> None:
    find_seats = True
    match event.data.text.lower():
        case "prune-idle-copilot-seats":
            prune = True
        case "find-idle-copilot-seats":
            prune = False
        case _:
            find_seats = False

    if find_seats:
        idle_seats = seats.find_idle_seats(prune=prune)
        action = "Pruned" if prune else "Found"
        msg = f"{action} {len(idle_seats)} idle seats for these users: "
        msg += ", ".join(_get_logins(idle_seats))
    else:
        msg = "Error: unrecognized command"

    slack_client("slack_conn").chat_postEphemeral(
        channel=event.data.channel_id, user=event.data.user_id, text=msg
    )


def _get_logins(idle_seats: list[dict[str, str]]) -> list[str]:
    return [seat["assignee_login"] for seat in idle_seats]
