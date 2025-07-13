"""WhatsApp chatbot using Twilio and ChatGPT integration."""

import autokitteh
from autokitteh.openai import openai_client
from autokitteh.twilio import twilio_client
from system_prompt import SYSTEM_PROMPT


twilio = twilio_client("twilio_conn")
chatgpt = openai_client("chatgpt_conn")


def handle_whatsapp_message(event):
    """Handle incoming WhatsApp messages and respond with ChatGPT."""
    print("Starting WhatsApp chatbot - waiting for messages...")

    # Subscribe to webhook events
    webhook_sub = autokitteh.subscribe("webhook")

    while True:
        # Wait for next webhook event (WhatsApp message)
        webhook_event = autokitteh.next_event(webhook_sub)

        if webhook_event:
            print(f"Received WhatsApp message: {webhook_event}")

            # Extract message details
            message_body = webhook_event.body.form.get("Body", "")
            sender_number = webhook_event.body.form.get("From", "")

            print(f"Message from {sender_number}: {message_body}")

            # Skip empty messages
            if not message_body.strip():
                print("Empty message received, skipping")
                continue

            try:
                response = generate_chatgpt_response(message_body)

                # Send response back via Twilio
                send_whatsapp_message(sender_number, response)

                print(f"Response sent to {sender_number}: {response}")

            except Exception as e:
                print(f"Error processing message: {e}")
                # Send error message to user
                error_msg = (
                    "Sorry, I'm having trouble processing your message. "
                    "Please try again later."
                )
                send_whatsapp_message(sender_number, error_msg)


@autokitteh.activity
def generate_chatgpt_response(user_message):
    """Generate response using ChatGPT."""
    try:
        response = chatgpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating ChatGPT response: {e}")
        return "I'm sorry, I couldn't process your request right now. Please try again."


def send_whatsapp_message(to_number, message):
    """Send WhatsApp message via Twilio."""
    try:
        from_number = "whatsapp:+14155238886"  # Twilio Sandbox number

        message = twilio.messages.create(body=message, from_=from_number, to=to_number)

        print(f"Message sent with SID: {message.sid}")
        return message.sid

    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        raise
