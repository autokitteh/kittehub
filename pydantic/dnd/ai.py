"""Docstring for pydantic.dnd.game"""

from collections.abc import Sequence
import json
from random import randint

from autokitteh import activity
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel

from autokitteh.pydantic import pydantic_gateway_provider
import protocol
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai import RunContext


def _model(name: str):
    """Return an AI model instance based on the given name.

    Return value is not picklable, so the caller should call this inside
    an explicit activity.
    """
    family = name.split("-")[0]

    model = {
        "gpt": ("openai", OpenAIModel),
        "claude": ("anthropic", AnthropicModel),
        "gemini": ("gemini", GeminiModel)
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


class DMResult(BaseModel):
    """Event returned by the DM agent and if it needs another turn immediately."""

    event: protocol.DMMessageEvent | protocol.DiceEvent | protocol.StatUpdateEvent
    """The event the DM decided to take this turn."""

    more: bool
    """True if the DM needs another turn immediately.
    For example - if the DM rolled a dice and now wants to send a message based on
    the result."""


def _list_players(ctx: RunContext[list[protocol.Player]]) -> str:
    return ",".join(json.dumps(d.dict()) for d in ctx.deps)


def _roll_dice(sides: int) -> int:
    return randint(1, sides)


# Global agent storage (avoid pickling by AutoKitteh)
_dm_agent: Agent | None = None
_player_agents: dict[int, Agent] = {}


@activity
def init_dm_agent(model_name: str) -> None:
    """Initialize the DM agent with the specified model."""
    global _dm_agent
    _dm_agent = Agent(
        _model(model_name),
        output_type=DMResult,
        deps_type=list[protocol.Player],
        tools=[
            _list_players,
            _roll_dice,
        ],
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


@activity
def create_player_stats(cls: str, race: str, model_name: str) -> protocol.PlayerStats:
    """Generate player stats using the specified model."""
    stats_agent = Agent(_model(model_name), output_type=protocol.PlayerStats)
    return stats_agent.run_sync(
        f"Create a D&D player of class {cls} and race {race}."
    ).output


def next_dm_event(
    recent_events: Sequence[protocol.SSEEvent],
    players: Sequence[protocol.Player],
    history: Sequence,
) -> tuple[DMResult, list]:
    assert _dm_agent

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


@activity
def init_player_agent(player_id: int, model_name: str) -> None:
    """Initialize a player agent with the specified model."""
    _player_agents[player_id] = Agent(
        _model(model_name),
        output_type=str,
        system_prompt="""
You are a D&D player participating in a game.
Respond to the Dungeon Master's messages and other events appropriately.
Keep your responses concise and in character.
NEVER roll a dice yourself - only the DM can do that, ask the DM to roll dice for you.
""",
    )


def next_player_event(
    player_id: int,
    recent_events: Sequence[protocol.SSEEvent],
    player: protocol.Player,
    history: Sequence,
) -> tuple[str, list]:
    agent = _player_agents.get(player_id)
    assert agent

    result = agent.run_sync(
        f"""
You are player {player.name}. Here is your full information:
{json.dumps(player.dict())}

Recent events: {json.dumps([e.dict() for e in recent_events])}.

It's your turn to respond.
        """,
        message_history=history,
    )
    return result.output, result.all_messages()
