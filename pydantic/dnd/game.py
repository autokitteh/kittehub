"""Docstring for pydantic.dnd.game"""

from collections.abc import Generator
from collections.abc import Sequence
import random

import ai
import data
import protocol


_SSEEventGenerator = Generator[protocol.SSEEvent, None, None]


class Game:
    """Game context"""

    _players: list[protocol.Player] = []
    _dm_history: Sequence = []
    _players_histories: dict[int, Sequence] = {}

    def turn(self, req: protocol.TurnRequest) -> _SSEEventGenerator:
        match a := req.action:
            case protocol.JoinAction():
                yield from self._on_join(a)
            case protocol.MessageAction():
                yield from self._on_message(a)
            case _:
                yield protocol.MessageEvent(text="Action not implemented yet.")

    def _on_join(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        """Effectively starts the game."""
        if self._players:
            yield protocol.MessageEvent(
                text="Game already started, cannot join.", player_id=None
            )
            return

        yield from self._create_players(a)

        yield protocol.ThinkingEvent()

        event, self._dm_history = ai.next_dm_event(
            [protocol.PlayerJoinedEvent(player=p, is_you=False) for p in self._players],
            self._players,
            self._dm_history,
        )

        yield event

    def _create_players(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        for i in range(a.player_count):
            print("Creating player", i)

            if i == 0:
                cls, race, name = a.class_name, a.race, a.player_name
            else:
                cls, race, name = data.random_character_attrs()

            yield protocol.ThinkingEvent()

            stats = ai.create_player_stats(cls, race)

            player = protocol.Player(
                id=i,
                name=name,
                class_name=cls,
                race=race,
                stats=stats,
                color=f"#{random.randint(0, 0xFFFFFF):06x}",
            )

            print("Created player:", player)

            self._players.append(player)

            yield protocol.PlayerJoinedEvent(player=player, is_you=i == 0)

    def _on_message(self, a: protocol.MessageAction) -> _SSEEventGenerator:
        yield protocol.MessageEvent(text=a.text, player_id=0)

        yield protocol.ThinkingEvent()

        event, self._dm_history = ai.next_dm_event(
            [a],
            self._players,
            self._dm_history,
        )

        yield event
