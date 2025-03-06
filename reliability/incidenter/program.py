"""Tracks Slack-reported incidents, integrating with Height and Zoom."""

import os
import re

from autokitteh import next_event, subscribe
from autokitteh.slack import normalize_channel_name
from autokitteh.slack import slack_client

import height
import zoom


_CHANNEL_PREFIX = os.getenv("SLACK_CHANNEL_PREFIX", "")

slack_client = slack_client("slack_conn")


def on_slack_app_mention(event):
    # Another option is to put this straight in the trigger definition as "filter".
    m = re.compile(r"^<.+?>\s*incident\s*(.*)").match(event.data.text)
    if not m:
        print("irrelevant")
        return

    incident = _start(event.data.user, event.data.channel, event.data.ts, m.group(1))

    _track(incident)


def _start(
    slack_user: str, trigger_channel_id: str, trigger_ts: str, title: str
) -> dict:
    task = height.create_task(title, "New incident created from slack", "inProgress")

    zoom_url = zoom.create_meeting(f"Incident: {title}")

    name = f"{_CHANNEL_PREFIX}{task['index']}_{normalize_channel_name(title)}"
    resp = slack_client.conversations_create(name=name, is_private=False)
    channel = resp.get("channel")

    slack_client.conversations_setTopic(
        channel=channel["id"],
        topic=f"⚠ Incident: {title}",
    )

    slack_client.conversations_setPurpose(
        channel=channel["id"],
        purpose=f"Task: {task['url']} | Zoom: {zoom_url}",
    )

    slack_client.conversations_invite(
        channel=channel["id"],
        users=slack_user,
    )

    slack_client.chat_postMessage(
        channel=trigger_channel_id,
        thread_ts=trigger_ts,
        text=f"""⚠⚠⚠ Started incident: {title}
Task created: {task["url"]}
Channel created: <#{channel["id"]}>
Zoom: {zoom_url}
""",
    )

    return {
        "title": title,
        "slack_user": slack_user,
        "trigger": {
            "channel_id": trigger_channel_id,
            "ts": trigger_ts,
        },
        "zoom_url": zoom_url,
        "channel": channel,
        "task": task,
    }


def _track(incident: dict):
    s = subscribe("slack", f"data.channel == '{incident['channel']['id']}'")

    while True:
        evt = next_event(s)
        text, user = evt.text.strip(), evt["user"]

        if not text.startswith("!"):
            continue

        parts = text[1:].strip().split(" ", 1)
        cmd = parts[0]
        rest = parts[1] if len(parts) > 1 else ""

        match cmd:
            case "abandon":
                slack_client.chat_postMessage(
                    channel=evt["channel"],
                    ts=evt["ts"],
                    text="abandoned.",
                )
                return
            case "resolve":
                _resolve(incident, user, rest)
                return
            case "note":
                _note(incident, user, rest)

                slack_client.reactions_add(
                    channel=evt["channel"],
                    timestamp=evt["ts"],
                    name="memo",
                )
            case _:
                slack_client.chat_postMessage(
                    channel=evt["channel"],
                    ts=evt["ts"],
                    text="unknown incident command.",
                )


def _resolve(incident: dict, slack_user: str, msg: str):
    text = "🎉 Incident resolved!"

    if msg:
        text += f"\nwith note from <@{slack_user}>: {msg}"

    slack_client.chat_postMessage(
        channel=incident["channel"]["id"],
        text=text,
    )

    slack_client.chat_postMessage(
        channel=incident["trigger"]["channel_id"],
        thread_ts=incident["trigger"]["ts"],
        text=text,
    )

    _note(incident, slack_user, msg)

    slack_client.reactions_add(
        channel=incident["trigger"]["channel_id"],
        timestamp=incident["trigger"]["ts"],
        name="white_check_mark",
    )


def _note(incident: dict, slack_user: str, msg: str):
    resp = slack_client.users_info(user=slack_user)

    height.add_task_message(
        incident["task"]["id"],
        f'{resp["user"]["name"]} via slack: "{msg}"',
    )
