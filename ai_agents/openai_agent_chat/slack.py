"""Entrypoint when using from AutoKitteh."""

import asyncio

from autokitteh import next_event, subscribe
from autokitteh.slack import slack_client
from chat import chat


_prefix = "!research "

slack = slack_client("slack_conn")


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def on_slack_message(event):
    ts = event.data.ts

    s = subscribe(
        "slack_conn",
        f"data.type == 'message' && data.thread_ts == '{ts}' && data.bot_id == ''",
    )

    q0 = event.data.text.removeprefix(_prefix)
    print(f"Q: {q0}")

    def next_message():
        text = next_event(s).text

        print(f"Q: {text}")

        return text

    def respond(text):
        print(f"A: {text}")

        slack.chat_postMessage(
            channel=event.data.channel,
            thread_ts=ts,
            text=text,
        )

    chat(q0, next_message, respond)
