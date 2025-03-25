"""Simple workflow that sends a message to Slack."""

import os

from autokitteh.slack import slack_client


CHANNEL = os.getenv("CHANNEL")


def on_manual_run(_):
    slack_client("slack_conn").chat_postMessage(
        channel=CHANNEL,
        text="Meow, world!",
    )
