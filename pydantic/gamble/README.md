---
title: Gamble - AI Casino Bot
description: Interactive roulette and blackjack games powered by AI tool calling with Pydantic AI
integrations: ["slack"]
categories: ["AI", "Samples"]
tags:
  [
    "slack_bot",
    "pydantic_ai",
    "tool_calling",
    "games",
    "interactive",
    "stateful",
    "multi_turn",
    "logfire",
    "observability",
  ]
---

# Gamble - AI Casino Bot 🎰🃏

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-gamble)

An AI-powered casino bot for Slack that plays roulette and blackjack with you. The AI acts as the dealer, using Pydantic AI's tool calling to spin wheels, deal cards, and manage game state. A perfect example of interactive AI with function calling.

### What AutoKitteh Provides

- **Durable Workflows**: Game state persists even if the server restarts
- **Event Subscriptions**: Automatic routing of thread messages to the game handler
- **State Management**: Game history and context maintained automatically
- **Reliable Execution**: Guaranteed message processing with no lost game actions

## Features

- **Multi-Game Support**: Play roulette or blackjack in the same thread
- **AI Tool Calling**: Demonstrates Pydantic AI's function calling capabilities
- **Interactive Gameplay**: Conversational interface for natural game flow
- **Persistent State**: Game history maintained throughout the session
- **Observability**: Logfire integration for monitoring AI decisions and tool calls
- **Configurable Models**: Switch between any Pydantic AI-compatible model

## How It Works

### Roulette

1. **Start game**: `!gamble I want to play roulette`
2. **AI asks for bet**: "Which number would you like to bet on (1-38)?"
3. **Place bet**: "I bet on 17"
4. **AI spins wheel**: Calls `roulette_wheel()` tool to get result
5. **Win/Lose**: AI announces the result and determines if you won

### Blackjack

1. **Start game**: `!gamble Let's play blackjack`
2. **AI deals cards**: Uses `draw_card()` tool to deal initial hands
3. **AI shows cards**: "You have a 7 and a King. I'm showing a 9. Hit or stand?"
4. **Player choice**: "Hit me"
5. **AI continues**: Deals more cards and plays dealer hand
6. **Determine winner**: AI announces winner based on standard blackjack rules

## Architecture

```
Slack Message (!gamble) → Durable Workflow Created
                          ↓
                     Subscribe to Thread
                          ↓
                     Conversation Loop:
                     ├─ Wait for message
                     ├─ AI processes with context
                     ├─ AI calls tools as needed
                     │  ├─ roulette_wheel() → returns 1-38
                     │  └─ draw_card() → returns 1-13
                     ├─ AI generates response
                     ├─ Reply in thread
                     └─ Repeat indefinitely
```

### Key Components

- **`handlers.py`**: Durable workflow handler with AI agent and tool definitions
- **`autokitteh.yaml`**: AutoKitteh project configuration with durable trigger
- **Tools**:
  - `roulette_wheel()`: Spins roulette wheel, returns winning number (1-38)
  - `draw_card()`: Draws a card, returns value (1-13 for Ace through King)

## Setup

### Prerequisites

- AutoKitteh account (cloud or self-hosted)
- Slack workspace where you can install apps
- API key for your chosen AI provider (Anthropic, OpenAI, etc.)
- Optional: Logfire account for observability (free tier available)

### Installation

1. Start using AutoKitteh Cloud:

   [![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=pydantic-gamble)

2. Configure your API keys:
   - Navigate to the project configuration in AutoKitteh UI
   - Go to the **Variables** tab
   - Set `ANTHROPIC_API_KEY` (or your provider's key)
   - Optional: Set `LOGFIRE_TOKEN` for observability
   - Optionally change `MODEL_NAME` (default: `anthropic:claude-sonnet-4-0`)

3. Initialize the Slack connection:
   - Go to the **Connections** tab
   - Initialize the `slack` connection
   - Follow the OAuth flow to authorize your Slack workspace

4. Invite the bot to a channel:
   - In Slack, type `/invite @AutoKitteh` in any channel
   - Or add it from the channel details

## Usage

### Starting a Game

Type `!gamble` followed by your message in any channel where the bot is present:

```
!gamble Let's play roulette
!gamble I want to play blackjack
!gamble Deal me in!
```

The AI will determine which game you want to play and start guiding you through it.

### Playing Roulette

Example conversation:

```
User: !gamble Let's play roulette!
Bot: Which number would you like to bet on (1-38)?

User: I'll bet on 7
Bot: [Tool call: roulette_wheel() → 23]
Bot: The wheel landed on 23 - sorry, you didn't win this time!

User: Let me try 23 this time
Bot: [Tool call: roulette_wheel() → 23]
Bot: The wheel landed on 23 - you win!
```

### Playing Blackjack

Example conversation:

```
User: !gamble Let's play blackjack
Bot: [Tool calls: draw_card() → 7, draw_card() → 10, draw_card() → 9, draw_card() → 5]
Bot: You have a 7 and a 10 (total 17). I'm showing a 9. Do you want to hit or stand?

User: I'll stand
Bot: [Tool calls: draw_card() → 8]
Bot: I reveal my hidden card - a 5 (total 14). I draw an 8 (total 22). I bust - you win!
```

### Switching Games

You can switch between games mid-thread:

```
User: !gamble Let's play roulette
Bot: Which number would you like to bet on?

User: Actually, let's play blackjack instead
Bot: Sure! Let me deal the cards...
```

### Changing the AI Model

Update the `MODEL_NAME` variable in `autokitteh.yaml`:

```yaml
vars:
  - name: MODEL_NAME
    value: "anthropic:claude-sonnet-4-0" # or "openai:gpt-4o", etc.
```

## Technical Details

### Pydantic AI Integration

The project uses [Pydantic AI](https://ai.pydantic.dev/) with tool calling:

- **Agent with Tools**: AI can call functions to interact with game mechanics
- **Stateful Conversations**: Maintains game state across multiple turns
- **Message History**: Uses conversation history for context
- **Tool Invocation**: Automatically determines when to call tools

### Tool Calling

Tools are defined as agent methods decorated with `@agent.tool_plain`:

```python
@roulette_agent.tool_plain
async def roulette_wheel() -> int:
    """Spin the roulette wheel and return the winning number."""
    return randint(1, 38)

@roulette_agent.tool_plain
async def draw_card() -> int:
    """Draw a card from a standard deck (1-13)."""
    return randint(1, 13)
```

The AI agent:

1. Understands tool descriptions and purposes
2. Decides when to call tools based on conversation
3. Uses tool results to formulate responses
4. Maintains game logic and rules in its reasoning

### Logfire Observability

Logfire integration provides visibility into:

- AI agent decisions and reasoning
- Tool calls with arguments and results
- Message history and conversation flow
- Performance metrics and latency

Configuration:

```python
logfire.configure()
logfire.instrument_pydantic_ai()
```

View logs and traces in your Logfire dashboard to understand how the AI is playing.

### Durable Workflows

AutoKitteh's durable workflows enable persistent game sessions:

```yaml
triggers:
  - name: slack_message
    is_durable: true # Game state survives server restarts
```

Benefits:

- Game state persists across AutoKitteh restarts
- No database needed for game history
- Automatic state management
- Reliable tool call execution

### System Prompt

The AI agent receives detailed instructions for both games:

- **Roulette**: Ask for number, call `roulette_wheel()`, compare results
- **Blackjack**: Deal cards using `draw_card()`, follow dealer rules, determine winner

The AI uses its understanding of game rules combined with tool calling to create an interactive experience.

## Comparison with Other Samples

| Sample           | Conversation History | Tools  | Use Case                        |
| ---------------- | -------------------- | ------ | ------------------------------- |
| **ask**          | ❌ No                | ❌ No  | Quick one-off questions         |
| **chat**         | ✅ Yes               | ❌ No  | Multi-turn conversations        |
| **chat_with_ui** | ✅ Yes               | ❌ No  | Browser-based chat              |
| **gamble**       | ✅ Yes               | ✅ Yes | Interactive AI games with tools |
| **dnd**          | ✅ Yes               | ✅ Yes | Complex multiplayer RPG         |

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
5. **Start playing**: Use `!gamble` in Slack

## Customization Ideas

### Additional Games

- **Poker**: Multi-player with betting rounds
- **Dice games**: Craps, Yahtzee
- **Card games**: War, Go Fish
- **Slots**: Virtual slot machine simulation

### Enhanced Features

- **Betting system**: Track virtual currency across games
- **Statistics**: Win/loss records, high scores
- **Multiplayer**: Allow multiple users in same game
- **Game rules**: Configurable house rules and payouts
- **Leaderboards**: Track top players across workspace

### Tool Enhancements

- **Deck management**: Track remaining cards in blackjack
- **Betting validation**: Ensure bets are within limits
- **Game history**: Export game results to spreadsheet
- **Animations**: Add ASCII art for cards and wheels

## Known Limitations

- Games run indefinitely until workflow times out
- No persistent betting/currency system
- Single player only (no multi-player support)
- Limited to two games (roulette and blackjack)
- No visual representation of cards/wheel (text only)
- AI may occasionally misinterpret game requests

## Troubleshooting

**Bot doesn't start game:**

- Ensure message starts with `!gamble`
- Check that bot has permission to read messages in channel
- Verify trigger is deployed and active in AutoKitteh UI

**Tools not being called:**

- Check Logfire logs for tool call attempts
- Verify model supports tool calling (most modern models do)
- Ensure prompts clearly request game actions

**Game state lost:**

- Check that `is_durable: true` is set in trigger configuration
- Verify workflow hasn't timed out
- Look for errors in AutoKitteh logs

**Inconsistent game rules:**

- Different AI models may interpret rules differently
- Consider adding more explicit rule details in system prompt
- Check tool call logs to debug AI reasoning

## Advanced: Adding New Games

To add a new game:

1. **Define tools** for game mechanics:

   ```python
   @roulette_agent.tool_plain
   async def roll_dice(sides: int) -> int:
       """Roll a dice with given number of sides."""
       return randint(1, sides)
   ```

2. **Update system prompt** with game rules:

   ```python
   system_prompt=(
       "..."
       "If the user wants to play dice, use the `roll_dice` function..."
   )
   ```

3. **Test the game** by describing it to the AI in Slack

The AI will automatically understand and play the new game using the provided tools!

## Security Considerations

- No real money involved (virtual casino only)
- Random number generation is pseudo-random (not cryptographically secure)
- Game results should not be used for real gambling
- Consider rate limiting to prevent spam
- No user authentication (anyone in channel can play)

This is a demonstration project for AI tool calling, not a production gambling system.
