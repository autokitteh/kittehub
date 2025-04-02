"""Main workflow logic."""

from os import getenv

from anthropic import Anthropic
from autokitteh.slack import slack_client


slack_client = slack_client("slack")

anthropic_client = Anthropic(api_key=getenv("ANTHROPIC_API_KEY"))

_MAX_TOKENS = int(getenv("MAX_TOKENS", 1000))
_MODEL = getenv("MODEL", "claude-3-5-haiku-20241022")


def on_slack_thread_message(event):
    """Run the entire interaction with the user."""
    # `ts` is the timestamp of the message that triggered this event.
    # `thread_ts` is the timestamp of the parent message.
    ch, ts, thread_ts = event.data.channel, event.data.ts, event.data.thread_ts

    # give an immediate feedback.
    slack_client.reactions_add(
        channel=ch,
        timestamp=ts,
        name="thinking_face",
    )

    # get the entire thread.
    resp = slack_client.conversations_replies(channel=ch, ts=thread_ts)
    msgs = resp.get("messages", [])

    print(f"in: {len(msgs)} messages")

    # ask claude to summarize the thread.
    message = anthropic_client.messages.create(
        max_tokens=_MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": (
                    "Compose a summary of the Slack conversation in this thread "
                    "using Slack mentions and markdown."
                    "Be concise - just emit bullet points."
                    "Here are the messages in the thread:\n"
                    "\n".join(f"\n- {msg['user']} said: {msg['text']}" for msg in msgs)
                ),
            }
        ],
        model=_MODEL,
    )

    print(f"claude: {message}")

    content = "".join(item.text for item in message.content if item.type == "text")

    print(f"tl;dr: {content}")

    # post the summary.
    slack_client.chat_postMessage(
        channel=ch,
        thread_ts=thread_ts,
        text=f"{content}",
    )

    # remove the thinking_face and add ok_hand, to indicate completion.
    slack_client.reactions_remove(channel=ch, timestamp=ts, name="thinking_face")
    slack_client.reactions_add(channel=ch, timestamp=ts, name="ok_hand")
