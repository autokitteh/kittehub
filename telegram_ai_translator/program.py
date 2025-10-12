"""Telegram AI Translator Bot

A smart translation bot that uses Gemini AI to provide contextual translations
with cultural nuances.
"""

import asyncio

from autokitteh.google import gemini_client
from autokitteh.telegram import telegram_client

from prompts import DETECT_USAGE
from prompts import get_detect_prompt
from prompts import get_translate_prompt
from prompts import HELP_TEXT
from prompts import TRANSLATE_USAGE


gemini = gemini_client("gemini_conn", model_name="gemini-2.5-flash-lite")
telegram = telegram_client("telegram_conn")


def on_message_trigger(event):
    """Entry point for handling incoming messages.

    Note: AutoKitteh triggers call this function synchronously,
    so we use asyncio.run() to execute async handlers.
    """
    asyncio.run(on_telegram_message(event))


async def on_telegram_message(event):
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
            await handle_translate_command(text, chat_id)
        case "/detect":
            await handle_detect_command(text, chat_id)
        case "/help":
            await handle_help_command(chat_id)


async def handle_translate_command(text: str, chat_id):
    """Handle /translate command.

    Note: Expected format is "/translate <target_lang> <text>"
    Example: /translate Spanish Hello, how are you?
    """
    parts = text.split(maxsplit=2)
    if len(parts) < 3:  # Not enough parts
        await telegram.send_message(chat_id=chat_id, text=TRANSLATE_USAGE)
        return

    target_lang = parts[1]
    text_to_translate = parts[2]
    prompt = get_translate_prompt(target_lang, text_to_translate)

    response = gemini.generate_content(prompt)
    await telegram.send_message(chat_id=chat_id, text=response.text)


async def handle_detect_command(text: str, chat_id):
    """Handle /detect command.

    Note: Expected format is "/detect <target_lang> <text>"
    Example: /detect English Hola, ¿cómo estás?
    """
    parts = text.split(maxsplit=2)
    if len(parts) < 3:
        await telegram.send_message(chat_id=chat_id, text=DETECT_USAGE)
        return

    target_lang = parts[1]
    text_to_translate = parts[2]
    prompt = get_detect_prompt(target_lang, text_to_translate)

    response = gemini.generate_content(prompt)
    await telegram.send_message(chat_id=chat_id, text=response.text)


async def handle_help_command(chat_id):
    """Handle /help command."""
    await telegram.send_message(chat_id=chat_id, text=HELP_TEXT)
