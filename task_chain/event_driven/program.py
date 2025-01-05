"""This module uses an event-driven approach for the task-chain project.

A single workflow runs all the tasks, except retries:

1. First workflow:
   - Trigger: Slack slash command
   - Task 1 -> Task 2 -> Task 3 (error) -> Workflow error
2. Second workflow:
   - Trigger: user clicks the "Retry" button in Slack
   - Task 3 (retry) -> Task 4 -> Successful workflow completion
"""

from pathlib import Path
import random

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
    run_tasks(0, event.data.user_id)


def run_tasks(start_index, user_id):
    # Note to the interested reader: it's easy to improve this project
    # to traverse a dynamic DAG, instead of a simple static list.
    for i, task in enumerate(tasks):
        if i >= start_index:
            run_retriable_task(task, i, user_id)

    message = "Workflow completed successfully :smiley_cat:"
    slack.chat_postMessage(channel=user_id, text=message)


def run_retriable_task(task, i, user_id):
    try:
        task()
    except Exception as e:
        ask_user_retry_or_abort(task.__name__, e, i, user_id)
        raise e  # Abort the current workflow.

    message = f"Task `{task.__name__}` completed"
    slack.chat_postMessage(channel=user_id, text=message)


def ask_user_retry_or_abort(task_name, error, i, user_id):
    message = f"The task `{task_name}` failed: `{error}`"
    blocks = Path("interactive_message.json.txt").read_text()
    blocks = blocks.replace("MESSAGE", message).replace("INDEX", str(i))
    slack.chat_postMessage(channel=user_id, text="Workflow error", blocks=blocks)


def on_slack_interaction(event):
    """Handle the user's response (retry / abort) in a new workflow."""
    if event.data.actions[0]["value"] == "abort":
        return

    # This workflow's starting point is a retry of the failed task in the aborted one.
    i = int(event.data.actions[0]["action_id"].split()[-1])
    run_tasks(i, event.data.user.id)
