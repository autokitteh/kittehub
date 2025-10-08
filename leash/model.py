"""Data models for the Leash incident management system.

This module defines the core data structures used throughout the system including
Contact (person to notify), ScheduleRow (on-call rotation schedule), Incident
(event being tracked), and IncidentState (lifecycle state). Models include
serialization methods for Google Sheets storage.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import auto
from enum import StrEnum
from typing import ClassVar

from utils import format_ts
from utils import parse_ts

import config


def _col(row: list, i: int, default=None):
    """Get a column from a row, returning a default if it doesn't exist."""
    try:
        return row[i]
    except IndexError:
        return default


@dataclass(frozen=True, kw_only=True)
class Contact:
    """A contact."""

    name: str
    """The name of the contact."""

    email: str | None = None
    """The email address of the contact, if any."""

    phone: str | None = None
    """The phone number of the contact, if any."""

    @staticmethod
    def from_row(row: list) -> "Contact":
        return Contact(
            name=row[0],
            email=_col(row, 1),
            phone=_col(row, 2),
        )


@dataclass(frozen=True, kw_only=True)
class ScheduleRow:
    """A schedule row."""

    start_time: datetime
    """When the schedule period begins."""

    end_time: datetime
    """When the schedule period ends."""

    assignees: list[str]
    """List of people assigned to this schedule in the order they should be assigned."""

    def get_next_assignee(self, curr: str | None) -> str | None:
        """Get the next assignee in the schedule after the current assignee."""
        if not self.assignees:
            return None

        if not curr:
            return self.assignees[0]

        i = self.assignees.index(curr)
        if i < 0:
            # Assignee does not exist, maybe removed. Reset rotation.
            return self.assignees[0]

        i = (i + 1) % len(self.assignees)

        return self.assignees[i]

    labels: ClassVar = ["start_time", "end_time", "assignees"]

    @property
    def row(self) -> list:
        """Return the schedule row as a list for storage."""
        return [
            format_ts(self.start_time),
            format_ts(self.end_time),
            *self.assignees,
        ]

    @staticmethod
    def from_row(row: list) -> "ScheduleRow":
        """Create a ScheduleRow from a row."""
        return ScheduleRow(
            start_time=parse_ts(row[0]),
            end_time=parse_ts(row[1]),
            assignees=[s for s in row[2:] if s],
        )

    def match(self, t: datetime) -> bool:
        """Return True if the given time is within the schedule period."""
        return self.start_time <= t <= self.end_time


class IncidentState(StrEnum):
    """An incident state."""

    PENDING = auto()
    """Incident has been reported but not yet assigned."""

    ASSIGNED = auto()
    """Incident has been assigned to someone but work hasn't started."""

    IN_PROGRESS = auto()
    """Someone is actively working on the incident."""

    RESOLVED = auto()
    """Incident has been resolved and closed."""

    ERROR = auto()
    """An error occurred while processing the incident."""

    @property
    def is_active(self) -> bool:
        """Return True if the incident is active (not resolved or error)."""
        return self in {
            IncidentState.PENDING,
            IncidentState.ASSIGNED,
            IncidentState.IN_PROGRESS,
        }


@dataclass(frozen=True, kw_only=True)
class Incident:
    """An incident."""

    id: str
    """Unique identifier for the incident."""

    started_at: datetime
    """When the incident was started."""

    details: str
    """Description of what happened, usually the payload of the notification."""

    state: IncidentState
    """Current state of the incident."""

    assignee: str | None = None
    """The person that was last assigned to the incident, if any."""

    assigned_at: datetime | None = None
    """When the incident was last assigned, if ever."""

    comment: str | None = None
    """Optional comment about the incident."""

    unique_id: str
    """A unique identifier for the incident, used to prevent scraping."""

    labels: ClassVar = [
        "id",
        "started_at",
        "state",
        "assignee",
        "assigned_at",
        "comment",
        "details",
        "action",
        "unique_id",
    ]

    @property
    def dashboard_url(self) -> str:
        """Return the URL of the incident dashboard, if configured."""
        if url := config.INCIDENT_DASHBOARD_WEBHOOK_URL:
            return f"{url}?unique_id={self.unique_id}"
        return ""

    @property
    def row(self) -> list:
        """Return the incident as a row for storage."""
        return [
            int(self.id),
            format_ts(self.started_at),
            self.state,
            self.assignee,
            format_ts(self.assigned_at) if self.assigned_at else "",
            self.comment or "",
            self.details,
            f'=HYPERLINK("{self.dashboard_url}", "ACT")' if self.dashboard_url else "",
            self.unique_id,
        ]

    @staticmethod
    def from_row(row: list) -> "Incident":
        """Create an Incident from a row."""
        return Incident(
            id=str(row[0]),
            started_at=parse_ts(row[1]),
            state=IncidentState(row[2]),
            assignee=row[3] or None,
            assigned_at=parse_ts(row[4]) if row[4] else None,
            comment=row[5] or None,
            details=row[6],
            unique_id=row[8],
        )
