"""Tests for Google Sheets storage backend functionality."""

from datetime import datetime, timedelta
import os
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from zoneinfo import ZoneInfo

from gspread.exceptions import WorksheetNotFound

import pytest


# Set required environment variables before importing store
os.environ["GOOGLE_SPREADSHEET_ID"] = "test_spreadsheet_id"

# Mock autokitteh dependencies before importing store
with (
    patch("autokitteh.get_webhook_url", return_value="http://test.webhook.url"),
    patch("autokitteh.google.gspread_client") as mock_gspread,
):
    mock_client = MagicMock()
    mock_gspread.return_value = mock_client
    import store

from model import Contact
from model import Incident
from model import IncidentState
from model import ScheduleRow


@pytest.fixture
def fixed_time():
    """Return a fixed datetime for testing."""
    return datetime(2024, 1, 15, 10, 0, 0, tzinfo=ZoneInfo("UTC"))


@pytest.fixture
def sample_incident(fixed_time):
    """Return a sample incident for testing."""
    return Incident(
        id="42",
        details="Test incident details",
        state=IncidentState.PENDING,
        started_at=fixed_time,
        unique_id="test_unique_id_xyz",
    )


@pytest.fixture
def sample_contact():
    """Return a sample contact for testing."""
    return Contact(
        name="alice@example.com",
        email="alice@example.com",
        phone="+1234567890",
    )


@pytest.fixture
def sample_schedule(fixed_time):
    """Return a sample schedule for testing."""
    return ScheduleRow(
        start_time=fixed_time - timedelta(hours=1),
        end_time=fixed_time + timedelta(hours=23),
        assignees=["alice@example.com", "bob@example.com"],
    )


class TestGet:
    """Tests for the get function."""

    def test_get_existing_worksheet(self):
        """Test getting an existing worksheet."""
        mock_worksheet = Mock()
        store._client.worksheet = Mock(return_value=mock_worksheet)

        result = store.get("test_sheet")

        assert result == mock_worksheet
        store._client.worksheet.assert_called_once_with("test_sheet")

    def test_get_nonexistent_worksheet(self):
        """Test getting a worksheet that doesn't exist."""
        store._client.worksheet = Mock(side_effect=WorksheetNotFound("Not found"))

        result = store.get("nonexistent_sheet")

        assert result is None
        store._client.worksheet.assert_called_once_with("nonexistent_sheet")


class TestNextIncidentId:
    """Tests for the next_incident_id function."""

    def test_next_incident_id_with_value(self):
        """Test getting next incident ID when value exists."""
        mock_cell = Mock()
        mock_cell.value = "42"
        store._scratchpad.acell = Mock(return_value=mock_cell)

        result = store.next_incident_id()

        assert result == "42"
        store._scratchpad.acell.assert_called_once_with("B1")

    def test_next_incident_id_default(self):
        """Test getting next incident ID when no value exists."""
        mock_cell = Mock()
        mock_cell.value = None
        store._scratchpad.acell = Mock(return_value=mock_cell)

        result = store.next_incident_id()

        assert result == "1"


class TestAddIncident:
    """Tests for the add_incident function."""

    def test_add_incident(self, sample_incident):
        """Test adding an incident to the sheet."""
        store._incidents.append_row = Mock()

        store.add_incident(sample_incident)

        store._incidents.append_row.assert_called_once()
        call_args = store._incidents.append_row.call_args
        assert call_args[0][0] == sample_incident.row
        assert "value_input_option" in call_args[1]


class TestGetIncidentByUniqueId:
    """Tests for the get_incident_by_unique_id function."""

    def test_get_incident_found(self, sample_incident):
        """Test getting an incident that exists."""
        mock_cell = Mock()
        mock_cell.row = 2
        store._incidents.find = Mock(return_value=mock_cell)
        store._incidents.row_values = Mock(return_value=sample_incident.row)

        result = store.get_incident_by_unique_id("test_unique_id_xyz")

        assert result is not None
        assert result.id == sample_incident.id
        assert result.unique_id == sample_incident.unique_id
        store._incidents.find.assert_called_once_with("test_unique_id_xyz", in_column=9)

    def test_get_incident_not_found(self):
        """Test getting an incident that doesn't exist."""
        store._incidents.find = Mock(return_value=None)

        result = store.get_incident_by_unique_id("nonexistent_id")

        assert result is None
        store._incidents.find.assert_called_once_with("nonexistent_id", in_column=9)


class TestUpdateIncident:
    """Tests for the update_incident function."""

    def test_update_incident_success(self, sample_incident):
        """Test updating an existing incident."""
        mock_cell = Mock()
        mock_cell.row = 3
        store._incidents.find = Mock(return_value=mock_cell)
        store._incidents.update = Mock()

        store.update_incident(sample_incident)

        store._incidents.find.assert_called_once_with(
            str(sample_incident.id), in_column=1
        )
        store._incidents.update.assert_called_once()
        call_args = store._incidents.update.call_args
        assert call_args[0][0] == [sample_incident.row]
        assert call_args[0][1] == "A3"

    def test_update_incident_not_found(self, sample_incident):
        """Test updating an incident that doesn't exist."""
        store._incidents.find = Mock(return_value=None)

        with pytest.raises(ValueError, match="Incident with id 42 not found"):
            store.update_incident(sample_incident)


class TestGetScheduleRow:
    """Tests for the get_schedule_row function."""

    def test_get_schedule_row_match(self, fixed_time, sample_schedule):
        """Test getting a schedule row that matches the time."""
        store._schedule.get_all_values = Mock(
            return_value=[
                ScheduleRow.labels,
                sample_schedule.row,
            ]
        )

        result = store.get_schedule_row(fixed_time)

        assert result is not None
        assert result.start_time == sample_schedule.start_time
        assert result.end_time == sample_schedule.end_time
        assert result.assignees == sample_schedule.assignees

    def test_get_schedule_row_no_match(self, fixed_time, sample_schedule):
        """Test getting a schedule row when time doesn't match."""
        # Create schedule that doesn't match the fixed_time
        past_schedule = ScheduleRow(
            start_time=fixed_time - timedelta(days=2),
            end_time=fixed_time - timedelta(days=1),
            assignees=["alice@example.com"],
        )

        store._schedule.get_all_values = Mock(
            return_value=[
                ScheduleRow.labels,
                past_schedule.row,
            ]
        )

        result = store.get_schedule_row(fixed_time)

        assert result is None

    def test_get_schedule_row_multiple_matches_returns_first(self, fixed_time):
        """Test that when multiple schedules match, the first one is returned."""
        schedule1 = ScheduleRow(
            start_time=fixed_time - timedelta(hours=1),
            end_time=fixed_time + timedelta(hours=1),
            assignees=["alice@example.com"],
        )
        schedule2 = ScheduleRow(
            start_time=fixed_time - timedelta(hours=2),
            end_time=fixed_time + timedelta(hours=2),
            assignees=["bob@example.com"],
        )

        store._schedule.get_all_values = Mock(
            return_value=[
                ScheduleRow.labels,
                schedule1.row,
                schedule2.row,
            ]
        )

        result = store.get_schedule_row(fixed_time)

        assert result is not None
        assert result.assignees == ["alice@example.com"]

    def test_get_schedule_row_invalid_row(self, fixed_time, sample_schedule):
        """Test getting a schedule row with an invalid row in the data."""
        store._schedule.get_all_values = Mock(
            return_value=[
                ScheduleRow.labels,
                ["invalid", "data"],  # Invalid row
                sample_schedule.row,  # Valid row
            ]
        )

        result = store.get_schedule_row(fixed_time)

        # Should skip invalid row and return the valid one
        assert result is not None
        assert result.assignees == sample_schedule.assignees

    def test_get_schedule_row_empty(self, fixed_time):
        """Test getting a schedule row when no schedules exist."""
        store._schedule.get_all_values = Mock(return_value=[ScheduleRow.labels])

        result = store.get_schedule_row(fixed_time)

        assert result is None


class TestGetContactByName:
    """Tests for the get_contact_by_name function."""

    def test_get_contact_by_name_found(self, sample_contact):
        """Test getting a contact that exists."""
        mock_cell = Mock()
        mock_cell.row = 2
        store._contacts = Mock()
        store._contacts.find = Mock(return_value=mock_cell)
        store._contacts.row_values = Mock(
            return_value=[
                sample_contact.name,
                sample_contact.email,
                sample_contact.phone,
            ]
        )

        result = store.get_contact_by_name("alice@example.com")

        assert result is not None
        assert result.name == sample_contact.name
        assert result.email == sample_contact.email
        assert result.phone == sample_contact.phone
        store._contacts.find.assert_called_once_with("alice@example.com", in_column=1)

    def test_get_contact_by_name_not_found(self):
        """Test getting a contact that doesn't exist."""
        store._contacts = Mock()
        store._contacts.find = Mock(return_value=None)

        result = store.get_contact_by_name("unknown@example.com")

        assert result is None

    def test_get_contact_by_name_no_contacts_sheet(self):
        """Test getting a contact when contacts sheet doesn't exist."""
        store._contacts = None

        result = store.get_contact_by_name("alice@example.com")

        assert result is None


class TestGetContactByEmail:
    """Tests for the get_contact_by_email function."""

    def test_get_contact_by_email_found(self, sample_contact):
        """Test getting a contact by email that exists."""
        mock_cell = Mock()
        mock_cell.row = 2
        store._contacts = Mock()
        store._contacts.find = Mock(return_value=mock_cell)
        store._contacts.row_values = Mock(
            return_value=[
                sample_contact.name,
                sample_contact.email,
                sample_contact.phone,
            ]
        )

        result = store.get_contact_by_email("alice@example.com")

        assert result is not None
        assert result.name == sample_contact.name
        assert result.email == sample_contact.email
        assert result.phone == sample_contact.phone
        store._contacts.find.assert_called_once_with("alice@example.com", in_column=2)

    def test_get_contact_by_email_not_found(self):
        """Test getting a contact by email that doesn't exist."""
        store._contacts = Mock()
        store._contacts.find = Mock(return_value=None)

        result = store.get_contact_by_email("unknown@example.com")

        assert result is None

    def test_get_contact_by_email_no_contacts_sheet(self):
        """Test getting a contact by email when contacts sheet doesn't exist."""
        store._contacts = None

        result = store.get_contact_by_email("alice@example.com")

        assert result is None
