"""Main entry-point for the "task chain" project."""

# import event_driven
import single_workflow
import tasks


def on_slack_slash_command(event):
    """Use a Slack slash command from a user to start a chain of tasks."""
    single_workflow.run_tasks(tasks.task1, event.data.user_id)
    # Alternative approach: event_driven.run_tasks(tasks.task1, event.data.user_id)
