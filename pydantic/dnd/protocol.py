"""D&D Chat Protocol - Server-Sent Events Message Definitions (Pydantic)

All message types for the streaming HTTP protocol, with automatic serialization.
Each message has a .serialized property that returns the SSE-formatted string.
"""

from typing import ClassVar, Literal

from pydantic import BaseModel
from pydantic import Field


class SSEEvent(BaseModel):
    """Base class for all Server-Sent Events

    Subclasses should define event_type as a ClassVar[str].
    """

    event_type: ClassVar[str]

    @property
    def serialized(self) -> str:
        r"""Returns the SSE-formatted string for this event.

        Format: event: type\ndata: json\n\n
        """
        event_str = f"event: {type(self).event_type}\n"
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
    model_name: str | None = Field(None, serialization_alias="modelName")
    """AI model name for this player. None for human players."""

    model_config = {"populate_by_name": True}


#
# Event Models (for server-sent events)
#


class PlayerJoinedEvent(SSEEvent):
    """A new player has joined the game.

    is_you indicates if this is the connecting player.
    """

    event_type: ClassVar[str] = "player_joined"

    player: Player
    is_you: bool = Field(..., serialization_alias="isYou")


class MessageEvent(SSEEvent):
    """A player sends a chat message"""

    event_type: ClassVar[str] = "message"

    player_id: int = Field(0, serialization_alias="playerId")
    text: str


class DiceEvent(SSEEvent):
    """A player rolls dice. Roll result is generated server-side."""

    event_type: ClassVar[str] = "dice"

    player_id: int = Field(..., serialization_alias="playerId")
    sides: int
    roll: int  # Server-generated result
    modifier: int | None = None
    total: int | None = None
    reason: str | None = None


class StatUpdateEvent(SSEEvent):
    """Player stats change (e.g., HP, AC)"""

    event_type: ClassVar[str] = "stat_update"

    player_id: int = Field(..., serialization_alias="playerId")
    player_name: str = Field(..., serialization_alias="playerName")
    stats: dict[str, int]  # Partial stats update


class DMMessageEvent(SSEEvent):
    """Dungeon Master narration.

    Can be from server AI or a fifth player acting as DM.
    """

    event_type: ClassVar[str] = "dm_message"

    text: str
    """Text of the DM message. Can use markdown formatting."""


class YourTurnEvent(SSEEvent):
    """Indicates it's this player's turn again.

    Triggers connection close on client side.
    """

    event_type: ClassVar[str] = "your_turn"


class ThinkingEvent(SSEEvent):
    """Indicates the server is processing something (e.g., AI generating stats)"""

    event_type: ClassVar[str] = "thinking"

    message: str = "thinking"
    who: str


#
# Request Models (for parsing incoming requests)
#


class JoinAction(BaseModel):
    """Join game action"""

    type: Literal["join"] = "join"
    player_name: str = Field(..., alias="playerName")
    race: str
    class_name: str = Field(..., alias="class")
    dm_model: str = Field(..., alias="dmModel")
    """AI model name for the Dungeon Master"""
    player_models: list[str] | None = Field(default_factory=list, alias="playerModels")
    """List of AI model names for each AI player (excluding the human player).
    Can be empty for human vs DM only. Total players = len(player_models) + 1"""

    model_config = {"populate_by_name": True}

    def model_post_init(self, __context):
        """Convert None to empty list after validation"""
        if self.player_models is None:
            self.player_models = []


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
