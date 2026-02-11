"""Docstring for pydantic.dnd.game"""

from collections.abc import Generator
from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import field
import random

import ai
import data
import protocol


_SSEEventGenerator = Generator[protocol.SSEEvent, None, None]


class Game:
    """Game context"""

    @dataclass
    class Participant:
        """Manages AI context for a single participant (DM or player).

        Encapsulates message history, event tracking, and player data.
        """

        player: protocol.Player | None = None
        """Player data. None for the DM."""

        message_history: Sequence = field(default_factory=list)
        """AI message history for prompt caching."""

        last_processed_event_index: int = 0
        """Index of the last event this participant has processed."""

        def get_new_events(
            self, all_events: list[protocol.SSEEvent]
        ) -> list[protocol.SSEEvent]:
            """Returns events that haven't been processed yet."""
            return all_events[self.last_processed_event_index :]

        def update_after_processing(
            self,
            new_history: Sequence,
            total_events: int,
        ) -> None:
            """Updates state after processing a turn."""
            self.message_history = new_history
            self.last_processed_event_index = total_events

    _participants: dict[int | None, Participant] = {None: Participant()}
    """Participants in the game. None is for the DM, integers for players."""

    _events: list[protocol.SSEEvent] = []
    """All events that have occurred in the game."""

    @property
    def _players(self) -> list[protocol.Player]:
        """Returns list of all players (excludes DM)."""
        return [
            p.player
            for key, p in sorted(self._participants.items(), key=lambda p: p[0] or -1)
            if key is not None and p.player is not None
        ]

    def turn(self, req: protocol.TurnRequest) -> _SSEEventGenerator:
        h: _SSEEventGenerator | None = None

        match a := req.action:
            case protocol.JoinAction():
                h = self._on_join(a)
            case protocol.MessageAction():
                h = self._on_message(a)
            case protocol.SyncAction():
                h = self._on_sync()
            case _:
                yield protocol.DMMessageEvent(text="Action not implemented yet.")

        for event in h or []:
            if type(event).event_type != protocol.ThinkingEvent.event_type:
                self._events.append(event)

            yield event

    def _on_join(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        """Effectively starts the game."""
        if self._players:
            yield protocol.DMMessageEvent(text="Game already started, cannot join.")
            return

        yield from self._create_players(a)

        # Initialize all AI agents after players are created
        ai.init_dm_agent(a.dm_model)
        for player_id, participant in self._participants.items():
            if (player_id is not None
                and participant.player
                and participant.player.model_name):
                ai.init_player_agent(player_id, participant.player.model_name)

        yield protocol.ThinkingEvent(who="DM")

        yield from self._dm()

    def _create_players(self, a: protocol.JoinAction) -> _SSEEventGenerator:
        assert a.player_models

        player_count = len(a.player_models) + 1  # Human + AI players

        for i in range(player_count):
            print("Creating player", i)

            if i == 0:
                cls, race, name = a.class_name, a.race, a.player_name
                model_name = None  # Human player
                stats_model = a.dm_model  # Use DM's model for human player stats
            else:
                cls, race, name = data.random_character_attrs()
                model_name = a.player_models[i - 1]  # AI player model
                stats_model = model_name  # Use player's model for their stats

            yield protocol.ThinkingEvent(who="DM", message="generating stats")

            stats = ai.create_player_stats(cls, race, stats_model)

            player = protocol.Player(
                id=i,
                name=name,
                class_name=cls,
                race=race,
                stats=stats,
                color=f"#{random.randint(0, 0xFFFFFF):06x}",
                model_name=model_name,
            )

            print("Created player:", player)

            self._participants[i] = Game.Participant(player)

            yield protocol.PlayerJoinedEvent(player=player, is_you=i == 0)

    def _on_message(self, a: protocol.MessageAction) -> _SSEEventGenerator:
        # Put player's message in the log.
        yield protocol.MessageEvent(text=a.text, player_id=0)

        # Other players respond in order.
        for i in range(1, len(self._players)):
            yield from self._player(i)

        # DM responds to all.
        yield from self._dm()

    def _on_sync(self) -> _SSEEventGenerator:
        """Handle sync request - return current game state or not started."""
        if not self._players:
            yield protocol.GameNotStartedEvent()
            return

        # Convert events to history items
        history = [self._event_to_history_item(event) for event in self._events]

        # Return game state
        yield protocol.GameStateEvent(
            players=self._players,
            history=[h for h in history if h],
            your_player_id=0,  # Always player 0 for now (human player)
            is_your_turn=True,  # Always their turn after sync
        )

    @staticmethod
    def _event_to_history_item(event: protocol.SSEEvent) -> protocol.HistoryItem | None:
        """Convert an SSE event to a history item."""
        match event:
            case protocol.MessageEvent(player_id=pid, text=text):
                return protocol.HistoryItem(type="message", player_id=pid, text=text)
            case protocol.DMMessageEvent(text=text):
                return protocol.HistoryItem(type="dm_message", text=text)
            case protocol.DiceEvent(
                player_id=pid,
                sides=sides,
                roll=roll,
                modifier=modifier,
                total=total,
                reason=reason,
            ):
                return protocol.HistoryItem(
                    type="dice",
                    player_id=pid,
                    sides=sides,
                    roll=roll,
                    modifier=modifier,
                    total=total,
                    reason=reason,
                )
            case protocol.StatUpdateEvent(player_id=pid, player_name=name, stats=stats):
                return protocol.HistoryItem(
                    type="stat_update", player_id=pid, player_name=name, stats=stats
                )
            case _:
                # Skip events that aren't part of history
                # (thinking, player_joined, etc.)
                return None

    def _dm(self) -> _SSEEventGenerator:
        more = True
        dm_participant = self._participants[None]

        while more:
            yield protocol.ThinkingEvent(who="DM")

            result, new_history = ai.next_dm_event(
                dm_participant.get_new_events(self._events),
                self._players,
                dm_participant.message_history,
            )

            dm_participant.update_after_processing(new_history, len(self._events))

            event, more = result.event, result.more

            match event:
                case protocol.StatUpdateEvent(player_id=player_id, stats=stats):
                    participant = self._participants.get(player_id)
                    if not participant or not participant.player:
                        print("ERROR: StatUpdateEvent for unknown player", player_id)
                        continue
                    else:
                        participant.player.stats = stats

            yield event

    def _player(self, id: int) -> _SSEEventGenerator:
        participant = self._participants[id]

        assert participant.player

        yield protocol.ThinkingEvent(who=participant.player.name)

        msg, new_history = ai.next_player_event(
            id,
            participant.get_new_events(self._events),
            participant.player,
            participant.message_history,
        )

        participant.update_after_processing(new_history, len(self._events))

        yield protocol.MessageEvent(text=msg, player_id=id)
