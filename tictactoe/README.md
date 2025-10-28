---
title: TicTacToe - Multiplayer Browser Game
description: Simple web-based TicTacToe game with multiplayer support and state persistence
integrations: []
categories: ["Demo"]
tags:
  [
    "webhook_handling",
    "sync_responses",
    "state_management",
    "interactive_workflows",
    "game",
  ]
---

# TicTacToe

[![Start with AutoKitteh](https://autokitteh.com/assets/autokitteh-badge.svg)](https://app.autokitteh.cloud/template?template-name=tictactoe)

A simple web-based TicTacToe game that demonstrates AutoKitteh's state management and webhook handling capabilities. Play with a friend by sharing game URLs, with automatic refresh when it's your turn.

### What AutoKitteh Provides

- State persistence without a database
- Atomic operations to prevent race conditions
- Webhook endpoints with path routing
- Synchronous HTTP responses
- No infrastructure to set up or maintain

## How It Uses AutoKitteh

The game uses 4 AutoKitteh features:

```python
from autokitteh import check_and_set_value, get_value, get_webhook_url, http_outcome, set_value
```

1. **Webhook Trigger** (`autokitteh.yaml`): Synchronous webhook for all game interactions

   ```yaml
   triggers:
     - name: webhook
       type: webhook
       call: handlers.py:on_webhook
       is_sync: true
   ```

2. **State Storage** (`handlers.py:79`): Store game state without a database

   ```python
   set_value(
       game_id,
       {
           "board": [[None] * 3] * 3,
           "turn": 0,
       },
   )
   ```

3. **Atomic Updates** (`handlers.py:123`): Prevent concurrent move conflicts

   ```python
   if not check_and_set_value(game_id, game, new_game):
       http_outcome(409, "conflict, please try again")
   ```

4. **HTTP Responses** (`handlers.py:68`): Return HTML and redirects
   ```python
   http_outcome(302, headers={"Location": f"/{_BASE_URL}/game/{game_id}/{who}"})
   ```

The rest is regular Python game logic.

## How It Works

1. **Start New Game**: Visit `/new` to create a new game and get redirected as player X
2. **Share URL**: Share the URL with another player who can join as player O
3. **Make Moves**: Click on empty cells to make your move
4. **Auto-Refresh**: When it's not your turn, the page auto-refreshes every 5 seconds
5. **Observe**: Anyone can observe a game without joining by visiting `/game/<game_id>`

## Features

- **Multiplayer**: Two players can play by sharing a game URL
- **State Persistence**: Game state is automatically saved and retrieved
- **Conflict Resolution**: Atomic operations prevent race conditions from concurrent moves
- **Auto-Refresh**: Page automatically refreshes when waiting for opponent's move
- **Observer Mode**: Watch games without participating
- **Clean UI**: Simple, responsive interface with hover effects

## Usage

### Starting a New Game

1. Visit the webhook URL: `https://api.autokitteh.cloud/webhooks/<WEBHOOK_SLUG>`
2. Click on `/new` to start a new game
3. You'll be redirected to your game as player X
4. Share the URL with a friend to join as player O

### URL Patterns

- `/` - Help page with instructions
- `/new` - Create a new game
- `/game/<game_id>` - Observe a game
- `/game/<game_id>/X` - Join/play as X
- `/game/<game_id>/O` - Join/play as O

### Game Rules

- X always goes first
- Players alternate turns
- Click on an empty cell to make your move
- First to get three in a row (horizontal, vertical, or diagonal) wins
- If all cells are filled without a winner, it's a draw

## Development

Just run `make` to test locally.

To deploy to AutoKitteh, either hit the "Start With AutoKitteh" button above, or use the CLI:

1. Install the CLI https://docs.autokitteh.com/get_started/install
2. Authenticate: `ak auth login`
3. Deploy: `make deploy`
4. Visit the webhook URL to start playing

## Configuration

No configuration needed! The game works out of the box with no external dependencies or connections.

## Technical Details

### State Management

Each game is stored with a unique game ID using AutoKitteh's key-value store:

```python
{
    "board": [[None, "X", None],
              [None, "O", None],
              [None, None, None]],
    "turn": 2
}
```

### Concurrency Handling

The `check_and_set_value` function ensures atomic updates, preventing race conditions when both players try to move simultaneously. If a conflict occurs, the player receives a 409 status code and can retry.

### Auto-Refresh Logic

When viewing a game where it's not your turn, JavaScript automatically refreshes the page every 5 seconds to show the opponent's latest move.
