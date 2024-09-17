"""Basic handler for incoming HTTP requests."""

import time


FIVE_SECONDS = 5


def on_http_request(event):
    if not event:
        print("Meow, world!")
        return

    print(f"Received {event.data.method} request")

    iterations = int(event.data.url.query.get("iterations", "0"))
    for i in range(iterations):
        print(f"Loop iteration: {i + 1} of {iterations}")
        time.sleep(FIVE_SECONDS)

    print(f"Finished processing {event.data.method} request")
