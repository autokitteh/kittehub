from autokitteh.slack import slack_client
from seats import prune_idle_seats, find_idle_seats

s = slack_client("slack_conn")


def on_schedule() -> None:
    "Entry point for the workflow"
    print(prune_idle_seats())


def on_slack_slash_command(event) -> None:
    "Entry point for the workflow"
    cmd = event.data.text
    cid = event.data.channel_id

    if cmd not in {"prune-idle-copilot-seats", "find-idle-copilot-seats"}:
        s.chat_postMessage(channel=cid, text="Unrecognized command")
        return

    if cmd == "prune-idle-copilot-seats":
        seats = prune_idle_seats()
        msg = f"Engaged {len(seats)} new idle seats: {', '.join(get_logins(seats))}"
        s.chat_postMessage(channel=cid, text=msg)
    elif cmd == "find-idle-copilot-seats":
        seats = find_idle_seats()
        msg = f"Found {len(seats)} idle seats: {', '.join(get_logins(seats))}"
        s.chat_postMessage(channel=cid, text=msg)


def get_logins(seats: list) -> list:
    return [seat["assignee"]["login"] for seat in seats]
