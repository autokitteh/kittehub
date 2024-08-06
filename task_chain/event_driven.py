"""This module uses an event-driven approach for this project.

A single workflow is in charge of running all the tasks, except retries:

1. First workflow:
   - Trigger: Slack slash command
   - Task 1 -> Task 2 -> Task 3 (error) -> Workflow error
2. Second workflow:
   - Trigger: user clicks the "Retry" button in Slack
   - Task 3 (retry) -> Task 4 -> Successful workflow completion
"""

from collections.abc import Callable

from autokitteh.slack import slack_client

from ask_user import ask_user


slack = slack_client("slack_conn")


def run_tasks(task: Callable, user_id: str) -> None:
    # Note to the interested reader: it's easy to improve this
    # loop to traverse a DAG, instead of a simple dynamic list.
    next_task = run_retriable_task(task, user_id)
    while next_task:
        next_task = run_retriable_task(next_task, user_id)

    success_message = "Workflow completed successfully :smiley_cat:"
    slack.chat_postMessage(channel=user_id, text=success_message)


def run_retriable_task(task: Callable, user_id: str) -> Callable | None:
    try:
        return task()
    except Exception as e:
        ask_user(task.__name__, str(e), user_id)
        raise e  # Abort the current workflow.


def on_slack_interaction(event):
    """Handle the user's response (retry / abort) in a new workflow."""
    if event.data.actions[0]["value"] == "abort":
        return

    # This workflow's starting point is a retry of the failed task in the aborted workflow.
    task_name = event.data.actions[0]["action_id"].split()[-1]
    run_tasks(globals()[task_name], event.data.user.id)
