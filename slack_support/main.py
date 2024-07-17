import os
from datetime import datetime

import autokitteh
from autokitteh.slack import slack_client

import gemini
import directory

HELP_REQUEST_TIMEOUT_MINUTES = os.getenv("HELP_REQUEST_TIMEOUT_MINUTES")
HELP_REQUEST_IDLE_TIMEOUT_MINUTES = os.getenv("HELP_REQUEST_IDLE_TIMEOUT_MINUTES")

slack_client = slack_client("slack")


def on_slack_mention(event):
    def reply(text):
        slack_client.chat_postMessage(
            channel=event.data.channel,
            thread_ts=event.data.ts,
            text=text,
        )

    help, topic = gemini.extract_topic(event.data.text)
    if not help:
        return

    staff = directory.find_by_topic(topic)
    if not staff:
        reply(f"Sorry, I don't know who to ask about {topic}.")
        return

    mentions = ", ".join(f"<@{p[1]}>" for p in staff)

    response = f"""Sure, people who can help are: {mentions}.
Responders: please reply in this thread with `!take` or `!resolve`."""

    if HELP_REQUEST_TIMEOUT_MINUTES:
        response += (
            f"If not taken or resolved, I will remind you in f{HELP_REQUEST_TIMEOUT_MINUTES}m."
        )

    reply(response)

    t0 = datetime.now()

    s = autokitteh.subscribe(
        "slack",
        f'data.type == "message" && data.thread_ts == "{event.data.ts}" && data.text.startsWith("!")',
    )

    taken_by = None

    while True:
        msg = autokitteh.next_event(s, timeout=60)
        print(msg)

        if not msg:  # timeout
            dt = datetime.now().total_seconds() - t0.total_seconds()

            if taken_by:
                if dt >= HELP_REQUEST_IDLE_TIMEOUT_MINUTES:
                    reply(f"Reminder: <@{taken_by}>, please resolve if done.")
                    t0 = datetime.now()
            elif dt >= HELP_REQUEST_TIMEOUT_MINUTES:
                reply(f"Reminder: {mentions}, please respond.")
                t0 = datetime.now()
            continue

        cmd = msg.text.strip()[1:]
        if cmd == "resolve":
            reply("Issue is now resolved.")
            return
        if cmd == "take":
            taken_by = msg.user
            reply(f"Thanks <@{msg.user}>, you've taken this issue.")
