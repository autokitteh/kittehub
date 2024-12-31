from autokitteh.slack import slack_client

import seats

s = slack_client("slack_conn")


def on_schedule() -> None:
    print(seats.prune_idle_seats())


def on_slack_slash_command(event) -> None:
    cmd = event.data.text.lower()
    cid = event.data.channel_id
    uid = event.data.user_id

    if cmd == "prune-idle-copilot-seats":
        idle_seats = seats.prune_idle_seats()
        msg = f"Engaged {len(idle_seats)} new idle seats: {', '.join(get_logins(idle_seats))}"
        s.chat_postEphemeral(channel=cid, user=uid, text=msg)
    elif cmd == "find-idle-copilot-seats":
        idle_seats = seats.find_idle_seats()
        msg = f"Found {len(idle_seats)} idle seats: {', '.join(get_logins(idle_seats))}"
        s.chat_postEphemeral(channel=cid, user=uid, text=msg)
    else:
        s.chat_postEphemeral(channel=cid, user=uid, text="Unrecognized command")


def get_logins(seat_list: list) -> list:
    return [seat["assignee"]["login"] for seat in seat_list]
