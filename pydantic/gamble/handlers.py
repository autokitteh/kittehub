"""AI-Powered Casino Games - Interactive roulette and blackjack using Pydantic AI tools

This module implements an AI casino dealer that plays roulette and blackjack with users.
The AI uses Pydantic AI's tool calling capabilities to interact with game mechanics,
demonstrating how AI agents can use functions to create interactive experiences.

Architecture:
    Slack Message (!gamble) → Durable Workflow → AI Agent with Tools →
    Loop: Message → Tool Calls (roulette_wheel, draw_card) → Reply → Next Message

Key Features:
    - Multi-game support (roulette and blackjack)
    - AI tool calling for game mechanics
    - Conversation-based gameplay
    - Durable workflow with persistent state
    - Logfire instrumentation for observability
"""

from os import getenv
from random import randint

import logfire
from pydantic_ai import Agent

from autokitteh import Event, next_event, subscribe
from autokitteh.slack import slack_client


# Initialize Slack client using AutoKitteh connection
_slack = slack_client("slack")

# AI model configuration - supports any Pydantic AI compatible model
_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

# Configure Logfire for observability and monitoring
# Logfire tracks AI agent interactions, tool calls, and performance
logfire.configure()
logfire.instrument_pydantic_ai()

# Create AI agent with casino game capabilities
# The agent acts as a dealer for both roulette and blackjack
# It uses tools to interact with game mechanics (wheel spins, card draws)
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
    """Spin the roulette wheel and return the winning number.

    Returns a random number between 1 and 38 (American roulette style).
    The AI agent calls this tool when the user wants to play roulette.

    Returns:
        int: The winning number (1-38)
    """
    return randint(1, 38)


@roulette_agent.tool_plain
async def draw_card() -> int:
    """Draw a card from a standard deck.

    Returns a random card value between 1-13:
    - 1 = Ace (can be 1 or 11 in blackjack)
    - 2-10 = Number cards
    - 11 = Jack
    - 12 = Queen
    - 13 = King

    The AI agent calls this tool when dealing cards in blackjack.

    Returns:
        int: The card value (1-13)
    """
    return randint(1, 13)


def on_slack_message(event: Event) -> None:
    """Handle incoming Slack messages starting with !gamble command.

    Triggered by Slack messages matching the filter in autokitteh.yaml:
    - Must not be in a thread (thread_ts == '')
    - Must start with '!gamble'

    This function starts a durable workflow that:
    1. Processes the initial message
    2. Subscribes to thread replies
    3. Maintains conversation loop with game state
    4. Allows AI to call tools (roulette_wheel, draw_card) as needed
    5. Tracks tool calls via Logfire for observability

    Args:
        event: AutoKitteh event containing Slack message data

    Workflow:
        - User starts game with !gamble
        - AI determines which game to play
        - AI uses tools to interact with game mechanics
        - Conversation continues with game state maintained
        - Tool calls are logged and can be inspected

    Note:
        The workflow runs indefinitely until AutoKitteh session times out.
        Game state is maintained in conversation history.
    """
    data = event.data
    # Remove the !chat command prefix (note: should be !gamble in practice)
    q = data.text.removeprefix("!chat").strip()

    # Extract channel and timestamp for thread management
    ch, ts = event.data.channel, event.data.ts

    # Subscribe to all non-bot messages in this specific thread
    s = subscribe(
        "slack",
        f"data.type == 'message' && data.bot_id == '' && data.thread_ts == '{ts}'",
    )

    # Initialize conversation history list
    # This maintains game state across turns
    history: list = []

    # Infinite loop for multi-turn game interaction
    while True:
        print(f"Q: {q}")

        # Run agent with conversation history
        # The agent may call tools (roulette_wheel, draw_card) during execution
        result = roulette_agent.run_sync(q, message_history=history)

        # Update history and get new messages (including tool calls)
        history, new = result.all_messages(), result.new_messages()

        # Extract the AI's response text
        a = result.output

        # Log tool calls for debugging and monitoring
        # This helps track what game actions the AI is taking
        for message in new:
            if hasattr(message, "parts"):
                for part in message.parts:
                    if part.part_kind == "tool-call":
                        print(f"Tool called: {part.tool_name}")
                        print(f"Arguments: {part.args}")
                    elif part.part_kind == "tool-return":
                        print(f"Tool result: {part.content}")

        print(f"A: {a}")

        # Post response in the thread
        _slack.chat_postMessage(
            channel=ch,
            thread_ts=ts,
            text=f"`{_MODEL_NAME}` says:\n```{a}```",
        )

        # Wait for next message in the thread
        q = next_event(s).text
