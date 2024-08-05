"""TODO: Documentation header..."""

from collections.abc import Callable
from pathlib import Path

import autokitteh
from autokitteh.slack import slack_client


slack = slack_client("slack_conn")


def on_slack_slash_command(event) -> None:
    """Use a Slack slash command from a user to start a task chain."""
    # Note to the interested reader: it's easy to improve this function
    # to traverse a DAG with BFS or DFS, instead of a simple dynamic list.
    next_task, ok = task_wrapper(task1, event.data.user_id)
    while next_task:
        next_task, ok = task_wrapper(next_task, event.data.user_id)

    if ok:
        success_message = "Workflow completed successfully :smiley_cat:"
        slack.chat_postMessage(channel=event.data.user_id, text=success_message)


def task_wrapper(task: Callable, user_id: str) -> tuple[Callable | None, bool]:
    """Enable optional retries when tasks fail."""
    try:
        return task(), True
    except Exception as e:
        retry = ask_user(task.__name__, str(e), user_id)
        result = task if retry else None
        return result, False


def ask_user(task_name: str, err: str, user_id: str) -> bool:
    """Ask the user what to do when a task fails (retry / abort)."""
    sub = autokitteh.subscribe("slack_conn", 'event_type == "interaction"')

    blocks = Path("interactive_message.json.txt").read_text()
    blocks = blocks.replace("MESSAGE", f"The task `{task_name}` failed:\n\n`{err}`")
    slack.chat_postMessage(channel=user_id, text="dummy text", blocks=blocks)

    event = autokitteh.next_event(sub)
    autokitteh.unsubscribe(sub)
    return event.actions[0]["value"] == "retry"


def task1() -> Callable | None:
    print("Task 1 is doing stuff...")
    return task2


def task2() -> Callable | None:
    print("Task 2 is doing stuff...")
    return task3


def task3() -> Callable | None:
    print("Task 3 is doing stuff...")
    raise RuntimeError("Something bad happened")


def task4() -> Callable | None:
    print("Task 4 is doing stuff...")
    return None  # This is the last task.
