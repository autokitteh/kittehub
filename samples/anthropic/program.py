"""This program demonstrates AutoKitteh's Anthropic Claude integration.

The program implements two entry-point functions:
- one that requires a custom prompt in the HTTP request body
- one that uses a default prompt for quick demos

Both functions are configured in the "autokitteh.yaml" manifest file.
They send requests to the Claude API and print the responses
in the AutoKitteh session log, along with Claude's usage statistics.

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

from autokitteh.anthropic import anthropic_client


MODEL = "claude-3-5-haiku-20241022"

claude = anthropic_client("anthropic_conn")


def on_http_post_with_prompt(event):
    """Entry-point function for handling HTTP POST requests with a custom prompt.

    This function requires a text prompt in the request body.

    Example usage:
    - URL: "http://localhost:9980/webhooks/<webhook_slug>"
    - Curl command:
      curl -X POST "<URL>" -H "Content-Type: text/plain" -d "Why do cats purr?"

    Args:
        event: The HTTP event containing request data.
    """
    body = event.data.body.bytes.decode("utf-8")

    # Send the user's prompt to Claude with system instructions.
    message = claude.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=(
            "You are a helpful coding assistant who explains complex "
            "programming concepts clearly and concisely."
        ),
        messages=[
            {
                "role": "user",
                "content": body,
            }
        ],
    )

    # Print Claude's response in the AutoKitteh session's log.
    print(f"User prompt: {body}")
    print(f"\nClaude's response: {message.content[0].text}")
    print(f"\nUsage statistics: {message.usage}")


def on_http_get_demo(event):
    """Entry-point function for HTTP GET requests with a default prompt.

    This function doesn't require any input and demonstrates Claude
    with a preset prompt.

    Example usage:
    - URL: "http://localhost:9980/webhooks/<webhook_slug>"
    - Curl command:
      curl -X GET "<URL>"

    Args:
        event: The HTTP event containing request data.
    """
    # Simple interaction with Claude using a default prompt.
    message = claude.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Give me 3 interesting facts about cats.",
            }
        ],
    )

    # Print Claude's response in the AutoKitteh session's log.
    print(f"Claude's response: {message.content[0].text}")
    print(f"\nUsage statistics: {message.usage}")
    print(f"Model: {message.model}")
