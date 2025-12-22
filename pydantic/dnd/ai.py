"""Docstring for pydantic.dnd.game"""

from collections.abc import Sequence
import json
from os import getenv
from random import randint

from pydantic_ai.models.anthropic import AnthropicModel

from autokitteh.anthropic import anthropic_pydantic_ai_provider
import protocol
from pydantic_ai import Agent
from pydantic_ai import RunContext


_DM_MODEL_NAME = getenv("DM_MODEL_NAME", "claude-sonnet-4-5")
_PLAYER_MODEL_NAME = getenv("PLAYER_MODEL_NAME", "claude-sonnet-4-5")

_player_model = AnthropicModel(
    _PLAYER_MODEL_NAME, provider=anthropic_pydantic_ai_provider("anthropic")
)

_player_stats_agent = Agent(_player_model, output_type=protocol.PlayerStats)

_dm_model = AnthropicModel(
    _DM_MODEL_NAME,
    provider=anthropic_pydantic_ai_provider("anthropic"),
)

DM_RESPONSE_TYPES = (
    protocol.DMMessageEvent | protocol.DiceEvent | protocol.StatUpdateEvent
)

_dm_agent = Agent(
    _dm_model,
    output_type=DM_RESPONSE_TYPES,
    system_prompt="""
You are the Dungeon Master running a D&D game.

It's your turn as DM.

In each invocation, you must take one of the following actions:
1. Send a message to the players. Return a DMMessageEvent with the text of your message.
2. Roll a dice, by returning a DiceEvent with the result of the roll.
3. Update a player's stat, by returning a StatUpdateEvent.

After each time you take an action, the players will respond in turn.
The first player in the list goes first. Then the rest.

Tool available to you:
- list_players: Returns the list of all players and their stats in the game.
- roll_dice: Rolls a dice with the given number of sides and returns the result.

If this is the start of the game, introduce the setting and scenario to the players.
""",
)


@_dm_agent.tool(name="list_players")
def _list_players(ctx: RunContext[list[protocol.Player]]) -> str:
    return ctx.deps


@_dm_agent.tool(name="roll_dice")
def _roll_dice(sides: int) -> int:
    return randint(1, sides)


def create_player_stats(cls: str, race: str) -> protocol.Player:
    return _player_stats_agent.run_sync(
        f"Create a D&D player of class {cls} and race {race}."
    ).output


def next_dm_event(
    turn_summary: list[protocol.MessageAction | protocol.JoinAction],
    players: list[protocol.Player],
    history: Sequence,
) -> tuple[DM_RESPONSE_TYPES, Sequence]:
    result = _dm_agent.run_sync(
        f"Actions made since last turn: {json.dumps([a.dict() for a in turn_summary])}"
        if history
        else "This is the beginning of the game.",
        deps=players,
        message_history=history,
    )
    return result.output, result.all_messages()
