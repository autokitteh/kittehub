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
    """A list of players in the game, indexed by player ID."""

    _ai_histories: dict[int | None, Sequence] = {None: []}
    """History of AI interactions per player ID. None is for the DM."""

    _ai_last_seen_event_index: dict[int | None, int] = {None: 0}
    """The last event index seen by each AI participant."""

    _events: list[protocol.SSEEvent] = []
    """All events that have occurred in the game."""

    def turn(self, req: protocol.TurnRequest) -> _SSEEventGenerator:
        h: _SSEEventGenerator | None = None

        match a := req.action:
            case protocol.JoinAction():
                h = self._on_join(a)
            case protocol.MessageAction():
                h = self._on_message(a)
            case _:
                yield protocol.DMMessageEvent(text="Action not implemented yet.")

        for event in h or []:
            self._events.append(event)
            yield event

    def _on_join(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        """Effectively starts the game."""
        if self._players:
            yield protocol.DMMessageEvent(text="Game already started, cannot join.")
            return

        yield from self._create_players(a)

        yield protocol.ThinkingEvent(who="DM")

        yield from self._dm()

    def _create_players(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        for i in range(a.player_count):
            print("Creating player", i)

            if i == 0:
                cls, race, name = a.class_name, a.race, a.player_name
            else:
                cls, race, name = data.random_character_attrs()

            yield protocol.ThinkingEvent(who="DM", message="generating stats")

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
            self._ai_histories[i] = []
            self._ai_last_seen_event_index[i] = 0

            yield protocol.PlayerJoinedEvent(player=player, is_you=i == 0)

    def _on_message(self, a: protocol.MessageAction) -> _SSEEventGenerator:
        yield protocol.MessageEvent(text=a.text, player_id=0)
        yield from self._dm()

    def _dm(self) -> _SSEEventGenerator:
        more = True

        while more:
            yield protocol.ThinkingEvent(who="DM")

            result, self._ai_histories[None] = ai.next_dm_event(
                self._events[self._ai_last_seen_event_index[None] :],
                self._players,
                self._ai_histories[None],
            )

            self._ai_last_seen_event_index[None] = len(self._events)

            event, more = result.event, result.more

            match event:
                case protocol.StatUpdateEvent(player_id=player_id, stats=stats):
                    if player_id >= len(self._players):
                        print("ERROR: StatUpdateEvent for unknown player", player_id)
                        continue
                    else:
                        self._players[player_id].stats = protocol.PlayerStats(**stats)

            yield event
