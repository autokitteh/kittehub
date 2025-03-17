"""Handler for manual runs with a simple loop."""

import time


FIVE_SECONDS = 5
ITERATIONS = 5


def on_manual_run(_):
    for i in range(ITERATIONS):
        print(f"Loop iteration: {i + 1} of {ITERATIONS}")
        time.sleep(FIVE_SECONDS)
