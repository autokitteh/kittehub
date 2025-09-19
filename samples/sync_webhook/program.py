"""A simple workflow that is triggered by a webhook."""

from autokitteh import next_event, subscribe, http_outcome


def on_first(_):
    print("First webhook triggered!")

    s = subscribe("second")
    e = next_event(s)

    print("Second webhook triggered!")

    http_outcome(status_code=200, body=e.body.text)
