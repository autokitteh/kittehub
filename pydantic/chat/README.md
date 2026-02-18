---
title: Chat - Conversational Slack Bot
description: Multi-turn conversation bot for Slack with persistent history using Pydantic AI
integrations: ["slack"]
categories: ["AI", "Samples"]
tags:
  [
    "slack_bot",
    "pydantic_ai",
    "conversation",
    "stateful",
    "multi_turn",
    "durable_workflows",
    "message_history",
  ]
---

# Chat - Conversational Slack Bot 💬

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-chat)

A Slack bot that maintains multi-turn conversations with full message history. Start a conversation with `!chat` and continue chatting in the thread - the bot remembers everything you've discussed.

### What AutoKitteh Provides

- **Durable Workflows**: Conversations persist even if the server restarts
- **Event Subscriptions**: Automatic routing of thread messages to the conversation handler
- **State Management**: Message history is maintained automatically across interactions
- **Reliable Delivery**: Guaranteed message processing with no lost responses

## Features

- **Conversation Memory**: Full message history maintained throughout the thread
- **Threaded Conversations**: Each `!chat` command starts an independent conversation
- **Durable State**: Survives server restarts without losing context
- **Configurable Models**: Switch between any Pydantic AI-compatible model
- **Infinite Duration**: Conversations continue indefinitely until workflow times out

## How It Works

1. **User starts conversation**: `!chat Tell me about quantum physics`
2. **AutoKitteh creates durable workflow**: Subscribes to thread events
3. **AI responds with context**: Uses Pydantic AI with message history
4. **User continues in thread**: Each reply is processed with full conversation context
5. **Loop continues**: Bot responds to every message, maintaining context

## Architecture

```
Slack Message (!chat) → Durable Workflow Created
                        ↓
                    Subscribe to Thread
                        ↓
                    Conversation Loop:
                    ├─ Wait for message
                    ├─ Process with full history
                    ├─ AI generates response
                    ├─ Reply in thread
                    └─ Repeat indefinitely
```

### Key Components

- **`handlers.py`**: Durable workflow handler that maintains conversation state and processes messages
- **`autokitteh.yaml`**: AutoKitteh project configuration with durable trigger enabled

## Setup

### Prerequisites

- AutoKitteh account (cloud or self-hosted)
- Slack workspace where you can install apps
- API key for your chosen AI provider (Anthropic, OpenAI, etc.)

### Installation

1. Start using AutoKitteh Cloud:

   [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-chat)

2. Configure your API key:
   - Navigate to the project configuration in AutoKitteh UI
   - Go to the **Variables** tab
   - Set `ANTHROPIC_API_KEY` (or your provider's key)
   - Optionally change `MODEL_NAME` (default: `anthropic:claude-sonnet-4-0`)

3. Initialize the Slack connection:
   - Go to the **Connections** tab
   - Initialize the `slack` connection
   - Follow the OAuth flow to authorize your Slack workspace

4. Invite the bot to a channel:
   - In Slack, type `/invite @AutoKitteh` in any channel
   - Or add it from the channel details

## Usage

### Starting a Conversation

Type `!chat` followed by your message in any channel where the bot is present:

```
!chat Let's discuss machine learning
```

The bot will respond in a thread, starting the conversation.

### Continuing the Conversation

Reply in the thread to continue the conversation. The bot remembers everything:

```
User: !chat What is neural network?
Bot: A neural network is a machine learning model inspired by biological neurons...

User: Can you explain backpropagation?
Bot: Backpropagation is the algorithm used to train neural networks by calculating...

User: How does it differ from forward propagation?
Bot: Forward propagation passes input through the network to generate output, while...
```

### Multiple Conversations

Each `!chat` command starts an independent conversation thread:

- Thread A: Discussion about Python
- Thread B: Discussion about JavaScript
- Thread C: Discussion about databases

Each thread maintains its own separate conversation history.

### Changing the AI Model

Update the `MODEL_NAME` variable in `autokitteh.yaml`:

```yaml
vars:
  - name: MODEL_NAME
    value: "anthropic:claude-sonnet-4-0"  # or "openai:gpt-4o", etc.
```

## Technical Details

### Pydantic AI Integration

The project uses [Pydantic AI](https://ai.pydantic.dev/) for AI interactions:

- **Stateful Agent**: Maintains message history across multiple turns
- **Message History**: Uses `message_history` parameter for context
- **Prompt Caching**: Efficient handling of long conversation histories
- **Structured Responses**: Type-safe message handling

### Durable Workflows

AutoKitteh's durable workflows enable persistent conversations:

```yaml
triggers:
  - name: slack_message
    is_durable: true  # Enables workflow persistence
```

Benefits:
- Conversation state survives server restarts
- No database needed - AutoKitteh handles persistence
- Automatic state management and recovery
- Reliable message processing

### Event Subscription

The handler subscribes to thread messages using AutoKitteh's event system:

```python
subscribe(
    "slack",
    f"data.type == 'message' && data.bot_id == '' && data.thread_ts == '{ts}'"
)
```

This ensures:
- Only user messages are processed (not bot messages)
- Only messages in the specific thread are captured
- Automatic event routing to the correct workflow instance

### Conversation Loop

The infinite loop maintains the conversation:

```python
while True:
    result = agent.run_sync(q, message_history=history)
    history = result.all_messages()
    # ... send response ...
    q = next_event(s).text  # Wait for next message
```

The `next_event()` call blocks until a new message arrives, efficiently using resources.

## Comparison with Other Samples

| Sample | Conversation History | UI | Use Case |
|--------|---------------------|-----|----------|
| **ask** | ❌ No | Slack | Quick one-off questions |
| **chat** | ✅ Yes | Slack | Multi-turn conversations |
| **chat_with_ui** | ✅ Yes | Web | Browser-based chat |
| **gamble** | ✅ Yes + Tools | Slack | Interactive AI games |

## Development

Run type checking and validation locally:

```bash
ak make
```

Deploy from the command line:

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `ak deploy`
4. **Initialize connections**: Log in to https://autokitteh.cloud and set up Slack
5. **Start chatting**: Use `!chat` in Slack

## Customization Ideas

- **Context injection**: Add system context or company knowledge to each request
- **Conversation summaries**: Periodically summarize long threads
- **User preferences**: Store and use per-user preferences
- **Multi-language**: Detect and respond in user's language
- **Conversation timeout**: Add custom timeout logic for inactive threads
- **Export conversations**: Save thread history to external storage
- **Agent tools**: Add function calling for specialized tasks

## Known Limitations

- Conversations run indefinitely until AutoKitteh workflow timeout
- All messages in thread are sent to the bot (can't distinguish @mentions)
- No support for direct messages (DMs) - only channels
- Single AI model per conversation (can't switch mid-thread)
- No built-in conversation reset command

## Troubleshooting

**Bot doesn't respond to thread messages:**
- Ensure the message is in the thread (not a new top-level message)
- Check that the bot has permission to read messages in the channel
- Verify the workflow is still running in AutoKitteh UI

**Context not maintained:**
- Check that `is_durable: true` is set in the trigger configuration
- Verify the workflow hasn't timed out or been terminated

**Multiple bot responses:**
- Ensure you haven't deployed multiple instances of the same project
- Check AutoKitteh logs for duplicate workflow executions
