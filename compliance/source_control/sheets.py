"""Convenient wrappers for Google Sheets's Python API."""

import os

import autokitteh
from autokitteh.google import google_sheets_client
from github.Commit import Commit
from github.PullRequest import PullRequest


SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")

sheets = google_sheets_client("sheets_conn").spreadsheets()


def save_violations(sheet_name: str, violations: list[Commit | PullRequest]) -> None:
    print(f"{sheet_name}: saving {len(violations)} violations")
    _add_sheet(sheet_name, len(violations), 10)
    _write_links(sheet_name, violations)


@autokitteh.activity
def _add_sheet(title: str, rows: int, cols: int) -> None:
    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": title,
                        "gridProperties": {"rowCount": rows, "columnCount": cols},
                    }
                }
            }
        ]
    }
    sheets.batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()


@autokitteh.activity
def _write_links(sheet_name, github_objects: list[Commit | PullRequest]) -> None:
    sheets.values().update(
        spreadsheetId=SHEET_ID,
        range=f"'{sheet_name}'!A1:A{len(github_objects)}",
        valueInputOption="USER_ENTERED",
        body={"values": [[o.html_url for o in github_objects]]},
    ).execute()
