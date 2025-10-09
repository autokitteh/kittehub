"""Telegram AI Translator Bot with Context Memory

A smart translation bot that uses Gemini AI to provide contextual translations
with cultural nuances and maintains conversation history for better accuracy.
"""

from autokitteh.google import gemini_client
from autokitteh.telegram import telegram_client
from telegram_ai_translator.prompts import DETECT_USAGE
from telegram_ai_translator.prompts import get_detect_prompt
from telegram_ai_translator.prompts import get_translate_prompt
from telegram_ai_translator.prompts import HELP_TEXT
from telegram_ai_translator.prompts import TRANSLATE_USAGE


MODEL = "gemini-2.5-flash-lite"

gemini = gemini_client("gemini_conn", model_name=MODEL)
telegram = telegram_client("telegram_conn")


def on_telegram_message(event):
    """Handle incoming Telegram messages and provide AI-powered translations."""
    message = event.data.message
    chat_id = message.chat.id
    text = message.text

    # Ignore empty messages.
    if not text:
        return

    command = text.split()[0] if text else ""
    match command:
        case "/translate":
            handle_translate_command(text, chat_id)
        case "/detect":
            handle_detect_command(text, chat_id)
        case "/help":
            handle_help_command(chat_id)


def handle_translate_command(text: str, chat_id):
    """Handle /translate command."""
    parts = text.split(maxsplit=2)
    if len(parts) < 3:
        telegram.send_message(chat_id=chat_id, text=TRANSLATE_USAGE)
        return

    target_lang = parts[1]
    text_to_translate = parts[2]
    prompt = get_translate_prompt(target_lang, text_to_translate)

    try:
        response = gemini.generate_content(prompt)
        telegram.send_message(chat_id=chat_id, text=response.text)
    except RuntimeError as e:
        telegram.send_message(chat_id=chat_id, text=f"Translation error: {e!s}")


def handle_detect_command(text: str, chat_id):
    """Handle /detect command."""
    parts = text.split(maxsplit=2)
    if len(parts) < 3:
        telegram.send_message(chat_id=chat_id, text=DETECT_USAGE)
        return

    target_lang = parts[1]
    text_to_translate = parts[2]
    prompt = get_detect_prompt(target_lang, text_to_translate)

    try:
        response = gemini.generate_content(prompt)
        telegram.send_message(chat_id=chat_id, text=response.text)
    except RuntimeError as e:
        telegram.send_message(chat_id=chat_id, text=f"Detection error: {e!s}")


def handle_help_command(chat_id):
    """Handle /help command."""
    telegram.send_message(chat_id=chat_id, text=HELP_TEXT)
