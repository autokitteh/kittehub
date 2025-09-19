"""WhatsApp chatbot using Twilio and ChatGPT."""

import os

from tenacity import retry
from tenacity import retry_if_exception
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from twilio.base.exceptions import TwilioRestException

import autokitteh
from autokitteh.openai import openai_client
from autokitteh.twilio import twilio_client


twilio = twilio_client("twilio_conn")
chatgpt = openai_client("chatgpt_conn")


SYSTEM_PROMPT = """You are a helpful WhatsApp chatbot assistant. Respond in a friendly,
        conversational tone.
        Keep your responses concise and helpful since this is a messaging platform.
        Be engaging and personable while providing useful information or assistance."""


# Number from environment variable or default Twilio number.
FROM_NUMBER = os.getenv("FROM_NUMBER", "whatsapp:+14155238886")

CHAT_HIST = {}


def start_chatbot(_):
    """Start WhatsApp chatbot that listens for messages and responds with ChatGPT."""
    print("Starting WhatsApp chatbot - waiting for messages...")
    webhook_sub = autokitteh.subscribe("whatsapp_message")

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
            try:
                if "clear history" in message_body.lower():
                    clear_conversation_history(sender_number)
                    send_whatsapp_message(
                        sender_number, "Conversation history cleared."
                    )
                    continue

                response = generate_chatgpt_response(sender_number, message_body)
                send_whatsapp_message(sender_number, response)
                print(f"Response sent to {sender_number}: {response}")

            except (KeyError, ValueError, AttributeError, TwilioRestException) as e:
                print(f"Error processing message: {e}")
                continue


def generate_chatgpt_response(sender_number, user_message):
    """Generate response using ChatGPT with conversation history."""
    try:
        if sender_number not in CHAT_HIST:
            CHAT_HIST[sender_number] = []

        # Add user message to history.
        CHAT_HIST[sender_number].append({"role": "user", "content": user_message})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
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


def retry_on_rate_limit(exception):
    return "429" in str(exception)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception(retry_on_rate_limit),
    reraise=True,
)
def send_whatsapp_message(to_number, message):
    """Send WhatsApp message via Twilio with retry on rate limits."""
    try:
        result = twilio.messages.create(body=message, from_=FROM_NUMBER, to=to_number)
        print(f"Message sent with SID: {result.sid}")
        return result.sid
    except Exception as e:
        print(f"Failed to send message: {e}")
        print("retrying to send message...")
        raise


def clear_conversation_history(sender_number):
    """Clear conversation history for a specific user."""
    if sender_number in CHAT_HIST:
        del CHAT_HIST[sender_number]
        print(f"Cleared conversation history for {sender_number}")
