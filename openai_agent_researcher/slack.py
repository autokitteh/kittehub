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
    first = True

    s = subscribe(
        "slack_conn",
        f"data.type == 'message' && data.thread_ts == '{ts}' && data.bot_id == ''",
    )

    def next_message():
        nonlocal first

        if first:
            first = False
            return event.data.text.removeprefix(_prefix)

        return next_event(s).text

    def respond(text):
        slack.chat_postMessage(
            channel=event.data.channel,
            thread_ts=ts,
            text=text,
        )

    chat(next_message, respond)
