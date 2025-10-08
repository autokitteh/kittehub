"""Google Sheets storage backend for Leash data.

This module provides data persistence using Google Sheets as the storage layer.
It manages worksheets for incidents, schedules, contacts, and internal state,
providing CRUD operations for incidents and queries for schedules and contacts.
"""

from datetime import datetime
from os import getenv

from autokitteh.google import gspread_client
from gspread.exceptions import WorksheetNotFound
from gspread.utils import ValueInputOption
from gspread.worksheet import Worksheet
from model import Contact
from model import Incident
from model import ScheduleRow


_GOOGLE_SPREADSHEET_ID = getenv("GOOGLE_SPREADSHEET_ID")
if not _GOOGLE_SPREADSHEET_ID:
    raise RuntimeError("GOOGLE_SPREADSHEET_ID not set")

_client = gspread_client("gsheets").open_by_key(_GOOGLE_SPREADSHEET_ID)


#
# Utils
#


def get(name: str) -> Worksheet | None:
    """Get a worksheet by name."""
    try:
        return _client.worksheet(name)
    except WorksheetNotFound:
        return None


def _get_or_create(name: str, init=None) -> Worksheet:
    """Ensure a worksheet exists, creating it if needed.

    If `init` is given, it is used to initialize the sheet.
    """
    try:
        return _client.worksheet(name)
    except WorksheetNotFound:
        pass

    w = _client.add_worksheet(name, rows=100, cols=20)

    if init:
        w.update(init, raw=False)

    return w


#
# Sheets
#


_incidents = _get_or_create("incidents", [Incident.labels])
_schedule = _get_or_create("schedule", [ScheduleRow.labels])

_scratchpad = _get_or_create(
    "_scratchpad",
    [
        ["next_incident_id", "=MAX(incidents!A:A) + 1"],
    ],
)

_contacts = get("contacts")


#
# Operations
#


def next_incident_id() -> str:
    return str(_scratchpad.acell("B1").value or 1)


def add_incident(inc: Incident) -> None:
    _incidents.append_row(inc.row, value_input_option=ValueInputOption.user_entered)


def get_incident_by_unique_id(unique_id: str) -> Incident | None:
    cell = _incidents.find(unique_id, in_column=9)
    if not cell:
        return None

    return Incident.from_row(_incidents.row_values(cell.row))


def update_incident(inc: Incident) -> None:
    print(f"update: {inc}")

    cell = _incidents.find(str(inc.id), in_column=1)
    if not cell:
        raise ValueError(f"Incident with id {inc.id} not found")

    _incidents.update(
        [inc.row],
        f"A{cell.row}",
        value_input_option=ValueInputOption.user_entered,
    )


def get_schedule_row(t: datetime) -> ScheduleRow | None:
    """Get the schedule row for a specific time.

    If no schedule is found, returns None.
    If more than one schedule matches, returns the first one.
    """
    rows = _schedule.get_all_values()
    for i, row in enumerate(rows[1:]):
        try:
            sched = ScheduleRow.from_row(row)
        except ValueError as exc:
            print(f"ERROR: Invalid schedule row {i + 1}: {row} -> {exc}")
            continue

        if sched.match(t):
            return sched

    return None


def get_contact_by_name(name: str) -> Contact | None:
    """Get a contact by name."""
    if not _contacts:
        return None

    cell = _contacts.find(name, in_column=1)
    if not cell:
        return None

    return Contact.from_row(_contacts.row_values(cell.row))


def get_contact_by_email(email: str) -> Contact | None:
    """Get a contact by email."""
    if not _contacts:
        return None

    cell = _contacts.find(email, in_column=2)
    if not cell:
        return None

    return Contact.from_row(_contacts.row_values(cell.row))
