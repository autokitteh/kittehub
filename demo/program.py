"""This program processes webhook data containing a person's name and email,
gets the name's meaning and a joke from ChatGPT, and sends an email.
"""

import base64
import json
import os

import autokitteh
from autokitteh.google import gmail_client
from autokitteh.openai import openai_client


# Initialize clients
chatgpt = openai_client("chatgpt_conn")
gmail = gmail_client("gmail_conn").users()

# Get sender email from environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


def on_webhook(event):
    """Process incoming webhook data and send an email with name information and a joke.

    Args:
        event: The webhook event containing the JSON payload with name and email.
    """
    try:
        # Extract data from webhook payload
        payload = event.data.body.json

        if not payload or not isinstance(payload, dict):
            print("Error: Invalid payload format")
            return

        name = payload.get("name")
        email = payload.get("email")

        if not name or not email:
            print("Error: Missing required fields (name or email)")
            return

        print(f"Processing request for {name} ({email})")

        # Get name meaning and joke from ChatGPT
        name_info = get_name_info(name)

        # Send email
        send_email(name, email, name_info)

        print(f"Email sent successfully to {email}")

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")


@autokitteh.activity
def get_name_info(name):
    """Get the meaning of a name and a related joke from ChatGPT.

    Args:
        name: The person's name to analyze.

    Returns:
        dict: A dictionary containing the name meaning and a joke.
    """
    prompt = f"""
    Please provide the following information about the name "{name}":
    1. The origin and meaning of the name
    2. A funny, clean joke related to the name

    Format your response as a JSON object with two fields:
    - "meaning": A paragraph about the name's origin and meaning
    - "joke": A funny joke related to the name

    Keep the response concise and friendly.
    """

    response = chatgpt.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that provides information about names and creates friendly jokes.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    # Parse the JSON response
    content = response.choices[0].message.content
    return json.loads(content)


@autokitteh.activity
def send_email(name, recipient_email, name_info):
    """Send an email with the name information and joke.

    Args:
        name: The recipient's name.
        recipient_email: The recipient's email address.
        name_info: Dictionary containing the name meaning and joke.
    """
    # Create email content
    subject = f"The Meaning of Your Name: {name}"

    body = f"""Hello {name},

We thought you might enjoy learning about your name!

MEANING OF YOUR NAME:
{name_info["meaning"]}

AND HERE'S A JOKE JUST FOR YOU:
{name_info["joke"]}

Hope this brightened your day!

Best regards,
The Name Joke Emailer
"""

    # Format email according to RFC 5322
    email_message = f"""From: {SENDER_EMAIL}
To: {recipient_email}
Subject: {subject}

{body}
"""

    # Encode the message
    encoded_message = base64.urlsafe_b64encode(email_message.encode()).decode()

    # Send the email
    gmail.messages().send(userId="me", body={"raw": encoded_message}).execute()
