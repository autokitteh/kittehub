"""Basic handler for incoming HTTP GET requests."""

import time


FIVE_SECONDS = 5


def on_http_get(event):
    print(f"Received {event.data.method} request")

    iterations = int(event.data.params.get("iters", "0"))
    for i in range(iterations):
        print("Loop iteration: %d of 50" % (i + 1))
        time.sleep(FIVE_SECONDS)

    print(f"Finished processing {event.data.method} request")
