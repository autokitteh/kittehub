---
title: D&D Party Chat - AI-Powered Multiplayer RPG
description: Web-based D&D game where you adventure with AI teammates, powered by multiple LLM providers
integrations: ["pydanticgw"]
categories: ["AI", "Samples"]
tags:
  [
    "webhook_handling",
    "sync_responses",
    "state_management",
    "interactive_workflows",
    "game",
    "streaming",
    "long_running",
  ]
---

# D&D Party Chat 🎲⚔️

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-dnd)

An AI-powered Dungeons & Dragons adventure where you play alongside AI teammates in a persistent, web-based multiplayer experience. Choose your character, select your preferred AI models for the Dungeon Master and party members, and embark on epic quests with seamless state persistence.

### What AutoKitteh Provides

- **Persistent Game State**: Sessions survive server restarts with no database needed
- **Streaming Responses**: Real-time AI-generated narrative using Server-Sent Events
- **Durable Workflows**: Long-running game sessions that never lose progress
- **Multi-Provider AI**: Support for Claude, GPT, and Gemini models
- **Session Management**: Automatic reconnection to ongoing games

## Features

- **Multiplayer Party System**: Play as the human hero with 0-3 AI-controlled teammates
- **AI Dungeon Master**: Dynamic storytelling and game management powered by AI
- **Model Selection**: Choose from multiple AI providers (Claude Sonnet 4.5, GPT-4o, Gemini, etc.)
- **Rich Character System**: Full D&D stats (HP, AC, STR, DEX, CON, INT, WIS, CHA)
- **Real-time Updates**: Streaming responses with thinking indicators
- **Persistent Sessions**: Resume your adventure from any browser
- **Beautiful UI**: Fantasy-themed interface with animations and character cards

## How It Works

1. **Start a Game**: Visit the webhook URL and join as a new player
2. **Configure Your Party**: Choose your character class/race and select AI models for DM and teammates
3. **Adventure Together**: Chat with your party and the DM responds with narrative
4. **AI Interactions**: Each AI player has their own personality and responds in turn
5. **Persistent State**: Your game is saved automatically - reload anytime to continue

## Architecture

```
Browser → AutoKitteh Webhook → Game Session (Durable)
                                 ├─ AI DM (Claude/GPT/Gemini)
                                 ├─ AI Player 1
                                 ├─ AI Player 2
                                 ├─ AI Player 3
                                 └─ Game State (Auto-persisted)
```

### Key Components

- **`handlers.py`**: Webhook handlers for game initialization and turn processing
- **`game.py`**: Core game logic with state management and event generation
- **`protocol.py`**: Pydantic models for type-safe client-server communication
- **`ai.py`**: AI agent management using Pydantic AI with tool use
- **`data.py`**: Character generation and D&D data
- **`game.html`**: Single-page web interface with SSE streaming
- **`autokitteh.yaml`**: AutoKitteh project configuration

## Setup

### Prerequisites

- AutoKitteh account (cloud or self-hosted)
- API keys for your chosen AI providers:
  - Anthropic API key (for Claude models)
  - OpenAI API key (for GPT models)
  - Google AI API key (for Gemini models)

### Installation

1. Start using AutoKitteh Cloud:

   [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-dnd)

2. Initialize the `pydanticgw` connection:

   - Navigate to your deployed project in AutoKitteh UI
   - Go to the **Connections** tab
   - Initialize the `pydanticgw` connection with your API keys for Anthropic, OpenAI, and/or Google AI
   - The Pydantic Gateway connection allows the game to use multiple AI providers seamlessly

3. Get your game webhook URL:

   - In AutoKitteh, go to your project's **Triggers** tab
   - Copy the `game` webhook URL
   - Visit this URL in your browser to start playing

4. Optional: Adjust game timeout

   Update the `GAME_TIMEOUT_SECONDS` variable in `autokitteh.yaml` (default: 3600 seconds / 1 hour)

   ```yaml
   vars:
     - name: GAME_TIMEOUT_SECONDS
       value: "7200" # 2 hours
   ```

## Usage

### Starting a New Game

1. Visit your game webhook URL: `https://api.autokitteh.cloud/webhooks/<WEBHOOK_SLUG>`
2. You'll be redirected to a new game session
3. Configure your adventure:
   - **Enter your name**
   - **Choose your race**: Human, Elf, Dwarf, Halfling, etc.
   - **Choose your class**: Warrior, Mage, Rogue, Cleric, etc.
   - **Select DM model**: Choose which AI runs the Dungeon Master
   - **Select AI teammates**: Choose 0-3 AI players and their models
4. Click **Join Game** to begin your adventure

### Playing

- **Your Turn**: Type your actions, questions, or dialogue in the chat input
- **AI Responses**: The DM and your AI party members respond in sequence
- **Character Stats**: View everyone's HP, AC, and abilities in the sidebar
- **Thinking Indicators**: See when the AI is generating responses
- **Persistent Sessions**: Close the browser and return later - your game continues

### Reconnecting

- Bookmark your game URL to return anytime
- The game automatically syncs state when you reload
- Your position, character stats, and full message history are preserved

## Available AI Models

The game supports multiple AI providers through Pydantic Gateway:

- **Claude Sonnet 4.5** (Recommended): Best for creative storytelling
- **Claude Sonnet 3.5**: Faster, good balance of quality and speed
- **GPT-4o**: OpenAI's multimodal model
- **GPT-4o Mini**: Faster, cost-effective option
- **GPT-5 Mini**: Latest OpenAI model
- **Gemini 3 Flash Preview**: Google's fast preview model
- **Gemini 3 Pro**: Google's production model

Each AI agent (DM and players) can use a different model, allowing you to experiment with combinations.

## Technical Details

### Pydantic AI Integration

The project uses [Pydantic AI](https://ai.pydantic.dev/) for type-safe AI interactions:

- **Structured Outputs**: AI responses are validated Pydantic models
- **Tool Use**: DM can roll dice, update stats, and manage game state
- **Prompt Caching**: Efficient handling of long conversation histories
- **Multi-Provider**: Seamless switching between Claude, GPT, and Gemini

### Protocol & Event Streaming

Client-server communication uses Server-Sent Events (SSE) with Pydantic validation:

```python
class MessageEvent(SSEEvent):
    event_type: ClassVar[str] = "message"
    player_id: int
    text: str

class DMMessageEvent(SSEEvent):
    event_type: ClassVar[str] = "dm_message"
    text: str  # Supports markdown formatting
```

### State Management

Game state is automatically persisted by AutoKitteh's durable workflows:

- **Player stats**: HP, AC, ability scores
- **Message history**: Full conversation log
- **AI context**: Each agent maintains its own message history for prompt caching
- **Turn tracking**: Knows whose turn it is and handles reconnection

### Sync Protocol

When reconnecting, clients send a sync request:

```python
class SyncAction(BaseModel):
    type: Literal["sync"] = "sync"
```

The server responds with either:
- `GameNotStartedEvent`: Show join UI
- `GameStateEvent`: Full game state with players and history

This allows seamless reconnection without losing context.

## Development

Run type checking and validation locally:

```bash
make
```

Deploy from the command line:

1. **Install the CLI**: https://docs.autokitteh.com/get_started/install
2. **Authenticate**: `ak auth login`
3. **Deploy**: `make deploy`
4. **Initialize connections**: Log in to https://autokitteh.cloud and initialize the `pydanticgw` connection
5. **Visit webhook URL**: Start your adventure

## Configuration

### Game Timeout

Adjust how long inactive games remain alive:

```yaml
vars:
  - name: GAME_TIMEOUT_SECONDS
    value: "3600" # 1 hour (default)
```

### Supported Models

The game automatically detects model families from names:
- Names starting with `claude-` use Anthropic
- Names starting with `gpt-` use OpenAI
- Names starting with `gemini-` use Google AI

Add new models by updating `modelOptions` in `game.html`.

## Known Limitations

- Single human player per game session
- Turn-based gameplay (no simultaneous actions)
- Session timeout after inactivity (configurable)
- No dice rolling UI (DM controls all rolls)

## Future Enhancements

- Multiple human players
- Custom character creation with point-buy system
- Dice rolling interface for players
- Combat encounter management
- Inventory and equipment system
- Save/load game snapshots
- Game master override controls
