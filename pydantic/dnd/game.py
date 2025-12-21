"""Docstring for pydantic.dnd.game"""

from collections.abc import Generator
import random

import ai
import data
import protocol


_SSEEventGenerator = Generator[protocol.SSEEvent, None, None]


class Game:
    """Game context"""

    _players: list[protocol.Player] = []

    def turn(self, req: protocol.TurnRequest) -> _SSEEventGenerator:
        match a := req.action:
            case protocol.JoinAction():
                yield from self._join(a)
            case _:
                yield protocol.MessageEvent(message="Action not implemented yet.")

    def _join(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        if self._players:
            yield protocol.MessageEvent(
                message="Game already started, cannot join.", player_id=None
            )
            return

        yield from self._create_players(a)

    def _create_players(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        for i in range(a.player_count):
            print("Creating player", i)

            if i == 0:
                cls, race, name = a.class_name, a.race, a.player_name
            else:
                cls, race, name = data.random_character_attrs()

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
