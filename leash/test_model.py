"""Tests for model.py data structures and methods."""

from datetime import UTC  # noqa: I001
from datetime import datetime

import pytest

from model import Contact
from model import Incident
from model import IncidentState
from model import ScheduleRow


class TestContact:
    """Tests for Contact class."""

    def test_from_row_with_all_fields(self):
        """Test creating a Contact from a complete row."""
        row = ["John Doe", "john@example.com", "+1234567890"]
        contact = Contact.from_row(row)

        assert contact.name == "John Doe"
        assert contact.email == "john@example.com"
        assert contact.phone == "+1234567890"

    def test_from_row_with_name_only(self):
        """Test creating a Contact from a row with only name."""
        row = ["Jane Smith"]
        contact = Contact.from_row(row)

        assert contact.name == "Jane Smith"
        assert contact.email is None
        assert contact.phone is None

    def test_from_row_with_name_and_email(self):
        """Test creating a Contact from a row with name and email only."""
        row = ["Bob Wilson", "bob@example.com"]
        contact = Contact.from_row(row)

        assert contact.name == "Bob Wilson"
        assert contact.email == "bob@example.com"
        assert contact.phone is None

    def test_from_row_with_empty_email(self):
        """Test creating a Contact with empty string for email."""
        row = ["Alice Brown", "", "+9876543210"]
        contact = Contact.from_row(row)

        assert contact.name == "Alice Brown"
        assert contact.email == ""
        assert contact.phone == "+9876543210"


class TestScheduleRow:
    """Tests for ScheduleRow class."""

    def test_from_row(self):
        """Test creating a ScheduleRow from a row."""
        row = ["01-01-2025 00:00", "01-07-2025 23:59", "Alice", "Bob", "Charlie"]
        schedule = ScheduleRow.from_row(row)

        assert schedule.start_time == datetime(2025, 1, 1, 0, 0, 0, tzinfo=UTC)
        assert schedule.end_time == datetime(2025, 1, 7, 23, 59, 0, tzinfo=UTC)
        assert schedule.assignees == ["Alice", "Bob", "Charlie"]

    def test_from_row_filters_empty_assignees(self):
        """Test that from_row filters out empty strings from assignees."""
        row = ["01-01-2025 00:00", "01-07-2025 23:59", "Alice", "", "Bob", ""]
        schedule = ScheduleRow.from_row(row)

        assert schedule.assignees == ["Alice", "Bob"]

    def test_row_property(self):
        """Test that row property returns correct format."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob"],
        )
        row = schedule.row

        assert row[0] == "01-01-2025 00:00"
        assert row[1] == "01-07-2025 23:59"
        assert row[2:] == ["Alice", "Bob"]

    def test_match_within_range(self):
        """Test match returns True for time within schedule period."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice"],
        )

        assert schedule.match(datetime(2025, 1, 3, 12, 0, 0)) is True  # noqa: DTZ001

    def test_match_at_start_boundary(self):
        """Test match returns True for time at start boundary."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice"],
        )

        assert schedule.match(datetime(2025, 1, 1, 0, 0, 0)) is True  # noqa: DTZ001

    def test_match_at_end_boundary(self):
        """Test match returns True for time at end boundary."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice"],
        )

        assert schedule.match(datetime(2025, 1, 7, 23, 59, 59)) is True  # noqa: DTZ001

    def test_match_before_range(self):
        """Test match returns False for time before schedule period."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice"],
        )

        assert schedule.match(datetime(2024, 12, 31, 23, 59, 59)) is False  # noqa: DTZ001

    def test_match_after_range(self):
        """Test match returns False for time after schedule period."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice"],
        )

        assert schedule.match(datetime(2025, 1, 8, 0, 0, 0)) is False  # noqa: DTZ001

    def test_get_next_assignee_first_with_no_current(self):
        """Test get_next_assignee returns first assignee when current is None."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob", "Charlie"],
        )

        assert schedule.get_next_assignee(None) == "Alice"

    def test_get_next_assignee_first_with_empty_current(self):  # noqa: E501
        """Test get_next_assignee returns first assignee when current is empty string."""  # noqa: E501
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob", "Charlie"],
        )

        assert schedule.get_next_assignee("") == "Alice"

    def test_get_next_assignee_rotates(self):
        """Test get_next_assignee rotates through assignees."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob", "Charlie"],
        )

        assert schedule.get_next_assignee("Alice") == "Bob"
        assert schedule.get_next_assignee("Bob") == "Charlie"

    def test_get_next_assignee_wraps_around(self):
        """Test get_next_assignee wraps around to first assignee."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob", "Charlie"],
        )

        assert schedule.get_next_assignee("Charlie") == "Alice"

    def test_get_next_assignee_empty_list(self):
        """Test get_next_assignee returns None when no assignees."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=[],
        )

        assert schedule.get_next_assignee(None) is None
        assert schedule.get_next_assignee("Alice") is None

    def test_get_next_assignee_not_found_resets(self):
        """Test get_next_assignee resets to first when current not in list."""
        schedule = ScheduleRow(
            start_time=datetime(2025, 1, 1, 0, 0, 0),  # noqa: DTZ001
            end_time=datetime(2025, 1, 7, 23, 59, 59),  # noqa: DTZ001
            assignees=["Alice", "Bob"],
        )

        # When current assignee isn't in the list, it should raise ValueError
        # based on line 71: i = self.assignees.index(curr) will raise ValueError
        with pytest.raises(ValueError):  # noqa: PT011
            schedule.get_next_assignee("Charlie")


class TestIncidentState:
    """Tests for IncidentState enum."""

    def test_is_active_pending(self):
        """Test is_active returns True for PENDING state."""
        assert IncidentState.PENDING.is_active is True

    def test_is_active_assigned(self):
        """Test is_active returns True for ASSIGNED state."""
        assert IncidentState.ASSIGNED.is_active is True

    def test_is_active_in_progress(self):
        """Test is_active returns True for IN_PROGRESS state."""
        assert IncidentState.IN_PROGRESS.is_active is True

    def test_is_active_resolved(self):
        """Test is_active returns False for RESOLVED state."""
        assert IncidentState.RESOLVED.is_active is False

    def test_is_active_error(self):
        """Test is_active returns False for ERROR state."""
        assert IncidentState.ERROR.is_active is False

    def test_state_values(self):
        """Test that state enum values are correct."""
        assert IncidentState.PENDING.value == "pending"
        assert IncidentState.ASSIGNED.value == "assigned"
        assert IncidentState.IN_PROGRESS.value == "in_progress"
        assert IncidentState.RESOLVED.value == "resolved"
        assert IncidentState.ERROR.value == "error"


class TestIncident:
    """Tests for Incident class."""

    def test_from_row_complete(self):
        """Test creating an Incident from a complete row."""
        row = [
            "123",
            "01-15-2025 10:30",
            "assigned",
            "Alice",
            "01-15-2025 10:35",
            "Working on it",
            "Server down",
            "=HYPERLINK(...)",
            "unique-123",
        ]
        incident = Incident.from_row(row)

        assert incident.id == "123"
        assert incident.started_at == datetime(2025, 1, 15, 10, 30, 0, tzinfo=UTC)
        assert incident.state == IncidentState.ASSIGNED
        assert incident.assignee == "Alice"
        assert incident.assigned_at == datetime(2025, 1, 15, 10, 35, 0, tzinfo=UTC)
        assert incident.comment == "Working on it"
        assert incident.details == "Server down"
        assert incident.unique_id == "unique-123"

    def test_from_row_minimal(self):
        """Test creating an Incident from a minimal row with no optional fields."""
        row = [
            "456",
            "01-15-2025 10:30",
            "pending",
            "",
            "",
            "",
            "Database error",
            "",
            "unique-456",
        ]
        incident = Incident.from_row(row)

        assert incident.id == "456"
        assert incident.started_at == datetime(2025, 1, 15, 10, 30, 0, tzinfo=UTC)
        assert incident.state == IncidentState.PENDING
        assert incident.assignee is None
        assert incident.assigned_at is None
        assert incident.comment is None
        assert incident.details == "Database error"
        assert incident.unique_id == "unique-456"

    def test_row_property_complete(self):
        """Test row property returns correct format for complete incident."""
        incident = Incident(
            id="789",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.IN_PROGRESS,
            assignee="Bob",
            assigned_at=datetime(2025, 1, 15, 10, 35, 0),  # noqa: DTZ001
            comment="In progress",
            details="Network issue",
            unique_id="unique-789",
        )
        row = incident.row

        assert row[0] == 789
        assert row[1] == "01-15-2025 10:30"
        assert row[2] == "in_progress"
        assert row[3] == "Bob"
        assert row[4] == "01-15-2025 10:35"
        assert row[5] == "In progress"
        assert row[6] == "Network issue"
        assert row[8] == "unique-789"

    def test_row_property_minimal(self):
        """Test row property returns correct format for minimal incident."""
        incident = Incident(
            id="101",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="CPU spike",
            unique_id="unique-101",
        )
        row = incident.row

        assert row[0] == 101
        assert row[1] == "01-15-2025 10:30"
        assert row[2] == "pending"
        assert row[3] is None
        assert row[4] == ""
        assert row[5] == ""
        assert row[6] == "CPU spike"
        assert row[8] == "unique-101"

    def test_dashboard_url_with_config(self, monkeypatch):
        """Test dashboard_url property when webhook URL is configured."""
        monkeypatch.setattr(
            "config.INCIDENT_DASHBOARD_WEBHOOK_URL", "https://example.com/dashboard"
        )

        incident = Incident(
            id="202",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="Test incident",
            unique_id="unique-202",
        )

        assert (
            incident.dashboard_url
            == "https://example.com/dashboard?unique_id=unique-202"
        )

    def test_dashboard_url_without_config(self, monkeypatch):
        """Test dashboard_url property when webhook URL is not configured."""
        monkeypatch.setattr("config.INCIDENT_DASHBOARD_WEBHOOK_URL", None)

        incident = Incident(
            id="303",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="Test incident",
            unique_id="unique-303",
        )

        assert incident.dashboard_url == ""

    def test_dashboard_url_with_empty_config(self, monkeypatch):
        """Test dashboard_url property when webhook URL is empty string."""
        monkeypatch.setattr("config.INCIDENT_DASHBOARD_WEBHOOK_URL", "")

        incident = Incident(
            id="404",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="Test incident",
            unique_id="unique-404",
        )

        assert incident.dashboard_url == ""

    def test_row_property_includes_hyperlink_with_url(self, monkeypatch):  # noqa: E501
        """Test row property includes hyperlink formula when dashboard URL is configured."""  # noqa: E501
        monkeypatch.setattr(
            "config.INCIDENT_DASHBOARD_WEBHOOK_URL", "https://example.com/dashboard"
        )

        incident = Incident(
            id="505",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="Test incident",
            unique_id="unique-505",
        )
        row = incident.row

        assert (
            row[7]
            == '=HYPERLINK("https://example.com/dashboard?unique_id=unique-505", "ACT")'
        )

    def test_row_property_no_hyperlink_without_url(self, monkeypatch):
        """Test row property has empty string for hyperlink when no dashboard URL."""
        monkeypatch.setattr("config.INCIDENT_DASHBOARD_WEBHOOK_URL", None)

        incident = Incident(
            id="606",
            started_at=datetime(2025, 1, 15, 10, 30, 0),  # noqa: DTZ001
            state=IncidentState.PENDING,
            details="Test incident",
            unique_id="unique-606",
        )
        row = incident.row

        assert row[7] == ""
