"""Simple Q&A using AI."""

from os import getenv

from pydantic_ai import Agent

from autokitteh import Event
from autokitteh.slack import slack_client


_slack = slack_client("slack")

_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

agent = Agent(
    _MODEL_NAME,
    instructions="Be concise, reply with one sentence.",
)


def on_slack_message(event: Event) -> None:
    data = event.data
    q = data.text.removeprefix("!ask").strip()

    print(f"Q: {q}")

    a = agent.run_sync(q).output

    print(f"A: {a}")

    _slack.chat_postMessage(
        channel=event.data.channel,
        text=f"`{_MODEL_NAME}` says:\n```{a}```",
        thread_ts=event.data.ts,
    )
