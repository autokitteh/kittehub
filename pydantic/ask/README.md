---
title: Ask - Slack Q&A Bot
description: Simple one-shot question answering bot for Slack using Pydantic AI
integrations: ["slack"]
categories: ["AI", "Samples"]
tags:
  [
    "slack_bot",
    "pydantic_ai",
    "question_answering",
    "stateless",
    "single_turn",
  ]
---

# Ask - Slack Q&A Bot 🤖

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-ask)

A simple Slack bot that answers questions using Pydantic AI. Send a message starting with `!ask` and get an instant AI-powered response in a thread. Each question is treated independently without conversation history.

### What AutoKitteh Provides

- **Slack Integration**: Seamless Slack event handling and message posting
- **Event Filtering**: Automatic routing of `!ask` commands to the handler
- **Connection Management**: Secure credential storage for Slack and AI providers
- **Reliable Execution**: Guaranteed message processing and response delivery

## Features

- **One-Shot Q&A**: Each question is independent with no conversation memory
- **Threaded Responses**: Replies appear as threads to keep channels clean
- **Configurable Models**: Switch between any Pydantic AI-compatible model
- **Simple Integration**: Just add the bot to your Slack workspace and start asking

## How It Works

1. **User posts message**: `!ask What is the capital of France?`
2. **AutoKitteh triggers**: Filters and routes the message to the handler
3. **AI processes**: Pydantic AI agent generates a concise response
4. **Bot replies**: Response appears in a thread attached to the original message

## Architecture

```
Slack Message (!ask) → AutoKitteh Event Trigger → Pydantic AI Agent → Slack Thread Reply
```

### Key Components

- **`handlers.py`**: Event handler that processes Slack messages and generates AI responses
- **`autokitteh.yaml`**: AutoKitteh project configuration with Slack trigger and event filter

## Setup

### Prerequisites

- AutoKitteh account (cloud or self-hosted)
- Slack workspace where you can install apps
- API key for your chosen AI provider (Anthropic, OpenAI, etc.)

### Installation

1. Start using AutoKitteh Cloud:

   [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-ask)

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

### Asking Questions

Simply type `!ask` followed by your question in any channel where the bot is present:

```
!ask What is the speed of light?
!ask Explain quantum entanglement in simple terms
!ask Who wrote "The Great Gatsby"?
```

The bot will respond in a thread with a concise answer.

### Changing the AI Model

Update the `MODEL_NAME` variable in `autokitteh.yaml` or in the AutoKitteh UI:

```yaml
vars:
  - name: MODEL_NAME
    value: "anthropic:claude-sonnet-4-0"  # or "openai:gpt-4o", etc.
```

Supported model formats:
- Anthropic: `anthropic:claude-sonnet-4-0`
- OpenAI: `openai:gpt-4o`
- Any other Pydantic AI-compatible provider

## Technical Details

### Pydantic AI Integration

The project uses [Pydantic AI](https://ai.pydantic.dev/) for AI interactions:

- **Stateless Agent**: No conversation history - each question is independent
- **Concise Instructions**: Agent is configured to respond in one sentence
- **Synchronous Processing**: Uses `run_sync()` for simple request/response flow

### Event Filtering

The AutoKitteh trigger uses a filter to only process relevant messages:

```python
filter: "data.thread_ts == '' && data.text.startsWith('!ask')"
```

This ensures:
- Only top-level messages are processed (not thread replies)
- Only messages starting with `!ask` trigger the bot

### Response Format

Responses are posted as threaded replies with the format:

```
`<model-name>` says:
```<answer>```
```

This keeps the main channel clean while providing context about which model generated the response.

## Comparison with Other Samples

| Sample | Conversation History | UI | Use Case |
|--------|---------------------|-----|----------|
| **ask** | ❌ No | Slack | Quick one-off questions |
| **chat** | ✅ Yes | Slack | Multi-turn conversations |
| **chat_with_ui** | ✅ Yes | Web | Browser-based chat |
| **gamble** | ✅ Yes | Slack | Interactive AI games |

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
5. **Start asking**: Use `!ask` in Slack

## Customization Ideas

- **Change response style**: Modify the agent's instructions for different tones
- **Add context**: Pass additional information to the agent (company docs, user data, etc.)
- **Multi-language**: Detect language and respond accordingly
- **Rate limiting**: Track usage per user or channel
- **Custom commands**: Add more `!` commands for different behaviors

## Known Limitations

- No conversation memory across questions
- Single sentence responses (by design)
- Requires the bot to be in the channel
- No support for direct messages (DMs) - only channels
