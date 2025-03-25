"""Entrypoint when using from AutoKitteh with Slack."""

from autokitteh import next_event, subscribe
from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError


slack = slack_client("slack_conn")

_ch = None
_ts = None
_subscription = None


def init(ch: str, ts: str):
    """Initialize the Slack channel and thread timestamp."""
    global _ch, _ts, _subscription

    _subscription = subscribe(
        "slack_conn",
        f"data.type == 'message' && data.bot_id == '' && data.thread_ts == '{ts}'",
    )

    _ch = ch
    _ts = ts


def _lookup_user(who: str) -> dict[str, any]:
    user_id = who
    if who.startswith("<@"):
        user_id = who[2:-1]
    elif who.startswith("@"):
        user_id = who[1:]
    elif "@" in who:
        try:
            user_id = slack.users_lookupByEmail(email=who)["user"]["id"]
        except SlackApiError as e:
            print(f"error: {e}")
            return None
    else:
        return None

    try:
        user = slack.users_info(user=user_id).get("user")
    except SlackApiError as e:
        print(f"error: {e}")
        return None

    print(f"lookup: {who} -> {user}")

    return user


def _post(text: str, user_id: str | None = None):
    ch, ts = _ch, _ts
    if user_id:
        ch, ts = user_id, None

    print(f"{ch}{(',' + ts) if ts else ''}: {text}")
    slack.chat_postMessage(channel=ch, text=text, thread_ts=ts)


def send(content: any, who: str | None = None):
    print(f"send: {who} <- {content}")
    if who:
        who = _lookup_user(who)
        if not who:
            _post(f"Sorry, I couldn't find the user {who}.")
            return

        who = who.get("id")

    _post(str(content), who)


def next_input():
    event = next_event(_subscription)
    if event is None:
        raise EOFError

    print(f"Q: {event.text}")

    return event.text


def ask(what: str, who: str, t: int | None = None) -> tuple[str, str]:
    user = _lookup_user(who)
    if not user:
        _post(f"Sorry, I couldn't find the user {who}.")
        return None, None

    user_id = user.get("id")

    send(f"❓ <@{user_id}>: {what}")

    while True:
        event = next_event(_subscription, timeout=t)
        if not event:
            return user, None

        if event.user == user_id:
            return user, event.text

        _post("Sorry, only the person mentioned can respond.")
