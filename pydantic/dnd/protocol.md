# D&D Chat Multiplayer Protocol (HTTP Streaming)

## Architecture Overview

```
┌─────────────┐                    ┌─────────────┐
│  Client 1   │                    │             │
│  (Thorin)   │──── POST ─────────►│             │
│             │                    │   Server    │
│             │◄─── Stream ────────│  (Node.js/  │
│             │  "Elara: Hello"    │   Express)  │
│             │  "Finn rolled 18"  │             │
│             │  "Your turn!"      │             │
└─────────────┘  Connection ends   └─────────────┘
       │                                  │
       └──── POST (next turn) ───────────┘
            "I attack!"
```

## How It Works

### The Single Call Per Turn

Each player makes **ONE HTTP POST** when it's their turn:
1. **Client sends** - Their action (message, dice roll, stat update, or "pass")
2. **Server streams back** - All game events until it's their turn again
3. **Connection closes** - When their turn comes back around
4. **Client makes new POST** - For their next action

### Turn Order

- Dynamic rotation based on initiative or server logic
- Server tracks whose turn it is
- Each player only POSTs when it's their turn
- Between turns, they watch the stream for updates
- **Supports any number of players** - not limited to 4!

## The Single API Endpoint

### POST /api/game/:gameId/turn

**Request Headers:**
```
Content-Type: application/json
Accept: text/event-stream
```

**Request Body:**
```json
{
  "playerId": 1,
  "action": {
    "type": "message",
    "text": "I attack the goblin!"
  }
}
```

**Note:** Before taking turns, players must first join the game. On first connection (before `playerId` is assigned), clients should send a join request:

```json
{
  "action": {
    "type": "join",
    "playerName": "Alice",
    "playerCount": 3
  }
}
```

The server will:
1. Assign them a player ID and character
2. Create or join a game session with the specified number of players
3. Stream back the `player_joined` event with `isYou: true`
4. Stream additional `player_joined` events as other players join

**Action Types:**

1. **Message** - Player says something
```json
{
  "type": "message",
  "text": "Let's explore the dungeon"
}
```

2. **Dice Roll** - Player rolls dice
```json
{
  "type": "dice",
  "sides": 20,
  "modifier": 5,
  "reason": "Attack roll"
  // NOTE: No "roll" value sent - server generates the random result
}
```

3. **Stat Update** - Player updates their stats
```json
{
  "type": "stat_update",
  "stats": {
    "hp": 38
  }
}
```

4. **Pass** - Player does nothing this turn
```json
{
  "type": "pass"
}
```

5. **Multiple Actions** - Combine actions in one turn
```json
{
  "type": "multiple",
  "actions": [
    { "type": "message", "text": "I cast fireball!" },
    { "type": "dice", "sides": 6, "count": 8, "reason": "Fireball damage" },
    { "type": "stat_update", "stats": { "hp": 42 } }
  ]
}
```

**Response (Server-Sent Events Stream):**

The server sends a continuous stream of events using SSE format:

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

event: action_confirmed
data: {"playerId":1,"action":"message","text":"I attack the goblin!"}

event: turn_start
data: {"playerId":2,"playerName":"Elara"}

event: message
data: {"playerId":2,"playerName":"Elara","text":"I'll cast Magic Missile!","timestamp":"2025-12-18T10:30:00Z"}

event: turn_start
data: {"playerId":3,"playerName":"Finn"}

event: dice
data: {"playerId":3,"playerName":"Finn","sides":20,"roll":18,"modifier":5,"total":23,"reason":"Sneak attack","timestamp":"2025-12-18T10:30:15Z"}

event: stat_update
data: {"playerId":3,"playerName":"Finn","stats":{"hp":28,"maxHp":32}}

event: turn_start
data: {"playerId":4,"playerName":"Lyra"}

event: message
data: {"playerId":4,"playerName":"Lyra","text":"I heal Finn","timestamp":"2025-12-18T10:30:30Z"}

event: stat_update
data: {"playerId":3,"playerName":"Finn","stats":{"hp":32,"maxHp":32}}

event: dm_message
data: {"text":"The goblin falls defeated!","timestamp":"2025-12-18T10:30:45Z"}

event: your_turn
data: {"playerId":1,"playerName":"Thorin"}

event: close
data: {}
```

## Event Types

### 1. action_confirmed
Confirms the player's action was received (and includes server-generated dice roll if applicable)
```json
{
  "playerId": 1,
  "action": {
    "type": "dice",
    "sides": 20,
    "roll": 15  // Server-generated random result
  }
}
```

### 2. player_joined
A new player has joined the game
```json
{
  "player": {
    "id": 2,
    "name": "Elara",
    "class": "Mage",
    "color": "#2980b9",
    "stats": {
      "hp": 28,
      "maxHp": 28,
      "ac": 12,
      "str": 8,
      "dex": 14,
      "con": 12,
      "int": 18,
      "wis": 13,
      "cha": 10
    }
  },
  "isYou": false  // true if this is the connecting player
}
```

### 3. turn_start
Indicates whose turn is starting
```json
{
  "playerId": 2,
  "playerName": "Elara",
  "color": "#2980b9"
}
```

### 4. message
A player sends a chat message
```json
{
  "playerId": 2,
  "playerName": "Elara",
  "color": "#2980b9",
  "text": "I cast fireball!",
  "timestamp": "2025-12-18T10:30:00Z"
}
```

### 5. dice
A player rolls dice
```json
{
  "playerId": 3,
  "playerName": "Finn",
  "color": "#27ae60",
  "sides": 20,
  "roll": 18,
  "modifier": 5,
  "total": 23,
  "reason": "Attack roll",
  "timestamp": "2025-12-18T10:30:15Z"
}
```

### 6. stat_update
Player stats change
```json
{
  "playerId": 3,
  "playerName": "Finn",
  "stats": {
    "hp": 28,
    "maxHp": 32
  }
}
```

### 7. dm_message
Dungeon Master narration (can be from server AI or fifth player)
```json
{
  "text": "The goblin falls defeated! You gain 50 XP.",
  "timestamp": "2025-12-18T10:30:45Z"
}
```

### 8. your_turn
Indicates it's this player's turn again (triggers connection close)
```json
{
  "playerId": 1,
  "playerName": "Thorin"
}
```

### 9. close
Signals the stream is ending
```json
{}
```

## Client Implementation

```javascript
let myPlayerId = 1; // Assigned at game start
let gameId = "game-abc123";

async function takeTurn(action) {
  const response = await fetch(`/api/game/${gameId}/turn`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'text/event-stream'
    },
    body: JSON.stringify({
      playerId: myPlayerId,
      action: action
    })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n\n');
    buffer = lines.pop(); // Keep incomplete message
    
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        const eventMatch = line.match(/event: (.+)\ndata: (.+)/);
        if (eventMatch) {
          const eventType = eventMatch[1];
          const data = JSON.parse(eventMatch[2]);
          
          handleEvent(eventType, data);
          
          // Connection closes when it's our turn again
          if (eventType === 'your_turn') {
            enableInput(); // Let player take their next action
            return;
          }
        }
      }
    }
  }
}

function handleEvent(eventType, data) {
  switch(eventType) {
    case 'action_confirmed':
      console.log('My action was processed:', data);
      disableInput(); // Wait for turn to come back
      break;
      
    case 'turn_start':
      displayTurnIndicator(data.playerName);
      break;
      
    case 'message':
      addMessageToChat(data);
      break;
      
    case 'dice':
      addDiceRollToChat(data);
      break;
      
    case 'stat_update':
      updatePlayerStats(data.playerId, data.stats);
      break;
      
    case 'dm_message':
      addDMMessageToChat(data);
      break;
      
    case 'your_turn':
      showTurnNotification();
      break;
  }
}

// Example: Player clicks "Send Message"
document.getElementById('sendBtn').onclick = () => {
  const text = document.getElementById('messageInput').value;
  takeTurn({
    type: 'message',
    text: text
  });
};

// Example: Player clicks "Roll d20"
document.getElementById('d20Btn').onclick = () => {
  takeTurn({
    type: 'dice',
    sides: 20,
    modifier: 3,
    reason: 'Initiative'
  });
};
```

## Server Implementation (Node.js/Express)

```javascript
const express = require('express');
const app = express();

// Game state
const games = {
  "game-abc123": {
    players: [
      { id: 1, name: "Thorin", ... },
      { id: 2, name: "Elara", ... },
      { id: 3, name: "Finn", ... },
      { id: 4, name: "Lyra", ... }
    ],
    currentTurnIndex: 0, // Whose turn it is (0-3)
    waitingConnections: [], // SSE connections for players waiting
    turnQueue: [] // Actions waiting to be processed
  }
};

app.post('/api/game/:gameId/turn', async (req, res) => {
  const { gameId } = req.params;
  const { playerId, action } = req.body;
  const game = games[gameId];
  
  // Verify it's this player's turn
  const currentPlayer = game.players[game.currentTurnIndex];
  if (currentPlayer.id !== playerId) {
    return res.status(403).json({ error: "Not your turn" });
  }
  
  // Set up SSE stream
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive'
  });
  
  // Confirm action received
  sendEvent(res, 'action_confirmed', { playerId, action });
  
  // Process the action
  await processAction(game, playerId, action);
  
  // Broadcast to all waiting connections
  broadcastAction(game, playerId, action);
  
  // Move to next turn
  game.currentTurnIndex = (game.currentTurnIndex + 1) % 4;
  
  // Store this connection for future updates
  game.waitingConnections.push({ playerId, res });
  
  // Keep streaming updates until it's this player's turn again
  await waitForTurn(game, playerId, res);
});

async function waitForTurn(game, playerId, res) {
  return new Promise((resolve) => {
    const checkTurn = () => {
      const currentPlayer = game.players[game.currentTurnIndex];
      
      if (currentPlayer.id === playerId) {
        // It's their turn again!
        sendEvent(res, 'your_turn', { 
          playerId, 
          playerName: currentPlayer.name 
        });
        sendEvent(res, 'close', {});
        res.end();
        
        // Remove from waiting connections
        game.waitingConnections = game.waitingConnections.filter(
          c => c.playerId !== playerId
        );
        
        resolve();
      }
    };
    
    // Check whenever a turn completes
    game.onTurnComplete = checkTurn;
  });
}

function sendEvent(res, event, data) {
  res.write(`event: ${event}\n`);
  res.write(`data: ${JSON.stringify(data)}\n\n`);
}

function broadcastAction(game, playerId, action) {
  const player = game.players.find(p => p.id === playerId);
  
  for (const connection of game.waitingConnections) {
    if (connection.playerId !== playerId) {
      // Send to other players
      if (action.type === 'message') {
        sendEvent(connection.res, 'message', {
          playerId,
          playerName: player.name,
          color: player.color,
          text: action.text,
          timestamp: new Date().toISOString()
        });
      } else if (action.type === 'dice') {
        const roll = Math.floor(Math.random() * action.sides) + 1;
        sendEvent(connection.res, 'dice', {
          playerId,
          playerName: player.name,
          color: player.color,
          sides: action.sides,
          roll: roll,
          timestamp: new Date().toISOString()
        });
      }
    }
  }
}
```

## Flow Example

**Turn 1 - Thorin's Turn:**
```
1. Thorin: POST /turn with "I attack!" 
   → Server confirms
   → Server broadcasts to Elara, Finn, Lyra
   → Thorin's connection stays open, waiting...

2. Elara's turn begins
   → All waiting connections get "turn_start: Elara"
   
3. Elara: POST /turn with dice roll
   → Server broadcasts roll to everyone
   → Elara's connection stays open
   
4. Finn's turn, Lyra's turn...

5. Back to Thorin's turn
   → Server sends "your_turn" to Thorin
   → Thorin's connection closes
   → Thorin can now POST again
```

## Advantages

✅ **Simple** - Only ONE endpoint to implement  
✅ **Efficient** - No polling, updates pushed immediately  
✅ **Turn-based** - Perfect for D&D's structure  
✅ **HTTP-based** - No WebSocket complexity  
✅ **Firewall-friendly** - Standard HTTP POST  
✅ **Stateful** - Server naturally tracks turn order

## Edge Cases

**Player disconnects mid-turn:**
- Their connection drops
- Server auto-passes their turn after 60s timeout
- They can rejoin and POST when it's their turn again

**Player tries to act out of turn:**
- Server returns 403 Forbidden
- Client shows "Wait for your turn"

**Multiple actions in one turn:**
- Use `type: "multiple"` with array of actions
- All execute atomically during that turn

This design perfectly matches D&D's turn-based nature!