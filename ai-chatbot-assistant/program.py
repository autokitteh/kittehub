import autokitteh
from autokitteh import slack


slack_client = slack.slack_client("slack_conn")


# TODO: figure out a trigger for this
def on_start(_):
    while True:
        print("Waiting for a message...")
        subs = [autokitteh.subscribe("slack_conn", "true")]
        # TODO: add a listen for sheets updates
        data = autokitteh.next_event(subs)
        if data:
            print(data)
