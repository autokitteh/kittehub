"""Tests for incident webhook handlers."""

import os
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest


# Set required environment variables before importing any modules
os.environ["GOOGLE_SPREADSHEET_ID"] = "test_spreadsheet_id"

# Mock autokitteh and store dependencies before importing handlers
with (
    patch("autokitteh.get_webhook_url", return_value="http://test.webhook.url"),
    patch("autokitteh.google.gspread_client", return_value=MagicMock()),
    patch("autokitteh.http_outcome") as mock_http_outcome,
):
    import handlers
    from model import Incident
    from model import IncidentState


@pytest.fixture
def mock_event():
    """Create a mock event object."""
    event = Mock()
    event.data = Mock()
    return event


@pytest.fixture
def sample_incident():
    """Return a sample incident for testing."""
    from datetime import datetime
    from zoneinfo import ZoneInfo

    return Incident(
        id="42",
        details="Test incident",
        state=IncidentState.PENDING,
        started_at=datetime(2024, 1, 15, 10, 0, 0, tzinfo=ZoneInfo("UTC")),
        unique_id="test_unique_id",
    )


class TestOnNewIncidentWebhook:
    """Tests for the on_new_incident_webhook handler."""

    @patch("handlers.incidents.run")
    @patch("handlers.incidents.create")
    @patch("handlers.http_outcome")
    def test_successful_incident_creation(
        self, mock_http_outcome, mock_create, mock_run, mock_event, sample_incident
    ):
        """Test successful creation of a new incident."""
        mock_event.data.body.text = "Server is down"
        mock_create.return_value = sample_incident

        handlers.on_new_incident_webhook(mock_event)

        # Verify incident was created
        mock_create.assert_called_once_with("Server is down")

        # Verify HTTP response
        mock_http_outcome.assert_called_once_with(
            status_code=201, json={"incident_id": "42"}
        )

        # Verify incident was run
        mock_run.assert_called_once_with(sample_incident)

    @patch("handlers.incidents.run")
    @patch("handlers.incidents.create")
    @patch("handlers.http_outcome")
    def test_strips_whitespace_from_details(
        self, mock_http_outcome, mock_create, mock_run, mock_event, sample_incident
    ):
        """Test that whitespace is stripped from incident details."""
        mock_event.data.body.text = "  Database connection failed  \n"
        mock_create.return_value = sample_incident

        handlers.on_new_incident_webhook(mock_event)

        mock_create.assert_called_once_with("Database connection failed")

    @patch("handlers.store.update_incident")
    @patch("handlers.incidents.run")
    @patch("handlers.incidents.create")
    @patch("handlers.http_outcome")
    def test_handles_exception_during_run(
        self,
        mock_http_outcome,
        mock_create,
        mock_run,
        mock_update,
        mock_event,
        sample_incident,
    ):
        """Test that exceptions during run are handled properly."""
        mock_event.data.body.text = "Test incident"
        mock_create.return_value = sample_incident
        mock_run.side_effect = RuntimeError("Something went wrong")

        with pytest.raises(RuntimeError, match="Something went wrong"):
            handlers.on_new_incident_webhook(mock_event)

        # Verify HTTP response was sent before error
        mock_http_outcome.assert_called_once_with(
            status_code=201, json={"incident_id": "42"}
        )

        # Verify incident was updated with error state
        mock_update.assert_called_once()
        updated_incident = mock_update.call_args[0][0]
        assert updated_incident.state == IncidentState.ERROR
        assert updated_incident.comment == "Something went wrong"


class TestOnIncidentDashboardWebhook:
    """Tests for the on_incident_dashboard_webhook handler."""

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_missing_unique_id(self, mock_http_outcome, mock_get_incident, mock_event):
        """Test that missing unique_id returns 403."""
        mock_event.data.url.query.get.return_value = None

        handlers.on_incident_dashboard_webhook(mock_event)

        mock_http_outcome.assert_called_once_with(
            status_code=403, json={"error": "missing unique_id"}
        )
        mock_get_incident.assert_not_called()

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_incident_not_found(self, mock_http_outcome, mock_get_incident, mock_event):
        """Test that non-existent incident returns 404."""
        mock_event.data.url.query.get.return_value = "nonexistent_id"
        mock_event.data.get.return_value = None
        mock_get_incident.return_value = None

        handlers.on_incident_dashboard_webhook(mock_event)

        mock_http_outcome.assert_called_once_with(
            status_code=404, json={"error": "not found"}
        )

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_unsupported_method(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that unsupported HTTP methods return 405."""
        mock_event.data.url.query.get.return_value = "test_unique_id"
        mock_event.data.get.return_value = None
        mock_event.data.method = "DELETE"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        mock_http_outcome.assert_called_once_with(
            status_code=405, json={"error": "method not allowed"}
        )

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_renders_dashboard(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that GET request renders the incident dashboard."""
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        # Verify HTTP response contains dashboard HTML
        mock_http_outcome.assert_called_once()
        call_args = mock_http_outcome.call_args
        assert call_args[1]["status_code"] == 200
        assert "Incident 42" in call_args[1]["body"]
        assert "Test incident" in call_args[1]["body"]
        assert sample_incident.state in call_args[1]["body"]

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_with_user(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test GET request includes user email in dashboard."""
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_user = Mock()
        mock_user.email = "alice@example.com"
        mock_event.data.get.return_value = mock_user
        mock_event.data.method = "GET"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        assert "alice@example.com" in call_args[1]["body"]

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_with_message(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test GET request includes message from query params."""
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": "notified",
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        assert "notified" in call_args[1]["body"]
        assert "color: green" in call_args[1]["body"]

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_pending_state_shows_buttons(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that PENDING state shows appropriate buttons."""
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]
        # Should show resolve and notify buttons
        assert 'value="resolve"' in body
        assert 'value="notify"' in body
        # Should not show ack button (only for ASSIGNED state)
        assert 'value="ack"' not in body

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_assigned_state_shows_ack(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that ASSIGNED state shows ack button."""
        from dataclasses import replace

        assigned_incident = replace(sample_incident, state=IncidentState.ASSIGNED)
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = assigned_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]
        # Should show ack, resolve, escalate, and notify buttons
        assert 'value="ack"' in body
        assert 'value="resolve"' in body
        assert 'value="escalate"' in body
        assert 'value="notify"' in body

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_in_progress_shows_escalate(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that IN_PROGRESS state shows escalate button."""
        from dataclasses import replace

        in_progress_incident = replace(sample_incident, state=IncidentState.IN_PROGRESS)
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = in_progress_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]
        assert 'value="escalate"' in body
        assert 'value="resolve"' in body

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_resolved_state_no_form(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that RESOLVED state shows no action form."""
        from dataclasses import replace

        resolved_incident = replace(sample_incident, state=IncidentState.RESOLVED)
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = resolved_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]
        # Should not show action form, but show message
        assert "<form" not in body
        assert "no longer active" in body

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_with_authenticated_user_shows_take(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that authenticated users see the take button."""
        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_user = Mock()
        mock_user.email = "alice@example.com"
        mock_event.data.get.return_value = mock_user
        mock_event.data.method = "GET"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]
        # Should show take button for authenticated user
        assert 'value="take"' in body

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_post_request_redirects_with_notification(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that POST request redirects with notification message."""
        mock_event.data.url.query.get.return_value = "test_unique_id"
        mock_event.data.get.return_value = None
        mock_event.data.method = "POST"
        mock_get_incident.return_value = sample_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        # Should return two http_outcome calls: redirect (303) and then content (200)
        assert mock_http_outcome.call_count == 2

        # First call should be redirect
        first_call = mock_http_outcome.call_args_list[0]
        assert first_call[1]["status_code"] == 303
        assert "Location" in first_call[1]["headers"]
        assert "&msg=notified" in first_call[1]["headers"]["Location"]

    @patch("handlers.store.get_incident_by_unique_id")
    @patch("handlers.http_outcome")
    def test_get_request_shows_incident_fields(
        self, mock_http_outcome, mock_get_incident, mock_event, sample_incident
    ):
        """Test that dashboard shows all incident fields."""
        from dataclasses import replace
        from datetime import datetime
        from zoneinfo import ZoneInfo

        detailed_incident = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="bob@example.com",
            assigned_at=datetime(2024, 1, 15, 10, 30, 0, tzinfo=ZoneInfo("UTC")),
            comment="Working on it",
        )

        mock_event.data.url.query.get.side_effect = lambda key: {
            "unique_id": "test_unique_id",
            "msg": None,
        }.get(key)
        mock_event.data.get.return_value = None
        mock_event.data.method = "GET"
        mock_get_incident.return_value = detailed_incident

        handlers.on_incident_dashboard_webhook(mock_event)

        call_args = mock_http_outcome.call_args
        body = call_args[1]["body"]

        # Verify all fields are displayed
        assert "Incident 42" in body
        assert "assigned" in body
        assert "Test incident" in body
        assert "Working on it" in body
        assert "bob@example.com" in body


class TestInit:
    """Tests for the init handler."""

    @patch("builtins.print")
    def test_init_prints_message(self, mock_print):
        """Test that init function prints initialization message."""
        handlers.init(None)

        mock_print.assert_called_once_with("initialized.")
