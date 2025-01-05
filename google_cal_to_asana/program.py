"""Create a new Asana task when a new event is created in Google Calendar."""

import os

import asana
from asana.rest import ApiException
from autokitteh.asana import asana_client


ASANA_PROJECT_GID = os.getenv("ASANA_PROJECT_GID")

api_client = asana_client("asana_conn")
tasks_api_instance = asana.TasksApi(api_client)


def on_calendar_event_created(event):
    """This is the workflow entry point."""
    # Extract relevant information from the Google Calendar event.
    task_name = event.data.get("summary", "New Task")
    due_date = event.data.get("start", {}).get("date_time")
    description = event.data.get("description", "")

    create_asana_task(task_name, due_date, description)


def create_asana_task(task_name, due_date, description):
    """Create a new task in Asana.

    See:
        https://github.com/Asana/python-asana/blob/v5.0.10/docs/TasksApi.md#create_task
    """
    body = {
        "data": {
            "name": task_name,
            "projects": [ASANA_PROJECT_GID],  # More than one project can be added.
            "due_on": due_date,
            "notes": description,
        }
    }

    opts = {"opt_fields": "name,assignee.name,due_on,created_at,projects.name,notes"}

    try:
        task = tasks_api_instance.create_task(body, opts)
        print(task)
    except ApiException as e:
        print(f"Exception when calling TasksApi->create_task: {e}")
