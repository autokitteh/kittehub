"""This program demonstrates AutoKitteh's OpenAI ChatGPT integration.

This program implements a single entry-point function, which is
configured in the "autokitteh.yaml" manifest file as the receiver
of Slack "slash_command" events.

It sends a couple of requests to the ChatGPT API, and sends the responses
back to the user over Slack, as well as ChatGPT token usage stats.

API details:
- OpenAI developer platform: https://platform.openai.com/
- Go client API: https://pkg.go.dev/github.com/sashabaranov/go-openai

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.

"""

from autokitteh import openai, slack

MODEL = "gpt-4o-mini"

chatgpt_client = openai.openai_client("chatgpt_conn")
slack_client = slack.slack_client("slack_conn")


def on_slack_slash_command(event):
    """https://api.slack.com/interactivity/slash-commands

    To use the slash command, simply type `/command-name` in the Slack message input,
    where `command-name` is the name you have assigned to the command in your app.
    This command does not require any additional text or arguments.

    Args:
        event: Slack event data.
    """

    # Example 1: trivial interaction with ChatGPT.
    msg = {"role": "user", "content": "Meow!"}
    resp = chatgpt_client.chat.completions.create(model=MODEL, messages=[msg])

    # For educational and debugging purposes, print ChatGPT's response
    # in the AutoKitteh session's log.
    print(resp)

    # Example 2: more verbose interaction with ChatGPT,
    # including the user's text as part of the conversation.
    contents = [
        "You are a poetic assistant, skilled in explaining complex engineering concepts.",
        "Compose a Shakespearean sonnet about the importance of reliability, scalability, and durability, in distributed workflows.",
    ]
    msgs = [
        {"role": "system", "content": contents[0]},
        {"role": "user", "content": contents[1]},
        {"role": "user", "content": event.data["text"]},
    ]

    resp = chatgpt_client.chat.completions.create(model=MODEL, messages=msgs)

    id = event.data["user_id"]
    for choice in resp.choices:
        slack_client.chat_postMessage(channel=id, text=choice.message.content)
    slack_client.chat_postMessage(channel=id, text=f"Usage: `{str(resp.usage)}`")
