"""Slack Conversational Chatbot - Multi-turn conversation using Pydantic AI

This module implements a stateful Slack chatbot that maintains conversation history
across multiple messages in a thread. Uses AutoKitteh's durable workflows to keep
the conversation alive and persistent.

Architecture:
    Slack Message (!chat) → Durable Workflow → Subscribe to Thread →
    Loop: Message → AI Agent (with history) → Reply → Wait for next message

Key Features:
    - Multi-turn conversations with memory
    - Durable workflow (survives server restarts)
    - Thread-based conversation isolation
    - Persistent message history using Pydantic AI
    - Automatic conversation continuation
"""

from os import getenv

from pydantic_ai import Agent

from autokitteh import Event, next_event, subscribe
from autokitteh.slack import slack_client


# Initialize Slack client using AutoKitteh connection
_slack = slack_client("slack")

# AI model configuration - supports any Pydantic AI compatible model
_MODEL_NAME = getenv("MODEL_NAME", "anthropic:claude-sonnet-4-0")

# Create Pydantic AI agent with message history support
# This agent is stateful - maintains conversation context across turns
agent = Agent(
    _MODEL_NAME,
    instructions="Be concise, reply with one sentence.",
)


def on_slack_message(event: Event) -> None:
    """Handle incoming Slack messages starting with !chat command.

    Triggered by Slack messages matching the filter in autokitteh.yaml:
    - Must not be in a thread (thread_ts == '')
    - Must start with '!chat'

    This function starts a durable workflow that:
    1. Processes the initial message
    2. Subscribes to thread replies
    3. Maintains conversation loop indefinitely
    4. Persists message history across interactions

    Args:
        event: AutoKitteh event containing Slack message data

    Workflow:
        - Initial message triggers this function
        - Creates a subscription to the thread
        - Enters infinite loop processing thread messages
        - Each message includes full conversation history
        - Workflow persists even if AutoKitteh server restarts

    Note:
        The workflow runs indefinitely until AutoKitteh session times out
        or is manually terminated.
    """
    data = event.data
    # Remove the !chat command prefix and any leading/trailing whitespace
    q = data.text.removeprefix("!chat").strip()

    # Extract channel and timestamp for thread management
    ch, ts = event.data.channel, event.data.ts

    # Subscribe to all non-bot messages in this specific thread
    # This creates a durable subscription that survives across workflow executions
    s = subscribe(
        "slack",
        f"data.type == 'message' && data.bot_id == '' && data.thread_ts == '{ts}'",
    )

    # Initialize conversation history list
    # Pydantic AI maintains this as a structured message history
    history: list = []

    # Infinite loop for multi-turn conversation
    # This loop is durable - it persists across AutoKitteh restarts
    while True:
        print(f"Q: {q}")

        # Run agent with full conversation history for context
        # Pydantic AI uses this for prompt caching and context maintenance
        result = agent.run_sync(q, message_history=history)

        # Update history with all messages (including tool calls if any)
        history = result.all_messages()

        # Extract the AI's response text
        a = result.output

        print(f"A: {a}")

        # Post response in the thread
        _slack.chat_postMessage(
            channel=ch,
            thread_ts=ts,  # Continues the thread
            text=f"`{_MODEL_NAME}` says:\n```{a}```",
        )

        # Wait for next message in the thread
        # This blocks until a new message arrives, maintaining workflow state
        q = next_event(s).text
