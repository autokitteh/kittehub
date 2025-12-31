"""D&D Chat Protocol - Server-Sent Events Message Definitions (Pydantic)

All message types for the streaming HTTP protocol, with automatic serialization.
Each message has a .serialized property that returns the SSE-formatted string.
"""

from typing import Literal

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


class PlayerJoinedEvent(SSEEvent):
    """A new player has joined the game.

    is_you indicates if this is the connecting player.
    """

    player: Player
    is_you: bool = Field(..., serialization_alias="isYou")

    @property
    def event_type(self) -> str:
        return "player_joined"


class MessageEvent(SSEEvent):
    """A player sends a chat message"""

    player_id: int = Field(0, serialization_alias="playerId")
    text: str

    @property
    def event_type(self) -> str:
        return "message"


class DiceEvent(SSEEvent):
    """A player rolls dice. Roll result is generated server-side."""

    player_id: int = Field(..., serialization_alias="playerId")
    sides: int
    roll: int  # Server-generated result
    modifier: int | None = None
    total: int | None = None
    reason: str | None = None

    @property
    def event_type(self) -> str:
        return "dice"


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
    """Text of the DM message. Can use markdown formatting."""

    @property
    def event_type(self) -> str:
        return "dm_message"


class YourTurnEvent(SSEEvent):
    """Indicates it's this player's turn again.

    Triggers connection close on client side.
    """

    @property
    def event_type(self) -> str:
        return "your_turn"


class ThinkingEvent(SSEEvent):
    """Indicates the server is processing something (e.g., AI generating stats)"""

    message: str = "thinking"
    who: str

    @property
    def event_type(self) -> str:
        return "thinking"


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
    """Text of the message to send. Can use markdown formatting."""


class TurnRequest(BaseModel):
    """Request body for /api/game/:gameId/turn endpoint"""

    player_id: int | None = Field(None, alias="playerId")
    action: JoinAction | MessageAction = Field(..., discriminator="type")

    model_config = {"populate_by_name": True}
