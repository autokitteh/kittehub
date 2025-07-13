"""WhatsApp chatbot using Twilio and ChatGPT."""

import os

import autokitteh
from autokitteh.openai import openai_client
from autokitteh.twilio import twilio_client
import system_prompt


twilio = twilio_client("twilio_conn")
chatgpt = openai_client("chatgpt_conn")

# Number from environment variable or default Twilio sandbox number.
FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")

CHAT_HIST = {}


def start_chatbot(_):
    """Start WhatsApp chatbot that listens for messages and responds with ChatGPT."""
    print("Starting WhatsApp chatbot - waiting for messages...")
    webhook_sub = autokitteh.subscribe("webhook")

    while True:
        webhook_event = autokitteh.next_event(webhook_sub)

        if webhook_event:
            message_body = webhook_event.body.form.get("Body", "")
            sender_number = webhook_event.body.form.get("From", "")
            print(f"Message from {sender_number}: {message_body}")

            # Skip empty messages.
            if not message_body.strip():
                print("Empty message received, skipping")
                continue

            if "clear history" in message_body.lower():
                clear_conversation_history(sender_number)
                send_whatsapp_message(sender_number, "Conversation history cleared.")
                continue

            try:
                response = generate_chatgpt_response(sender_number, message_body)
                send_whatsapp_message(sender_number, response)
                print(f"Response sent to {sender_number}: {response}")

            except (KeyError, ValueError, AttributeError) as e:
                print(f"Error processing message: {e}")
                error_msg = (
                    "Sorry, I'm having trouble processing your message. "
                    "Please try again later."
                )
                send_whatsapp_message(sender_number, error_msg)


def generate_chatgpt_response(sender_number, user_message):
    """Generate response using ChatGPT with conversation history."""
    try:
        if sender_number not in CHAT_HIST:
            CHAT_HIST[sender_number] = []

        # Add user message to history.
        CHAT_HIST[sender_number].append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": system_prompt.SYSTEM_PROMPT}]
        messages.extend(CHAT_HIST[sender_number])

        # Limit conversation history to prevent token overflow (keep last 20 messages).
        if len(messages) > 21:
            messages = [messages[0]] + messages[-20:]
            CHAT_HIST[sender_number] = messages[1:]

        print(f"Sending {len(messages)} messages to ChatGPT for {sender_number}")

        response = chatgpt.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )

        ai_response = response.choices[0].message.content.strip()

        CHAT_HIST[sender_number].append({"role": "assistant", "content": ai_response})

        return ai_response

    except (KeyError, ValueError, AttributeError) as e:
        print(f"Error generating ChatGPT response: {e}")
        return "I'm sorry, I couldn't process your request right now. Please try again."


def send_whatsapp_message(to_number, message):
    """Send WhatsApp message via Twilio."""
    try:
        message = twilio.messages.create(body=message, from_=FROM_NUMBER, to=to_number)
        print(f"Message sent with SID: {message.sid}")
        return message.sid
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")
        raise


def clear_conversation_history(sender_number):
    """Clear conversation history for a specific user."""
    if sender_number in CHAT_HIST:
        del CHAT_HIST[sender_number]
        print(f"Cleared conversation history for {sender_number}")
