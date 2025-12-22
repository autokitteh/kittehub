"""Docstring for pydantic.dnd.game"""

from collections.abc import Sequence
import json
from os import getenv
from random import randint

from pydantic_ai.models.anthropic import AnthropicModel

from autokitteh.anthropic import anthropic_pydantic_ai_provider
import logfire
import protocol
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai import RunContext


if getenv("LOGFIRE_TOKEN"):
    logfire.configure()
    logfire.instrument_anthropic()
    print("logfire configured.")


_DM_MODEL_NAME = getenv("DM_MODEL_NAME", "claude-sonnet-4-5")
_PLAYER_MODEL_NAME = getenv("PLAYER_MODEL_NAME", "claude-sonnet-4-5")

_player_model = AnthropicModel(
    _PLAYER_MODEL_NAME, provider=anthropic_pydantic_ai_provider("anthropic")
)

_player_stats_agent = Agent(_player_model, output_type=protocol.PlayerStats)

_player_agent = Agent(
    _player_model,
    output_type=protocol.MessageAction,
    system_prompt="""
Tools available to you:
- list_players: Returns the list of all players and their stats in the game.
""",
)


@_player_agent.tool(name="list_players")
def _list_players(ctx: RunContext[list[protocol.Player]]) -> str:
    return ctx.deps


_dm_model = AnthropicModel(
    _DM_MODEL_NAME,
    provider=anthropic_pydantic_ai_provider("anthropic"),
)


class DMResult(BaseModel):
    """Event returned by the DM agent and if it needs another turn immediately."""

    event: protocol.DMMessageEvent | protocol.DiceEvent | protocol.StatUpdateEvent
    """The event the DM decided to take this turn."""

    more: bool
    """True if the DM needs another turn immediately.
    For example - if the DM rolled a dice and now wants to send a message based on
    the result."""


_dm_agent = Agent(
    _dm_model,
    output_type=DMResult,
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


@_dm_agent.tool_plain(name="roll_dice")
def _roll_dice(sides: int) -> int:
    return randint(1, sides)


def create_player_stats(cls: str, race: str) -> protocol.Player:
    return _player_stats_agent.run_sync(
        f"Create a D&D player of class {cls} and race {race}."
    ).output


def next_dm_event(
    acts: Sequence[protocol.MessageAction | protocol.JoinAction],
    players: Sequence[protocol.Player],
    history: Sequence,
) -> tuple[DMResult, Sequence]:
    result = _dm_agent.run_sync(
        f"Actions made: {json.dumps([a.dict() for a in acts])}"
        if history
        else "This is the beginning of the game.",
        deps=players,
        message_history=history,
    )
    return result.output, result.all_messages()


def next_player_action(
    player_id: int,
    players: Sequence[protocol.Player],
    latest_events: Sequence[protocol.SSEEvent],
    history: Sequence,
) -> tuple[protocol.MessageAction, Sequence]:
    result = _player_agent.run_sync(
        f"""
You are player {player_id}.

Events that happened since your last turn:
{json.dumps([a.dict() for a in latest_events])}

It's your turn. What do you say or do? Keep it to 1-2 sentences.
Try to follow player 0's lead.
Respond naturally in character.
""",
        deps=players,
        message_history=history,
    )
    return result.output, result.all_messages()
