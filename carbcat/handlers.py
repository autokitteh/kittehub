"""Handlers for CarbCat events."""

from os import getenv

import ai
from autokitteh import del_value, Event, get_value, next_event, set_value, subscribe
from autokitteh.twilio import twilio_client


_twilio = twilio_client("twilio")

_TWILIO_PHONE_NUMBER = getenv("TWILIO_PHONE_NUMBER")


def _respond(to: str, msg: str) -> None:
    resp = _twilio.messages.create(
        body=msg,
        from_=f"whatsapp:{_TWILIO_PHONE_NUMBER}",
        to=f"{to}",
    )

    print(f"me: {msg}\n-> twilio: {resp}")


def on_whatsapp_message(event: Event):
    src = event.data.body.form.get("From")
    body = event.data.body.form.get("Body", "").strip()

    print(f"@{src}: {body}")

    if not src:
        print("no source specified.")
        return

    if not body:
        print("no body specified.")
        return

    if body == "/reset":
        del_value(src)
        _respond(src, "↺")
        return

    if get_value(src):
        print(f"already processing a request for {src}, ignoring new message")
        return

    set_value(src, True)

    try:
        _handle(body, src)
    except Exception:
        _respond(src, "Error processing your request, please try again later.")
        raise
    finally:
        del_value(src)


def _handle(body: str, to: str) -> None:
    s = subscribe("whatsapp_message", filter=f"data.body.form.From.startsWith('{to}')")

    def get_next() -> str:
        print(f"waiting for next user message from {to}...")
        evt = next_event(s)
        return evt["body"]["form"]["Body"]

    def say(msg: str) -> None:
        return _respond(to, msg)

    resp = ai.interact(body, get_next, say)
    if resp is None:
        say("Could not determine food item. Please try again.")
        return

    food, portion, amount = resp

    total_carbs = amount * food.carbs * (portion.gram_weight / 100.0)

    say(
        f"{amount} x {portion.amount} {portion.modifier} of {food.name} "
        f"({portion.gram_weight}g each) contains approximately "
        f"{total_carbs:.2f}g of carbohydrates."
    )
