"""Main entry-point for the "task chain" project."""

import os

import event_driven
import single_workflow
import tasks


SINGLE_WORKFLOW = os.getenv("SINGLE_WORKFLOW", "true").lower()


def on_slack_slash_command(event):
    """Use a Slack slash command from a user to start a chain of tasks."""
    first_task = tasks.task1
    if SINGLE_WORKFLOW in ["true", "yes", "on", "1"]:
        single_workflow.run_tasks(first_task, event.data.user_id)
    else:
        event_driven.run_tasks(first_task, event.data.user_id)
