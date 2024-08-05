"""Ask the user what to do when a task fails (retry / abort).

If `wait_resp` is True, this function waits for the user's response.
It returns True if the user wants to retry the task, and False if
the user wants to abort the workflow.

If `wait_resp` is False, this function returns immediately
and its return value is meaningless.
"""

from pathlib import Path

import autokitteh
from autokitteh.slack import slack_client


slack = slack_client("slack_conn")


def ask_user(task_name: str, error: str, user_id: str, *, wait_resp: bool) -> bool:
    if wait_resp:
        sub = autokitteh.subscribe("slack_conn", 'event_type == "interaction"')

    message = f"The task `{task_name}` failed:\n\n`{error}`"
    blocks = Path("interactive_message.json.txt").read_text()
    blocks = blocks.replace("MESSAGE", message).replace("TASK_NAME", task_name)
    slack.chat_postMessage(channel=user_id, text="dummy text", blocks=blocks)

    # Event-driven approach: the user's response is handled by a different workflow.
    if not wait_resp:
        return False

    # Single-workflow approach: wait for and handle the user's response in this workflow.
    event = autokitteh.next_event(sub)
    autokitteh.unsubscribe(sub)
    return event.actions[0]["value"] == "retry"
