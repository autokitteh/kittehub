"""This program demonstrates AutoKitteh's runtime event handling."""

import autokitteh


def on_http_get_meow(event):
    """This workflow is triggered by a predefined HTTP GET request event."""
    print("Got a meow, waiting for a woof")

    # Wait (up to 60 seconds) for a subsequent webhook
    # event where the URL path ends with "woof".
    filter = "data.url.path.endsWith('/woof')"
    sub = autokitteh.subscribe("meow_webhook", filter)
    next = autokitteh.next_event(sub, timeout=60)

    if next:
        print("Got a woof: ", next)
    else:
        print("Timeout!")
