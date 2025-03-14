"""Basic handler for incoming HTTP requests."""

import time


FIVE_SECONDS = 5


def on_manual_run():
    for i in range(10):
        print(f"Loop iteration: {i + 1} of {10}")
        time.sleep(FIVE_SECONDS)
