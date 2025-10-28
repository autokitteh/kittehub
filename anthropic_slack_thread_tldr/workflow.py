"""Workflow to summarize Slack threads using Anthropic's API."""

from os import getenv

from anthropic import Anthropic
from autokitteh.slack import slack_client


_CMD = "!tldr"

slack_client = slack_client("slack")

anthropic_client = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))

_MAX_TOKENS = int(getenv("MAX_TOKENS", 1000))


def on_slack_thread_message(event):
    text = event.data.text.strip()

    if not (text == _CMD or text.startswith(_CMD + " ")):
        print("irrelevant")
        return

    focus, q = "", text[len(_CMD) :].strip()
    if q:
        focus = f"Focus on: {q}"
        print(focus)

    ch, ts, thread_ts = event.data.channel, event.data.ts, event.data.thread_ts

    try:
        slack_client.reactions_add(channel=ch, timestamp=ts, name="thinking_face")

        msgs = slack_client.conversations_replies(channel=ch, ts=thread_ts).get(
            "messages", []
        )

        msgs = "\n".join(f"- {msg['user']}: {msg['text']}" for msg in msgs)

        message = anthropic_client.messages.create(
            max_tokens=_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Compose a summary of the Slack conversation in this thread.
{focus}

Use Slack mentions.

These are the messages in the thread:
{msgs}""",
                }
            ],
            model="claude-3-5-sonnet-latest",
        )

        summary = "".join(
            block.text for block in message.content if block.type == "text"
        )

        print(summary)

        slack_client.reactions_remove(channel=ch, timestamp=ts, name="thinking_face")
        slack_client.reactions_add(channel=ch, timestamp=ts, name="ok_hand")

        slack_client.chat_postMessage(
            channel=ch,
            thread_ts=thread_ts,
            text=summary,
        )
    except:
        slack_client.reactions_add(channel=ch, timestamp=ts, name="scream")
        raise
