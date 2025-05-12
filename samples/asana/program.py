"""Demonstrates AutoKitteh’s Asana integration for managing tasks via the Asana API."""

import os

import asana
from autokitteh.asana import asana_client


api_client = asana_client("asana_conn")
client = asana.TasksApi(api_client)

WORKSPACE_GID = os.getenv("WORKSPACE_GID", "")


def create_task(event):
    task_name = event.data.url.query.get("name") or "autokitteh task"
    body = {
        "data": {
            "workspace": WORKSPACE_GID,
            "name": task_name,
            "assignee": "me",
        }
    }

    task = client.create_task(body, {})
    print(f"Task '{task['name']}' has been successfully created!")


def update_task(event):
    """Updates an Asana task's name and due date."""
    form = event.data.body.form
    task_gid = form.get("task_gid")
    new_due_date = form.get("new_due_date", "2025-01-20")
    new_name_suffix = form.get("name_suffix", " - Updated by AutoKitteh")

    task = client.get_task(task_gid, {"opt_fields": "name,assignee,due_on,tags"})
    print(f"Current Task: {task}")

    body = {
        "data": {
            "name": task["name"] + new_name_suffix,
            "due_on": new_due_date,
        }
    }

    updated_task = client.update_task(body, task_gid, {})

    print(f"Task '{updated_task['name']}' has been successfully updated!")
