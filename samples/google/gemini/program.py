"""Demonstration of AutoKitteh's Gemini integration.

Two entry-point functions are implemented that send requests to the
Gemini API and print the responses in the AutoKitteh session log.
"""

from autokitteh.google import gemini_client


MODEL = "gemini-1.5-flash"

gemini = gemini_client("gemini_conn", model_name=MODEL)


def trivial_interaction(_):
    prompt = "say meow in different languages"
    response = gemini.generate_content(prompt)
    print(response.text)


def interactive_chat(_):
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
