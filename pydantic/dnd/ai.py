"""Docstring for pydantic.dnd.game"""

from os import getenv

from pydantic_ai.models.anthropic import AnthropicModel

from autokitteh.anthropic import anthropic_pydantic_ai_provider
import protocol
from pydantic_ai import Agent


_DM_MODEL_NAME = getenv("DM_MODEL_NAME", "claude-sonnet-4-5")
_PLAYER_MODEL_NAME = getenv("PLAYER_MODEL_NAME", "claude-sonnet-4-5")

_dm_model = AnthropicModel(
    _DM_MODEL_NAME, provider=anthropic_pydantic_ai_provider("anthropic")
)

_player_model = AnthropicModel(
    _PLAYER_MODEL_NAME, provider=anthropic_pydantic_ai_provider("anthropic")
)

_player_stats_agent = Agent(_player_model, output_type=protocol.PlayerStats)


def create_player_stats(cls: str, race: str) -> protocol.Player:
    return _player_stats_agent.run_sync(
        f"Create a D&D player of class {cls} and race {race}."
    ).output
