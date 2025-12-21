"""D&D Chat Protocol - Server-Sent Events Message Definitions (Pydantic)

All message types for the streaming HTTP protocol, with automatic serialization.
Each message has a .serialized property that returns the SSE-formatted string.
"""

from datetime import datetime, UTC
from typing import Any, Literal

from pydantic import BaseModel
from pydantic import Field


# ============================================================================
# Base Classes
# ============================================================================


class SSEEvent(BaseModel):
    """Base class for all Server-Sent Events"""

    @property
    def event_type(self) -> str:
        """Override in subclasses to specify event type"""
        raise NotImplementedError

    @property
    def serialized(self) -> str:
        r"""Returns the SSE-formatted string for this event.

        Format: event: type\ndata: json\n\n
        """
        event_str = f"event: {self.event_type}\n"
        event_str += f"data: {self.model_dump_json(exclude_none=True, by_alias=True)}\n"
        event_str += "\n"  # Blank line signals end of event
        return event_str


class PlayerStats(BaseModel):
    """Player statistics"""

    hp: int
    max_hp: int = Field(..., serialization_alias="maxHp")
    ac: int
    strength: int = Field(..., serialization_alias="str")
    dex: int
    con: int
    intelligence: int = Field(..., serialization_alias="int")
    wis: int
    cha: int

    model_config = {
        "populate_by_name": True  # Allow parsing with either name
    }


class Player(BaseModel):
    """Player information"""

    id: int
    name: str
    race: str
    class_name: str = Field(..., serialization_alias="class")
    color: str
    stats: PlayerStats

    model_config = {"populate_by_name": True}


# ============================================================================
# Event Messages
# ============================================================================


class ActionConfirmedEvent(SSEEvent):
    """Confirms the player's action was received.

    For dice rolls, includes the server-generated roll result.
    """

    player_id: int = Field(..., serialization_alias="playerId")
    action: dict[str, Any]

    @property
    def event_type(self) -> str:
        return "action_confirmed"


class PlayerJoinedEvent(SSEEvent):
    """A new player has joined the game.

    is_you indicates if this is the connecting player.
    """

    player: Player
    is_you: bool = Field(..., serialization_alias="isYou")

    @property
    def event_type(self) -> str:
        return "player_joined"


class TurnStartEvent(SSEEvent):
    """Indicates whose turn is starting"""

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")
    color: str

    @property
    def event_type(self) -> str:
        return "turn_start"


class MessageEvent(SSEEvent):
    """A player sends a chat message"""

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")
    player_color: str = Field(..., serialization_alias="playerColor")
    text: str
    timestamp: str

    @property
    def event_type(self) -> str:
        return "message"

    @classmethod
    def create(cls, player_id: int, player_name: str, player_color: str, text: str):
        """Convenience constructor that auto-generates timestamp"""
        return cls(
            player_id=player_id,
            player_name=player_name,
            player_color=player_color,
            text=text,
            timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        )


class DiceEvent(SSEEvent):
    """A player rolls dice. Roll result is generated server-side."""

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")
    player_color: str = Field(..., serialization_alias="playerColor")
    sides: int
    roll: int  # Server-generated result
    modifier: int | None = None
    total: int | None = None
    reason: str | None = None
    timestamp: str | None = None

    @property
    def event_type(self) -> str:
        return "dice"

    @classmethod
    def create(
        cls,
        player_id: int,
        player_name: str,
        player_color: str,
        sides: int,
        roll: int,
        modifier: int | None = None,
        reason: str | None = None,
    ):
        """Convenience constructor that auto-generates timestamp and total"""
        total = roll + (modifier or 0) if modifier else None
        return cls(
            player_id=player_id,
            player_name=player_name,
            player_color=player_color,
            sides=sides,
            roll=roll,
            modifier=modifier,
            total=total,
            reason=reason,
            timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        )


class StatUpdateEvent(SSEEvent):
    """Player stats change (e.g., HP, AC)"""

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")
    stats: dict[str, int]  # Partial stats update

    @property
    def event_type(self) -> str:
        return "stat_update"


class DMMessageEvent(SSEEvent):
    """Dungeon Master narration.

    Can be from server AI or a fifth player acting as DM.
    """

    text: str
    timestamp: str

    @property
    def event_type(self) -> str:
        return "dm_message"

    @classmethod
    def create(cls, text: str):
        """Convenience constructor that auto-generates timestamp"""
        return cls(
            text=text,
            timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        )


class YourTurnEvent(SSEEvent):
    """Indicates it's this player's turn again.

    Triggers connection close on client side.
    """

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")

    @property
    def event_type(self) -> str:
        return "your_turn"


class CloseEvent(SSEEvent):
    """Signals the stream is ending"""

    @property
    def event_type(self) -> str:
        return "close"

    @property
    def serialized(self) -> str:
        """Close event has empty data"""
        return "event: close\ndata: {}\n\n"


# ============================================================================
# Request Models (for parsing incoming requests)
# ============================================================================


class JoinAction(BaseModel):
    """Join game action"""

    type: Literal["join"] = "join"
    player_name: str = Field(..., alias="playerName")
    player_count: int = Field(..., alias="playerCount")
    race: str
    class_name: str = Field(..., alias="class")

    model_config = {"populate_by_name": True}


class MessageAction(BaseModel):
    """Send message action"""

    type: Literal["message"] = "message"
    text: str


class DiceAction(BaseModel):
    """Roll dice action (client sends, server generates roll)"""

    type: Literal["dice"] = "dice"
    sides: int
    modifier: int | None = None
    reason: str | None = None


class StatUpdateAction(BaseModel):
    """Update stats action"""

    type: Literal["stat_update"] = "stat_update"
    stats: dict[str, int]


class TurnRequest(BaseModel):
    """Request body for /api/game/:gameId/turn endpoint"""

    player_id: int | None = Field(None, alias="playerId")
    action: JoinAction | MessageAction | DiceAction | StatUpdateAction = Field(
        ..., discriminator="type"
    )

    model_config = {"populate_by_name": True}
