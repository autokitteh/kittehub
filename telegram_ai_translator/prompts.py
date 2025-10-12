"""Constants for the Telegram AI Translator bot."""

# Help message
HELP_TEXT = """🌍 AI Translator Bot

Commands:
/translate <lang> <text> - Translate text to target language
/detect <lang> <text> - Auto-detect source language and translate
/help - Show this help message

Examples:
/translate es Hello, how's your project going?
/translate fr Good morning!
/detect en Bonjour le monde!

Powered by Gemini AI 🤖
"""

# Usage messages
TRANSLATE_USAGE = """Usage: /translate <target_language> <text>
Example: /translate es Hello, how are you?"""

DETECT_USAGE = """Usage: /detect <target_language> <text>
Example: /detect en Hola, ¿cómo estás?"""


# Prompt templates
def get_translate_prompt(target_lang: str, text: str) -> str:
    """Generate translation prompt for Gemini."""
    return f"""Translate the following text to {target_lang}.
Provide a natural, contextual translation that preserves tone and meaning.
If there are cultural nuances or idioms, briefly explain them after the translation.

Text: {text}

Format your response as:
Translation: <translated text>
Notes: <any cultural context or notes, if applicable>
"""


def get_detect_prompt(target_lang: str, text: str) -> str:
    """Generate auto-detect translation prompt for Gemini."""
    return f"""Detect the source language and translate to {target_lang}.
Provide a natural translation with cultural context.

Text: {text}

Format:
Detected: <source language>
Translation: <translated text>
Notes: <cultural context if relevant>
"""
