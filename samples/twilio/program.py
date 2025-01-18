"""This program demonstrates AutoKitteh's Twilio integration.

This program implements a single entry-point function triggered by an
HTTP GET request event, as defined in the "autokitteh.yaml" manifest file.

API details:
- Messaging API overview: https://www.twilio.com/docs/messaging/api
- Voice API overview: https://www.twilio.com/docs/voice/api

It also demonstrates using constant values which are set for each
AutoKitteh environment in the "autokitteh.yaml" manifest file.
"""

import os

from autokitteh.twilio import twilio_client


FROM_PHONE_NUMBER = os.getenv("FROM_PHONE_NUMBER")

t = twilio_client("twilio_conn")


def on_http_get(event):
    """Entry-point for workflow.

    This function is triggered by an HTTP GET request event and is used to
    send SMS and WhatsApp messages via Twilio.

    Example usage:
    curl "http://localhost:9980/webhooks/<webhook_slug>?to=+15551234567"

    The phone number to send the message to must be provided in the query
    parameter 'to'. The message will be sent both as an SMS and a WhatsApp
    message to the specified number.

    Args:
        event (object): An event object containing the request data.
    """
    to = event.data["url"]["query"]["to"]

    # Add a '+' if missing
    if not to.startswith("+"):
        to = f"+{to}"

    # Send SMS text via Twilio
    message = t.messages.create(
        from_=FROM_PHONE_NUMBER,
        to=to,
        body="This is an AutoKitteh demo message, meow!",
    )
    print(f"SMS message sent: {message.sid}")

    # Send a WhatsApp message to the same number
    whatsapp_message = t.messages.create(
        from_="whatsapp:" + FROM_PHONE_NUMBER,
        to="whatsapp:" + to,
        body="This is an AutoKitteh demo message, meow!",
    )
    print(f"WhatsApp message sent: {whatsapp_message.sid}")
