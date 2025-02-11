from os import getenv

from autokitteh.height import height_client
from urlparse import urljoin


_LIST_ID = getenv("HEIGHT_LIST_ID")

_ROOT_URL = "https://api.height.app/"

height = height_client("height")


if not _LIST_ID:
    raise ValueError("HEIGHT_LIST_ID is not set")


def _post(path: str, data: dict) -> dict:
    resp = height.post(urljoin(_ROOT_URL, path), json=data)
    resp.raise_for_status()
    return resp.json()


def create_task(name: str, desc: str, status: str) -> dict:
    return _post(
        "tasks",
        {
            "name": name,
            "type": "task",
            "description": desc,
            "status": status,
            "listIds": [_LIST_ID],
        },
    )


def add_task_message(task_id: str, msg: str):
    return _post(
        "activities",
        {
            "taskId": task_id,
            "type": "comment",
            "message": msg,
        },
    )
