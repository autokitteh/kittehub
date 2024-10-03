"""This program demonstrates AutoKitteh's OpenAI ChatGPT integration.

The program implements a single entry-point function, which is
configured in the "autokitteh.yaml" manifest file to receive HTTP GET requests.

It sends a couple of requests to the ChatGPT API, and returns the responses
to the user, along with ChatGPT token usage stats.

API details:
- OpenAI developer platform: https://platform.openai.com/
- Python client library: https://github.com/openai/openai-python

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

from autokitteh.openai import openai_client

MODEL = "gpt-4o-mini"

chatgpt_client = openai_client("chatgpt_conn")


def on_http_get(event):
    """Entry-point function for workflow.

    example URL: "http://localhost:9980/webhooks/<webhook_slug>?text=autokittens"

    Args:
        event: HTTP event data (including URL query parameters).
    """
    params = event.data.url.query
    text = params.get("text", "")
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
        {"role": "user", "content": text if text else contents[1]},
    ]

    resp = chatgpt_client.chat.completions.create(model=MODEL, messages=msgs)

    for choice in resp.choices:
        print(choice.message.content)
    print(f"Usage: `{str(resp.usage)}`")
