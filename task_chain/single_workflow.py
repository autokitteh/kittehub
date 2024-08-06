"""This module uses a single-workflow approach for this project.

A single workflow is in charge of running all the tasks, including retries.
It handles Slack interactions internally using runtime event subscriptions.
"""

from collections.abc import Callable

from autokitteh.slack import slack_client

from ask_user import ask_user


slack = slack_client("slack_conn")


def run_tasks(task: Callable, user_id: str) -> None:
    # Note to the interested reader: it's easy to improve this
    # loop to traverse a DAG, instead of a simple dynamic list.
    next_task, ok = run_retriable_task(task, user_id)
    while next_task:
        next_task, ok = run_retriable_task(next_task, user_id)

    if ok:
        success_message = "Workflow completed successfully :smiley_cat:"
        slack.chat_postMessage(channel=user_id, text=success_message)


def run_retriable_task(task: Callable, user_id: str) -> tuple[Callable | None, bool]:
    try:
        return task(), True
    except Exception as e:
        retry = ask_user(task.__name__, str(e), user_id, wait_resp=True)
        result = task if retry else None
        return result, False
