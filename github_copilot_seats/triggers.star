load("@slack", "myslack")
load("seats.star", "prune_idle_seats", "find_idle_seats")

def on_schedule():
    print(prune_idle_seats())

def on_slack_app_mention(data):
    parts = data.text.split(" ")
    if len(parts) < 2:
        myslack.chat_post_message(data.channel, "unrecorgnized command", thread_ts=data.ts)
        return

    cmd = parts[1].strip()

    reply = lambda msg: myslack.chat_post_message(data.channel, msg, thread_ts=data.ts)
    logins = lambda seats: [seat.assignee.login for seat in seats]

    if cmd == "prune-idle-copilot-seats":
        seats = prune_idle_seats()
        reply("engaged {} new idle seats: {}".format(len(seats), logins(seats)))
    elif cmd == "find-idle-copilot-seats":
        seats = find_idle_seats()
        reply("found {} idle seats: {}".format(len(seats), logins(seats)))
