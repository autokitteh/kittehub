"""Simple Q&A using AI."""

from os import getenv
from pathlib import Path

from autokitteh import Event, get_webhook_url, http_outcome, next_event, subscribe
from pydantic_ai import Agent


_CHAT_HTML = Path("chat.html").read_text()

_WEBHOOK_URL = get_webhook_url("ask")

_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")


agent = Agent(
    _MODEL_NAME,
    instructions="Be concise, reply with one sentence.",
)


def on_start(_: Event, session_id: str) -> None:
    http_outcome(
        200,
        body=_CHAT_HTML.replace("{{API_ENDPOINT}}", f"{_WEBHOOK_URL}/{session_id}"),
    )

    s = subscribe("chat", f"data.url.path_suffix == '{session_id}'")

    history: list = []

    while True:
        event = next_event(s, full=True)

        print(f"E: {event}")

        q = event.data.body.text

        print(f"Q: {q}")

        result = agent.run_sync(q, message_history=history)

        history = result.all_messages()

        a = result.output

        print(f"A: {a}")

        http_outcome(200, body=a, event_id=event.event_id)
