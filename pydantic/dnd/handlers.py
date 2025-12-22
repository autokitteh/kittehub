"""Simple Q&A using AI."""

from pathlib import Path

from autokitteh import Event, get_webhook_url, http_outcome, next_event, subscribe
import game
import protocol
from pydantic import ValidationError


_GAME_HTML = Path("game.html").read_text()

_API_ENDPOINT_URL = get_webhook_url("turn")


def on_game(event: Event, session_id: str) -> None:
    data = event.data

    if sid := data.url.path_suffix:
        _existing_game(sid)
    else:
        _new_game(session_id)


def _existing_game(session_id: str) -> None:
    http_outcome(404, "Not implemented yet.")


def _new_game(session_id: str) -> None:
    print(f"Starting new game with session ID: {session_id}")

    http_outcome(
        200,
        body=_GAME_HTML.replace(
            "{{API_ENDPOINT}}", f"{_API_ENDPOINT_URL}/{session_id}"
        ),
    )

    g = game.Game()

    s = subscribe("turn", f"data.url.path_suffix == '{session_id}'")

    while True:
        print("Waiting for next request...")
        event = next_event(s, full=True)

        body = event.data.body.json

        print(f"<- {body}")

        try:
            req = protocol.TurnRequest.model_validate(body)
        except ValidationError as e:
            print(f"Invalid request: {e}")
            http_outcome(400, f"Invalid request: {e}", event_id=event.id)
            continue

        if req.player_id:  # must be either None or 0.
            print(f"Only player ID 0 is supported, got: {req.player_id}")
            http_outcome(400, "Only player ID 0 is supported.", event_id=event.id)
            continue

        for update in g.turn(req):
            body = update.serialized
            print(f"-> {body}")
            http_outcome(body=body, more=True, event_id=event.event_id)

        http_outcome(body=protocol.YourTurnEvent().serialized, event_id=event.event_id)
