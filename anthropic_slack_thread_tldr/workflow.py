"""Workflow to summarize Slack threads using Anthropic's API."""

from os import getenv

from autokitteh.anthropic import anthropic_client
from autokitteh.slack import slack_client


_CMD = "!tldr"
_MAX_TOKENS = int(getenv("MAX_TOKENS", "1000"))
_MODEL = getenv("MODEL", "claude-3-5-haiku-20241022")

_slack_client = slack_client("slack")
_anthropic = anthropic_client("anthropic")


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
        _slack_client.reactions_add(channel=ch, timestamp=ts, name="thinking_face")

        msgs = _slack_client.conversations_replies(channel=ch, ts=thread_ts).get(
            "messages", []
        )

        msgs = "\n".join(f"- {msg['user']}: {msg['text']}" for msg in msgs)

        message = _anthropic.messages.create(
            max_tokens=_MAX_TOKENS,
            model=_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"""
Compose a summary of the Slack conversation in this thread.
{focus}

Use Slack mentions, for example: <@U12345678>.

These are the messages in the thread:
{msgs}""",
                }
            ],
        )

        summary = "".join(
            block.text for block in message.content if block.type == "text"
        )

        print(summary)

        _slack_client.reactions_remove(channel=ch, timestamp=ts, name="thinking_face")
        _slack_client.reactions_add(channel=ch, timestamp=ts, name="ok_hand")

        _slack_client.chat_postMessage(
            channel=ch,
            thread_ts=thread_ts,
            text=summary,
        )
    except:
        _slack_client.reactions_add(channel=ch, timestamp=ts, name="scream")
        raise
