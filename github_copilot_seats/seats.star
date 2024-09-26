load("env", "GITHUB_ORG", "IDLE_USAGE_THRESHOLD", "LOGINS", "LOG_CHANNEL")
load("@github", "mygithub")
load("@slack", "myslack")
load("helpers.star", "github_username_to_slack_user_id")
load("msg.json", "blocks")

logins = LOGINS.split(",")

def prune_idle_seats():
    seats = find_idle_seats()
    new_idle_seats = []
    for seat in seats:
        new_idle_seats.append(seat)

        print("new idle: {}".format(seat))
        start("seats.star:engage_seat", {"seat": seat})
    return new_idle_seats

def _get_all_seats():
    # TODO: pagination.
    return mygithub.list_copilot_seats(GITHUB_ORG).seats

def find_idle_seats():
    seats = _get_all_seats()
    idle_usage_threshold = time.parse_duration(IDLE_USAGE_THRESHOLD)

    t, idle_seats = time.now(), []
    for seat in seats:
        if logins and (seat.assignee.login not in logins):
            print("skipping %s" % seat.assignee.login)
            continue

        delta = t - seat.last_activity_at
        is_idle = delta >= idle_usage_threshold

        print("{}: {} - {} = {} {} {}".format(
            seat.assignee.login,
            t,
            seat.last_activity_at,
            delta, 
            ">=" if is_idle else "<",
            idle_usage_threshold,
        ))

        if is_idle:
            idle_seats.append(seat)

    return idle_seats

def engage_seat(seat):
    log = lambda msg: myslack.chat_post_message(LOG_CHANNEL, "{}: {}".format(seat.assignee.login, msg))

    log("engaging")

    github_login = seat.assignee.login
    slack_id = github_username_to_slack_user_id(github_login, GITHUB_ORG)
    if not slack_id:
        print("No slack user found for github user %s" % github_login)
        return

    mygithub.remove_copilot_users(GITHUB_ORG, [github_login])

    myslack.chat_post_message(slack_id, blocks=blocks)

    s = subscribe('myslack', 'data.type == "block_actions" && data.user.id == "{}"'.format(slack_id))

    say = lambda msg: myslack.chat_post_message(slack_id, msg)

    value = next_event(s)["actions"][0].value

    if value == 'ok':
        say("Okey dokey!")
        log("ok")
        return

    if value == 'reinstate':    
        log("reinstate")
        mygithub.add_copilot_users(GITHUB_ORG, [github_login])
        say("You have been reinstated to the Copilot program.")
        return

    log("weird response: {}".format(value))
