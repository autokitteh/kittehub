"""Handles Slack mentions and help requests, sending reminders if unresolved."""

from datetime import datetime, UTC
import os

import autokitteh
from autokitteh.slack import slack_client

import directory
import gemini


HELP_REQUEST_TIMEOUT_MINUTES = int(os.getenv("HELP_REQUEST_TIMEOUT_MINUTES"))

slack_client = slack_client("myslack")


def on_slack_mention(event):
    def send(text):
        """Helper function to just post some text back in the same thread."""
        slack_client.chat_postMessage(
            channel=event.data.channel,
            thread_ts=event.data.ts,
            text=text,
        )

        # prints are used for logging, and can be seen in the console output.
        print(f"sent: '{text}'")

    topics_to_people = directory.load()

    help, topic = gemini.extract_topic(event.data.text, topics_to_people.keys())
    if not help:
        return

    people = topics_to_people.get(topic)
    if not people:
        send(f"Sorry, I don't know who to ask about {topic}.")
        return

    mentions = ", ".join(f"<@{p.slack_id}>" for p in people)

    send(f"""People who can help are: {mentions}.
Responders: please reply in this thread with `!take` or `!resolve`.
If not taken or resolved, I will remind you in {HELP_REQUEST_TIMEOUT_MINUTES}m.
""")

    # From this point on we are interested in any message that is added to the thread.
    # Further below we'll consume the messages and act on them using `next_event`.
    filter = "data.type == 'message' && data.thread_ts == "
    filter += f"'{event.data.ts}' && data.text.startsWith('!')"
    s = autokitteh.subscribe("myslack", filter)

    taken_by = None
    start_time = datetime.now(UTC)

    while True:
        msg = autokitteh.next_event(s, timeout=60)

        if not msg:  # timeout
            dt = (datetime.now(UTC) - start_time).total_seconds()
            print(f"timeout, dt={dt}")

            if not taken_by and dt >= HELP_REQUEST_TIMEOUT_MINUTES * 60:
                send(f"Reminder: {mentions}, please respond.")
                start_time = datetime.now(UTC)
            continue

        cmd = msg.text.strip()[1:]
        if cmd == "resolve":
            send("Issue is now resolved.")
            # this effectively ends the workflow.
            return
        if cmd == "take":
            taken_by = msg.user
            send(f"Thanks <@{msg.user}>, you've taken this issue.")
