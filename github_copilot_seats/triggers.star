load("@slack", "myslack")
load("seats.star", "prune_idle_seats", "find_idle_seats")

def on_schedule():
    print(prune_idle_seats())

def on_slack_slash_command(data):
    cmd = data.text
    if cmd not in ["prune-idle-copilot-seats", "find-idle-copilot-seats"]:
        myslack.chat_post_message(data.channel_id, "unrecognized command")
        return


    reply = lambda msg: myslack.chat_post_message(data.channel_id, msg)
    logins = lambda seats: [seat.assignee.login for seat in seats]

    if cmd == "prune-idle-copilot-seats":
        seats = prune_idle_seats()
        reply("engaged {} new idle seats: {}".format(len(seats), logins(seats)))
    elif cmd == "find-idle-copilot-seats":
        seats = find_idle_seats()
        reply("found {} idle seats: {}".format(len(seats), logins(seats)))
