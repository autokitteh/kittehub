"""Simple Q&A using AI."""

from os import getenv
from random import randint

from pydantic_ai import Agent

from autokitteh import Event, next_event, subscribe
from autokitteh.slack import slack_client


_slack = slack_client("slack")

_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

roulette_agent = Agent(
    _MODEL_NAME,
    system_prompt=(
        "Be concise, reply with one sentence."
        "\n"
        "Determine if the user wants to play roulette or black-jack based on their "
        "message."
        "\n"
        "If the user wishes to roll the roulette, use the `roulette_wheel` function "
        "to see if the user has won based on the number they provide, which must be "
        "between 1 and 38. Always ask the number the user wants to bet on before "
        "calling the `roulette_wheel` function."
        "\n"
        "If the user wishes to play black-jack, play as the dealer. Deal two cards to "
        "the user and two cards to yourself. Reveal one of your cards. Ask the user if "
        "they want to 'hit' or 'stand'. If they choose 'hit', deal them another card. "
        "If they choose 'stand', reveal your hidden card and play according to "
        "standard black-jack rules (hit until you reach 17 or higher). Determine the "
        "winner based on who has the higher total without going over 21."
        "To draw cards, use the `draw_card` function."
    ),
)


@roulette_agent.tool_plain
async def roulette_wheel() -> int:
    return randint(1, 38)


@roulette_agent.tool_plain
async def draw_card() -> int:
    """Draw a card from a standard deck (1-13)."""
    return randint(1, 13)


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

        result = roulette_agent.run_sync(q, message_history=history)

        history, new = result.all_messages(), result.new_messages()

        a = result.output

        for message in new:
            if hasattr(message, "parts"):
                for part in message.parts:
                    if part.part_kind == "tool-call":
                        print(f"Tool called: {part.tool_name}")
                        print(f"Arguments: {part.args}")
                    elif part.part_kind == "tool-return":
                        print(f"Tool result: {part.content}")

        print(f"A: {a}")

        _slack.chat_postMessage(
            channel=ch,
            thread_ts=ts,
            text=f"`{_MODEL_NAME}` says:\n```{a}```",
        )

        q = next_event(s).text
