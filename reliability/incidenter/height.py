"""Create Height tasks and add messages to them."""

import os
from urllib.parse import urljoin

from autokitteh.height import height_client


_ROOT_URL = "https://api.height.app/"

_HEIGHT_LIST_ID = os.getenv("HEIGHT_LIST_ID")

if not _HEIGHT_LIST_ID:
    raise ValueError("HEIGHT_LIST_ID project variable must be set")

height = height_client("height_conn")


def _post(path: str, data: dict) -> dict:
    resp = height.post(urljoin(_ROOT_URL, path), json=data)
    resp.raise_for_status()
    return resp.json()


def create_task(name: str, desc: str, status: str) -> dict:
    return _post(
        "tasks",
        {
            "type": "task",
            "name": name,
            "description": desc,
            "status": status,
            "listIds": [_HEIGHT_LIST_ID],
        },
    )


def add_task_message(task_id: str, msg: str) -> dict:
    return _post(
        "activities",
        {
            "type": "comment",
            "taskId": task_id,
            "message": msg,
        },
    )
