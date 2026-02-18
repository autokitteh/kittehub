---
title: Chat with UI - Web-Based Conversational AI
description: Browser-based chat interface with persistent conversation history using Pydantic AI
integrations: []
categories: ["AI", "Samples"]
tags:
  [
    "web_ui",
    "pydantic_ai",
    "conversation",
    "stateful",
    "multi_turn",
    "durable_workflows",
    "webhook",
    "http",
  ]
---

# Chat with UI - Web-Based Conversational AI 🌐💬

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-chat-with-ui)

A web-based chat interface for conversing with AI. Simply visit the webhook URL in your browser and start chatting - no Slack or external integrations required. Each browser tab gets its own persistent conversation.

### What AutoKitteh Provides

- **Instant Web UI**: No frontend development needed - just deploy and access the URL
- **Durable Workflows**: Conversations persist even if the server restarts
- **Session Management**: Each browser tab gets an isolated conversation
- **Synchronous HTTP**: Instant responses without polling or WebSockets
- **State Persistence**: Message history maintained automatically

## Features

- **Browser-Based**: Access from any web browser, no additional apps needed
- **Conversation Memory**: Full message history maintained throughout the session
- **Isolated Sessions**: Each tab/URL has its own independent conversation
- **Durable State**: Survives server restarts without losing context
- **Configurable Models**: Switch between any Pydantic AI-compatible model
- **Simple HTML UI**: Clean, functional interface included

## How It Works

1. **User visits webhook URL**: `https://api.autokitteh.cloud/webhooks/<slug>`
2. **AutoKitteh serves HTML**: Chat interface loaded with unique session ID
3. **User types message**: Browser sends POST request to session-specific endpoint
4. **AI processes with history**: Pydantic AI generates response with full context
5. **Response displayed**: Answer appears instantly in the chat interface
6. **Loop continues**: Each message includes full conversation history

## Architecture

```
Browser GET /webhook → Serve HTML with Session ID
                       ↓
                  Durable Workflow Created
                       ↓
Browser POST /webhook/{session} → Process with History → Return Response
         ↑                                                      ↓
         └─────────────────────────────────────────────────────┘
                        (Conversation Loop)
```

### Key Components

- **`handlers.py`**: Webhook handler that serves UI and processes chat messages
- **`chat.html`**: HTML/JavaScript chat interface with message history display
- **`autokitteh.yaml`**: AutoKitteh project configuration with webhook triggers

## Setup

### Prerequisites

- AutoKitteh account (cloud or self-hosted)
- API key for your chosen AI provider (Anthropic, OpenAI, etc.)

### Installation

1. Start using AutoKitteh Cloud:

   [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-chat-with-ui)

2. Configure your API key:
   - Navigate to the project configuration in AutoKitteh UI
   - Go to the **Variables** tab
   - Set `ANTHROPIC_API_KEY` (or your provider's key)
   - Optionally change `MODEL_NAME` (default: `anthropic:claude-sonnet-4-0`)

3. Get your webhook URL:
   - In AutoKitteh, go to your project's **Triggers** tab
   - Copy the `start` webhook URL
   - Visit this URL in your browser to start chatting

## Usage

### Starting a Conversation

1. Visit your webhook URL in a browser: `https://api.autokitteh.cloud/webhooks/<WEBHOOK_SLUG>`
2. The chat interface loads automatically
3. Type your message in the input box and press Enter or click Send
4. The AI responds instantly with full conversation context

### Continuing the Conversation

Simply keep typing messages. The conversation history is maintained:

```
You: What is machine learning?
AI: Machine learning is a subset of artificial intelligence where algorithms...

You: Can you give me an example?
AI: A common example is email spam detection, where the system learns to...

You: How does it differ from traditional programming?
AI: Traditional programming uses explicit rules written by developers, while ML...
```

### Multiple Conversations

Each browser tab or window gets its own unique session:
- **Tab 1**: Discussion about Python → `https://api.../webhooks/abc/session-1`
- **Tab 2**: Discussion about cooking → `https://api.../webhooks/abc/session-2`
- **Tab 3**: Discussion about history → `https://api.../webhooks/abc/session-3`

Each session maintains completely independent conversation history.

### Reconnecting to a Conversation

Bookmark the URL with the session ID to return to the same conversation later:
- Original URL creates new session: `https://api.../webhooks/abc`
- Bookmarked URL returns to session: `https://api.../webhooks/abc/session-123`

As long as the AutoKitteh workflow is still active, the conversation history persists.

### Changing the AI Model

Update the `MODEL_NAME` variable in `autokitteh.yaml`:

```yaml
vars:
  - name: MODEL_NAME
    value: "anthropic:claude-sonnet-4-0"  # or "openai:gpt-4o", etc.
```

Deploy the updated configuration and the new model will be used for all new sessions.

## Technical Details

### Pydantic AI Integration

The project uses [Pydantic AI](https://ai.pydantic.dev/) for AI interactions:

- **Stateful Agent**: Maintains message history across HTTP requests
- **Message History**: Uses `message_history` parameter for context
- **Prompt Caching**: Efficient handling of long conversation histories
- **Structured Responses**: Type-safe message handling

### Durable Workflows

AutoKitteh's durable workflows enable persistent conversations:

```yaml
triggers:
  - name: start
    is_durable: true   # Enables workflow persistence
    is_sync: true      # Returns HTTP response synchronously
```

Benefits:
- Conversation state survives server restarts
- No database needed - AutoKitteh handles persistence
- Automatic state management and recovery
- Each session runs in isolated workflow instance

### Session Management

Session IDs are automatically generated by AutoKitteh:
- GET request to webhook → AutoKitteh generates session_id
- HTML served with session-specific API endpoint embedded
- POST requests include session_id in URL path
- Subscription filter ensures correct workflow processes messages

### Synchronous HTTP Responses

Unlike traditional async architectures, this uses synchronous responses:

```python
http_outcome(200, body=a, event_id=event.event_id)
```

The `event_id` links the response to the specific HTTP request, allowing AutoKitteh to return the response to the waiting browser.

### HTML Interface

The `chat.html` template includes:
- Message input form with submit handler
- Message history display (user messages and AI responses)
- JavaScript for AJAX POST requests
- Simple CSS styling for readability
- Session-specific API endpoint injected via `{{API_ENDPOINT}}` placeholder

## Comparison with Other Samples

| Sample | Conversation History | UI | Use Case |
|--------|---------------------|-----|----------|
| **ask** | ❌ No | Slack | Quick one-off questions |
| **chat** | ✅ Yes | Slack | Multi-turn Slack conversations |
| **chat_with_ui** | ✅ Yes | Web | Browser-based chat |
| **gamble** | ✅ Yes + Tools | Slack | Interactive AI games |
| **dnd** | ✅ Yes + Tools | Web | Multiplayer AI RPG |

## Development

Run type checking and validation locally:

```bash
ak make
```

Deploy from the command line:

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `ak deploy`
4. **Visit webhook URL**: Start chatting in your browser

## Customization Ideas

### UI Enhancements
- Add markdown rendering for AI responses
- Implement typing indicators
- Add conversation export functionality
- Support for file uploads or image inputs
- Dark mode toggle
- Message timestamps

### Functionality
- Add system prompts configurable via UI
- Implement conversation reset button
- Support for multiple AI models with selector
- Rate limiting per session
- User authentication and stored conversations
- Conversation sharing via unique URLs

### Integration
- Connect to external knowledge bases
- Add web search capabilities
- Implement RAG (Retrieval-Augmented Generation)
- Support for multi-modal inputs (images, documents)

## Known Limitations

- No built-in authentication (anyone with URL can access)
- Session persistence limited by AutoKitteh workflow timeout
- No conversation list or management UI
- Simple HTML interface (no advanced UI framework)
- No support for streaming responses (responses appear all at once)
- No message editing or deletion
- Single AI model per session (can't switch mid-conversation)

## Troubleshooting

**Chat interface doesn't load:**
- Verify the webhook URL is correct
- Check that the `start` trigger is deployed and active
- Ensure `chat.html` file exists in the project directory

**Messages not getting responses:**
- Check AutoKitteh logs for errors
- Verify API key is configured correctly
- Ensure the workflow hasn't timed out

**Lost conversation history:**
- Session may have expired (AutoKitteh workflow timeout)
- Server restart without proper session ID bookmark
- Check that `is_durable: true` is set in trigger configuration

**Multiple simultaneous responses:**
- Avoid clicking Send button multiple times
- Check browser network tab for duplicate requests
- Verify only one AutoKitteh deployment is active

## Security Considerations

- **No authentication**: Anyone with the webhook URL can use the chat
- **Session hijacking**: If someone knows the session URL, they can access the conversation
- **Rate limiting**: Consider implementing rate limits to prevent abuse
- **API key exposure**: Ensure environment variables are properly secured
- **Input validation**: Add validation for message length and content

For production use, consider adding authentication, rate limiting, and input validation.
