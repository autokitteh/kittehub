"""Slack Q&A Bot - Simple one-shot question answering using Pydantic AI

This module implements a stateless Slack bot that answers questions using AI.
Each message is treated independently without conversation history.

Architecture:
    Slack Message (!ask) → AutoKitteh Trigger → Pydantic AI Agent → Slack Reply

Key Features:
    - One-shot Q&A (no conversation history)
    - Configurable AI model via environment variable
    - Threaded replies in Slack
    - Synchronous processing
"""

from os import getenv

from pydantic_ai import Agent

from autokitteh import Event
from autokitteh.slack import slack_client


# Initialize Slack client using AutoKitteh connection
_slack = slack_client("slack")

# AI model configuration - supports any Pydantic AI compatible model
# Format: "provider:model-name" (e.g., "anthropic:claude-sonnet-4-0")
_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

# Create Pydantic AI agent with concise response instructions
# This agent is stateless - each run is independent
agent = Agent(
    _MODEL_NAME,
    instructions="Be concise, reply with one sentence.",
)


def on_slack_message(event: Event) -> None:
    """Handle incoming Slack messages starting with !ask command.

    Triggered by Slack messages matching the filter in autokitteh.yaml:
    - Must not be in a thread (thread_ts == '')
    - Must start with '!ask'

    Args:
        event: AutoKitteh event containing Slack message data

    Process:
        1. Extract question text (remove !ask prefix)
        2. Send to Pydantic AI agent for processing
        3. Post response back to Slack in a thread

    Note:
        No conversation history is maintained - each question is independent.
    """
    data = event.data
    # Remove the !ask command prefix and any leading/trailing whitespace
    q = data.text.removeprefix("!ask").strip()

    print(f"Q: {q}")

    # Run agent synchronously - no message history passed
    a = agent.run_sync(q).output

    print(f"A: {a}")

    # Post response in a thread attached to the original message
    _slack.chat_postMessage(
        channel=event.data.channel,
        text=f"`{_MODEL_NAME}` says:\n```{a}```",
        thread_ts=event.data.ts,  # Creates a thread reply
    )
