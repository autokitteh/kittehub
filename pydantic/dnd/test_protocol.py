"""Tests for D&D Chat Protocol - Server-Sent Events Message Definitions"""

import json

import protocol
from protocol import ActionConfirmedEvent
from protocol import CloseEvent
from protocol import DiceEvent
from protocol import DMMessageEvent
from protocol import MessageEvent
from protocol import Player
from protocol import PlayerJoinedEvent
from protocol import PlayerStats
from protocol import StatUpdateEvent
from protocol import TurnRequest
from protocol import TurnStartEvent
from protocol import YourTurnEvent


# Test helper functions
def create_warrior(player_id: int, name: str) -> Player:
    """Create a warrior character"""
    return Player(
        id=player_id,
        name=name,
        class_name="Warrior",
        color="#c0392b",
        stats=PlayerStats(
            hp=45,
            max_hp=45,
            ac=18,
            strength=16,
            dex=12,
            con=15,
            intelligence=10,
            wis=11,
            cha=9,
        ),
    )


def create_mage(player_id: int, name: str) -> Player:
    """Create a mage character"""
    return Player(
        id=player_id,
        name=name,
        class_name="Mage",
        color="#2980b9",
        stats=PlayerStats(
            hp=28,
            max_hp=28,
            ac=12,
            strength=8,
            dex=14,
            con=12,
            intelligence=18,
            wis=13,
            cha=10,
        ),
    )


def create_rogue(player_id: int, name: str) -> Player:
    """Create a rogue character"""
    return Player(
        id=player_id,
        name=name,
        class_name="Rogue",
        color="#27ae60",
        stats=PlayerStats(
            hp=32,
            max_hp=32,
            ac=15,
            strength=10,
            dex=18,
            con=13,
            intelligence=12,
            wis=14,
            cha=11,
        ),
    )


def create_cleric(player_id: int, name: str) -> Player:
    """Create a cleric character"""
    return Player(
        id=player_id,
        name=name,
        class_name="Cleric",
        color="#f39c12",
        stats=PlayerStats(
            hp=38,
            max_hp=38,
            ac=16,
            strength=14,
            dex=10,
            con=14,
            intelligence=11,
            wis=17,
            cha=13,
        ),
    )


class TestCharacterCreation:
    """Test character creation helper functions"""

    def test_create_warrior(self):
        player = create_warrior(1, "Alice")
        assert player.id == 1
        assert player.name == "Alice"
        assert player.class_name == "Warrior"
        assert player.color == "#c0392b"
        assert player.stats.hp == 45
        assert player.stats.max_hp == 45
        assert player.stats.ac == 18
        assert player.stats.strength == 16

    def test_create_mage(self):
        player = create_mage(2, "Bob")
        assert player.id == 2
        assert player.name == "Bob"
        assert player.class_name == "Mage"
        assert player.color == "#2980b9"
        assert player.stats.intelligence == 18
        assert player.stats.ac == 12

    def test_create_rogue(self):
        player = create_rogue(3, "Carol")
        assert player.id == 3
        assert player.name == "Carol"
        assert player.class_name == "Rogue"
        assert player.color == "#27ae60"
        assert player.stats.dex == 18

    def test_create_cleric(self):
        player = create_cleric(4, "Dave")
        assert player.id == 4
        assert player.name == "Dave"
        assert player.class_name == "Cleric"
        assert player.color == "#f39c12"
        assert player.stats.wis == 17


class TestSSEEventSerialization:
    """Test SSE event serialization to proper format"""

    def test_player_joined_event(self):
        player = create_warrior(1, "Alice")
        event = PlayerJoinedEvent(player=player, is_you=True)
        serialized = event.serialized

        # Check format
        assert serialized.startswith("event: player_joined\n")
        assert "data: " in serialized
        assert serialized.endswith("\n\n")

        # Parse the data line
        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["isYou"] is True
        assert data["player"]["name"] == "Alice"
        assert data["player"]["class"] == "Warrior"
        assert data["player"]["stats"]["maxHp"] == 45

    def test_message_event(self):
        event = MessageEvent.create(
            player_id=1,
            player_name="Alice",
            player_color="#c0392b",
            text="I attack the goblin!",
        )
        serialized = event.serialized

        assert serialized.startswith("event: message\n")
        assert "data: " in serialized

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 1
        assert data["playerName"] == "Alice"
        assert data["playerColor"] == "#c0392b"
        assert data["text"] == "I attack the goblin!"
        assert "timestamp" in data

    def test_dice_event(self):
        event = DiceEvent.create(
            player_id=1,
            player_name="Alice",
            player_color="#c0392b",
            sides=20,
            roll=18,
            modifier=5,
            reason="Attack roll",
        )
        serialized = event.serialized

        assert serialized.startswith("event: dice\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 1
        assert data["playerName"] == "Alice"
        assert data["sides"] == 20
        assert data["roll"] == 18
        assert data["modifier"] == 5
        assert data["total"] == 23
        assert data["reason"] == "Attack roll"

    def test_dice_event_without_modifier(self):
        event = DiceEvent.create(
            player_id=1,
            player_name="Alice",
            player_color="#c0392b",
            sides=6,
            roll=4,
        )

        data_line = event.serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["roll"] == 4
        assert "modifier" not in data  # exclude_none should remove it
        assert "total" not in data

    def test_stat_update_event(self):
        event = StatUpdateEvent(
            player_id=1, player_name="Alice", stats={"hp": 38, "maxHp": 45}
        )
        serialized = event.serialized

        assert serialized.startswith("event: stat_update\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 1
        assert data["playerName"] == "Alice"
        assert data["stats"]["hp"] == 38
        assert data["stats"]["maxHp"] == 45

    def test_dm_message_event(self):
        event = DMMessageEvent.create("The goblin falls defeated! You gain 50 XP.")
        serialized = event.serialized

        assert serialized.startswith("event: dm_message\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["text"] == "The goblin falls defeated! You gain 50 XP."
        assert "timestamp" in data

    def test_turn_start_event(self):
        event = TurnStartEvent(player_id=2, player_name="Bob", color="#2980b9")
        serialized = event.serialized

        assert serialized.startswith("event: turn_start\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 2
        assert data["playerName"] == "Bob"
        assert data["color"] == "#2980b9"

    def test_your_turn_event(self):
        event = YourTurnEvent(player_id=1, player_name="Alice")
        serialized = event.serialized

        assert serialized.startswith("event: your_turn\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 1
        assert data["playerName"] == "Alice"

    def test_close_event(self):
        event = CloseEvent()
        serialized = event.serialized

        assert serialized == "event: close\ndata: {}\n\n"

    def test_action_confirmed_event(self):
        event = ActionConfirmedEvent(
            player_id=1, action={"type": "message", "text": "Hello"}
        )
        serialized = event.serialized

        assert serialized.startswith("event: action_confirmed\n")

        data_line = serialized.split("\n")[1]
        data_json = data_line.replace("data: ", "")
        data = json.loads(data_json)

        assert data["playerId"] == 1
        assert data["action"]["type"] == "message"
        assert data["action"]["text"] == "Hello"


class TestRequestParsing:
    """Test parsing incoming requests"""

    def test_parse_join_request(self):
        request_data = {
            "action": {"type": "join", "playerName": "Alice", "playerCount": 3},
        }
        request = TurnRequest(**request_data)

        assert request.action.type == "join"
        assert isinstance(request.action, protocol.JoinAction)
        assert request.action.player_name == "Alice"
        assert request.action.player_count == 3

    def test_parse_message_request(self):
        request_data = {
            "playerId": 1,
            "action": {"type": "message", "text": "Hello!"},
        }
        request = TurnRequest(**request_data)

        assert request.action.type == "message"
        assert isinstance(request.action, protocol.MessageAction)
        assert request.action.text == "Hello!"
        assert request.player_id == 1

    def test_parse_dice_request(self):
        request_data = {
            "playerId": 1,
            "action": {"type": "dice", "sides": 20, "modifier": 3, "reason": "Attack"},
        }
        request = TurnRequest(**request_data)

        assert request.action.type == "dice"
        assert isinstance(request.action, protocol.DiceAction)
        assert request.action.sides == 20
        assert request.action.modifier == 3
        assert request.action.reason == "Attack"

    def test_parse_unknown_action_type(self):
        """Unknown action types should raise validation error"""
        import pytest
        from pydantic import ValidationError

        request_data = {
            "playerId": 1,
            "action": {"type": "unknown_action"},
        }

        with pytest.raises(ValidationError) as exc_info:
            TurnRequest(**request_data)

        # Verify it's a union tag error (discriminated union validation)
        error_msg = str(exc_info.value).lower()
        assert "input tag" in error_msg or "union_tag" in error_msg


class TestPlayerStats:
    """Test player stats model"""

    def test_player_stats_serialization(self):
        stats = PlayerStats(
            hp=30,
            max_hp=40,
            ac=15,
            strength=14,
            dex=12,
            con=13,
            intelligence=10,
            wis=11,
            cha=9,
        )
        data = json.loads(stats.model_dump_json(by_alias=True))

        assert data["hp"] == 30
        assert data["maxHp"] == 40
        assert data["ac"] == 15
        assert data["str"] == 14
        assert data["int"] == 10

    def test_player_with_stats(self):
        player = Player(
            id=1,
            name="Test",
            class_name="Warrior",
            color="#fff",
            stats=PlayerStats(
                hp=30,
                max_hp=40,
                ac=15,
                strength=14,
                dex=12,
                con=13,
                intelligence=10,
                wis=11,
                cha=9,
            ),
        )
        data = json.loads(player.model_dump_json(by_alias=True))

        assert data["id"] == 1
        assert data["class"] == "Warrior"
        assert data["stats"]["maxHp"] == 40
        assert data["stats"]["str"] == 14
