"""Entrypoint when using from AutoKitteh."""

from os import getenv

from autokitteh import next_event, subscribe
from autokitteh.slack import slack_client
from chat import chat


Q_TIMEOUT_SECS = int(getenv("Q_TIMEOUT_SECS", "30"))

_prefix = "!research "

slack = slack_client("slack_conn")


def on_slack_message(event):
    ts = event.data.ts

    s = subscribe(
        "slack_conn",
        f"data.type == 'message' && data.thread_ts == '{ts}' && data.bot_id == ''",
    )

    q0 = event.data.text.removeprefix(_prefix)
    print(f"Q: {q0}")

    def next_message():
        event = next_event(s, timeout=Q_TIMEOUT_SECS)
        if event is None:
            raise EOFError

        print(f"Q: {event.text}")

        return event.text

    def respond(text):
        print(f"A: {text}")

        slack.chat_postMessage(
            channel=event.data.channel,
            thread_ts=ts,
            text=text,
        )

    chat(q0, next_message, respond)
