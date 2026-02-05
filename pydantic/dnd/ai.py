"""Docstring for pydantic.dnd.game"""

from collections.abc import Sequence
import json
from os import getenv
from random import randint

from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel

from autokitteh.pydantic import pydantic_gateway_provider
import protocol
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai import RunContext


def _model(name: str):
    family = name.split("-")[0]

    model = {
        "gpt": ("openai", OpenAIModel),
        "claude": ("anthropic", AnthropicModel),
    }.get(family)

    if not model:
        raise ValueError(f"Unsupported model name: {name}")

    return model[1](
        name,
        provider=pydantic_gateway_provider("pydanticgw", model[0]),
    )

#
# DM
#

_dm_model = _model(getenv("DM_MODEL_NAME", "claude-sonnet-4-5"))


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
    deps_type=list[protocol.Player],
    system_prompt="""
You are the Dungeon Master running a D&D game.

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
    return ",".join(json.dumps(d.dict()) for d in ctx.deps)


@_dm_agent.tool_plain(name="roll_dice")
def _roll_dice(sides: int) -> int:
    return randint(1, sides)


def create_player_stats(cls: str, race: str) -> protocol.PlayerStats:
    return _player_stats_agent.run_sync(
        f"Create a D&D player of class {cls} and race {race}."
    ).output


def next_dm_event(
    recent_events: Sequence[protocol.SSEEvent],
    players: Sequence[protocol.Player],
    history: Sequence,
) -> tuple[DMResult, list]:
    result = _dm_agent.run_sync(
        (
            f"Recent events: {json.dumps([e.dict() for e in recent_events])}"
            if history
            else "This is the beginning of the game."
        )
        + "\nIt's your turn as DM.",
        deps=list(players),
        message_history=history,
    )
    return result.output, result.all_messages()


#
# Player
#

_player_model = _model(getenv("PLAYER_MODEL_NAME", "claude-sonnet-4-5"))

_player_agent = Agent(
    _player_model,
    output_type=str,
    system_prompt="""
You are a D&D player participating in a game.
Respond to the Dungeon Master's messages and other events appropriately.
Keep your responses concise and in character.
NEVER roll a dice yourself - only the DM can do that, ask the DM to roll dice for you.
""",
)

_player_stats_agent = Agent(_player_model, output_type=protocol.PlayerStats)


def next_player_event(
    recent_events: Sequence[protocol.SSEEvent],
    player: protocol.Player,
    history: Sequence,
) -> tuple[str, list]:
    result = _player_agent.run_sync(
        f"""
You are player {player.name}. Here is your full information:
{json.dumps(player.dict())}

Recent events: {json.dumps([e.dict() for e in recent_events])}.

It's your turn to respond.
        """,
        message_history=history,
    )
    return result.output, result.all_messages()
