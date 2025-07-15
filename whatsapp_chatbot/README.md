---
title: WhatsApp ChatGPT Bot
description: WhatsApp chatbot that responds to messages using ChatGPT intelligence
integrations: ["twilio", "chatgpt"]
categories: ["AI", "Productivity"]
tags: ["webhook_handling", "next_event", "long_running"]
---

# WhatsApp ChatGPT Bot

This project creates a WhatsApp chatbot that responds to messages using ChatGPT by integrating Twilio's WhatsApp API with OpenAI's ChatGPT.

API documentation:

- Twilio: https://www.twilio.com/docs/whatsapp/api
- OpenAI: https://platform.openai.com/docs/api-reference/chat

## How It Works

1. Start workflow using a webhook
2. User sends WhatsApp message to Twilio number
3. Twilio forwards message to webhook endpoint
4. Chatbot processes message and generates ChatGPT response
5. Response is sent back to user via WhatsApp

> [!NOTE]
> Users can send "clear history" message at any time to reset the conversation history.

## Cloud Usage

1. Initialize your connections (Twilio and ChatGPT)
2. Copy the `whatsapp_message` webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
3. Set up Twilio WhatsApp by navigating to Twilio Console → Messaging → Try it out → Send a WhatsApp message, then follow the instructions to join the conversation
4. Navigate to your Twilio Console → WhatsApp → Settings
5. Paste the copied webhook URL in the "When a message comes in" field
6. (Optional) Set the `FROM_NUMBER` environment variable if using a custom WhatsApp number instead of the default Twilio number.
7. Copy the `start_chatbot` webhook URL from the "Triggers" tab (see the [instructions here](https://docs.autokitteh.com/get_started/deployment#webhook-urls))
8. Set the webhook URL in your Twilio console for WhatsApp messages
9. Deploy project

## Trigger Workflow

> [!IMPORTANT]
> Ensure all connections (Twilio and ChatGPT) are initialized.

Start a long-running AutoKitteh session by sending an HTTP request to the webhook URL from step 6 in the [Cloud Usage](#cloud-usage) section above:

```shell
curl -i "${WEBHOOK_URL}"
```

> [!TIP]
> The workflow can also be triggered manually by clicking the "Run" button in the UI, and selecting start_chatbot as the entry-point function.

## Self-Hosted Deployment

Follow [these detailed instructions](https://docs.autokitteh.com/get_started/deployment) to deploy the project on a self-hosted server.

## Known Limitations

- Limited to 20 message history per conversation to prevent token overflow
- Requires Twilio WhatsApp approval for production use
