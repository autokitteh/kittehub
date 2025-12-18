"""Simple Q&A using AI."""

from os import getenv

from pydantic_ai import Agent

from autokitteh import Event, next_event, subscribe
from autokitteh.slack import slack_client


_slack = slack_client("slack")

_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

agent = Agent(
    _MODEL_NAME,
    instructions="Be concise, reply with one sentence.",
)


def on_slack_message(event: Event) -> None:
    data = event.data
    q = data.text.removeprefix("!chat").strip()

    ch, ts = event.data.channel, event.data.ts

    s = subscribe(
        "slack",
        f"data.type == 'message' && data.bot_id == '' && data.thread_ts == '{ts}'",
    )

    history: list = []

    while True:
        print(f"Q: {q}")

        result = agent.run_sync(q, message_history=history)

        history = result.all_messages()

        a = result.output

        print(f"A: {a}")

        _slack.chat_postMessage(
            channel=ch,
            thread_ts=ts,
            text=f"`{_MODEL_NAME}` says:\n```{a}```",
        )

        q = next_event(s).text
