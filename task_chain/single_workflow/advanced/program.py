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


tasks = [step1, step2, step3, step4]


def on_slack_slash_command(event):
    """Use a Slack slash command from a user to start a chain of tasks."""
    user_id = event.data.user_id

    # Note to the interested reader: it's easy to improve this project
    # to traverse a dynamic DAG, instead of a simple static list.
    success = True
    while len(tasks) > 0 and success:
        success = run_retriable_task(tasks[0], user_id)

    if success:
        message = "Workflow completed successfully :smiley_cat:"
        slack.chat_postMessage(channel=user_id, text=message)


def run_retriable_task(task, user_id) -> bool:
    try:
        task()
    except RuntimeError as e:
        return ask_user_retry_or_abort(task.__name__, e, user_id)

    message = f"Task `{task.__name__}` completed"
    slack.chat_postMessage(channel=user_id, text=message)

    global tasks
    tasks.remove(task)
    return True


def ask_user_retry_or_abort(task_name, error, user_id) -> bool:
    sub = autokitteh.subscribe("slack_conn", 'event_type == "interaction"')

    blocks = Path("interactive_message.json.txt").read_text()
    blocks = blocks.replace("MESSAGE", f"The task `{task_name}` failed: `{error}`")
    slack.chat_postMessage(channel=user_id, text="Workflow error", blocks=blocks)

    # Wait for and handle the user's response in this workflow.
    event = autokitteh.next_event(sub)
    autokitteh.unsubscribe(sub)
    return event.actions[0]["value"] == "retry"
