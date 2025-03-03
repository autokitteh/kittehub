"""This module uses a single-workflow approach for the task-chain project.

A single workflow runs all the tasks, including retry loops.
It handles Slack interactions using runtime event subscriptions.
"""

from pathlib import Path
import random

import autokitteh
from autokitteh.slack import slack_client


slack = slack_client("slack_conn")


def step1():
    print("Step 1 is doing stuff...")


def step2():
    print("Step 2 is doing stuff...")


def step3():
    print("Step 3 is doing stuff...")
    if random.choice([True, False]):
        raise RuntimeError("Something bad happened")


def step4():
    print("Step 4 is doing stuff...")


def on_slack_slash_command(event):
    """Use a Slack slash command from a user to start a chain of tasks."""
    user_id = event.data.user_id

    if not run_retriable_task(step1, user_id):
        return
    if not run_retriable_task(step2, user_id):
        return
    if not run_retriable_task(step3, user_id):
        return
    if not run_retriable_task(step4, user_id):
        return

    message = "Workflow completed successfully :smiley_cat:"
    slack.chat_postMessage(channel=user_id, text=message)


def run_retriable_task(task, user_id) -> bool:
    result = True
    while result:
        try:
            task()
            break
        except RuntimeError as e:
            result = ask_user_retry_or_abort(task.__name__, e, user_id)

    if result:
        message = f"Task `{task.__name__}` completed"
        slack.chat_postMessage(channel=user_id, text=message)

    return result


def ask_user_retry_or_abort(task_name, error, user_id) -> bool:
    sub = autokitteh.subscribe("slack_conn", 'event_type == "interaction"')

    blocks = Path("interactive_message.json.txt").read_text()
    blocks = blocks.replace("MESSAGE", f"The task `{task_name}` failed: `{error}`")
    slack.chat_postMessage(channel=user_id, text="Workflow error", blocks=blocks)

    # Wait for and handle the user's response in this workflow.
    event = autokitteh.next_event(sub)
    autokitteh.unsubscribe(sub)
    return event.actions[0]["value"] == "retry"
