"""Demonstration of AutoKitteh's Gemini integration.

A single entry-point function is implemented, it sends a couple of requests
to the Gemini API, and prints the responses in the AutoKitteh session log.
"""

from autokitteh.google import gemini_client


MODEL = "gemini-1.5-flash"

gemini = gemini_client("gemini_conn", model_name=MODEL)


def on_http_get(event):
    """Entry-point function for handling HTTP GET requests in this workflow."""
    # Example 1: trivial interaction with Gemini.
    prompt = "say meow in different languages"
    response = gemini.generate_content(prompt)
    print(response.text)

    # Example 2: interactive chat using the Gemini.
    chat = gemini.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {
                "role": "model",
                "parts": "Great to meet you. What would you like to know?",
            },
        ]
    )
    response = chat.send_message("I have 2 cats in my house.")
    print(response.text)
    response = chat.send_message("How many paws are in my house?")
    print(response.text)
