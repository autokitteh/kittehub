# WhatsApp Chatbot

A simple WhatsApp chatbot powered by Twilio and ChatGPT integration.

## Metadata

- **Title**: WhatsApp Chatbot with ChatGPT
- **Description**: A responsive WhatsApp chatbot that uses ChatGPT to generate intelligent responses to incoming messages via Twilio integration
- **Integrations**: twilio, chatgpt
- **Categories**: AI, Samples

## Features

- Receives WhatsApp messages via Twilio webhook
- Processes messages using ChatGPT for intelligent responses
- Sends responses back to users via WhatsApp
- Error handling for failed API calls
- Configurable system prompt for chatbot personality

## Setup

1. **Twilio Setup**:
   - Create a Twilio account and get your Account SID and Auth Token
   - Set up WhatsApp Sandbox or get approved WhatsApp Business number
   - Configure webhook URL to point to your AutoKitteh deployment

2. **ChatGPT Setup**:
   - Get OpenAI API key
   - Configure the connection in AutoKitteh

3. **Configuration**:
   - Update the `SYSTEM_PROMPT` variable to customize chatbot behavior
   - Ensure Twilio webhook points to your AutoKitteh trigger endpoint

## How It Works

1. User sends a WhatsApp message
2. Twilio forwards the message to AutoKitteh via webhook
3. The `handle_whatsapp_message` function processes the incoming message
4. ChatGPT generates a response based on the message content
5. Response is sent back to the user via Twilio WhatsApp API

## Customization

- Modify the `SYSTEM_PROMPT` in `autokitteh.yaml` to change chatbot personality
- Adjust ChatGPT model parameters (temperature, max_tokens) in `program.py`
- Add conversation history storage for multi-turn conversations
- Implement user-specific context or preferences

## Error Handling

The chatbot includes error handling for:
- Empty or malformed messages
- ChatGPT API failures
- Twilio messaging errors
- General processing exceptions

## Usage

Once deployed and configured:
1. Send a message to your Twilio WhatsApp number
2. The chatbot will respond with a ChatGPT-generated message
3. Continue the conversation naturally