"""Main workflow for the Kubernetes sheet dashboard."""

import datetime
from os import getenv

from autokitteh import activity
from autokitteh.google import google_sheets_client

from data import CurrentState
from data import Deployment


gsheets = google_sheets_client("gsheets").spreadsheets().values()

_GSHEET_ID = getenv("GOOGLE_SHEET_ID")

# Header:
#       A      B         C         D        E      F      G         H             I             J           K      L    # noqa: E501
#   +------+-------+--------------------+---------------+--------------------------------------------------------------+  # noqa: E501
# 1 |      |       | COMMAND            | DESIRED       | CURRENT                                                      |  # noqa: E501
# 2 | Name | Slack | Operation | Status | Image | Scale | Image | R: Desired | R: Available | R: Ready | R: Update | T |  # noqa: E501
#   +------+-------+-----------+--------+------+--------+-------+------------+--------------+----------+-----------+---+  # noqa: E501
_HEADER_HEIGHT = 2


def _time() -> str:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()


@activity
def _get_values() -> list[list[str]]:
    rows = (
        gsheets.get(spreadsheetId=_GSHEET_ID, range=f"A{_HEADER_HEIGHT + 1}:F64")
        .execute()
        .get("values", [])
    )

    return [r + [""] * (6 - len(r)) for r in rows]


def _parse_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


# TODO: Indicate parsing errors?
def get_deployments() -> list[Deployment]:
    rows = _get_values()

    return [
        Deployment(
            row_num=row_num,
            name=vs[0],
            slack=vs[1].split(","),
            op=vs[2],
            status=vs[3],
            desired_image=vs[4],
            desired_replicas=_parse_int(vs[5]),
        )
        for row_num, vs in enumerate(rows, _HEADER_HEIGHT + 1)
        if len(vs)
    ]


@activity
def update_deployment_current_state(row_num: int, s: CurrentState) -> None:
    """Update a row in the sheet."""
    gsheets.update(
        spreadsheetId=_GSHEET_ID,
        range=f"G{row_num}:L{row_num}",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                [
                    s.image,
                    s.desired_replicas or 0,
                    s.available_replicas or 0,
                    s.ready_replicas or 0,
                    s.updated_replicas or 0,
                    _time(),
                ]
                if s
                else ["", "", "", "", "", _time()],
            ]
        },
    ).execute()


@activity
def update_deployment_status(row_num: int, op: str, status: str) -> None:
    gsheets.update(
        spreadsheetId=_GSHEET_ID,
        range=f"C{row_num}:D{row_num}",
        valueInputOption="USER_ENTERED",
        body={
            "values": [
                [
                    op,
                    f"[{_time()}] {status}",
                ]
            ]
        },
    ).execute()
