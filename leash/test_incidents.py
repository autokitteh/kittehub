"""Tests for incident management logic and workflow orchestration."""

from dataclasses import replace
from datetime import datetime, timedelta
import os
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest


# Set required environment variables before importing any modules
os.environ["GOOGLE_SPREADSHEET_ID"] = "test_spreadsheet_id"

# Mock autokitteh and store dependencies before importing incidents
with (
    patch("autokitteh.get_webhook_url", return_value="http://test.webhook.url"),
    patch("autokitteh.google.gspread_client", return_value=MagicMock()),
):
    import incidents
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
        id="1",
        details="Test incident",
        state=IncidentState.PENDING,
        started_at=fixed_time,
        unique_id="test_unique_id_123",
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
        assignees=["alice@example.com", "bob@example.com", "charlie@example.com"],
    )


class TestCreate:
    """Tests for the create function."""

    @patch("incidents.store.next_incident_id")
    @patch("incidents.store.add_incident")
    @patch("incidents._now")
    @patch("incidents.secrets.token_urlsafe")
    def test_create_new_incident(
        self, mock_token, mock_now, mock_add, mock_next_id, fixed_time
    ):
        """Test creating a new incident."""
        mock_next_id.return_value = "42"
        mock_now.return_value = fixed_time
        mock_token.return_value = "unique_token_abc"

        inc = incidents.create("Server is down")

        assert inc.id == "42"
        assert inc.details == "Server is down"
        assert inc.state == IncidentState.PENDING
        assert inc.started_at == fixed_time
        assert inc.unique_id == "unique_token_abc"
        assert inc.assignee is None
        assert inc.assigned_at is None

        mock_add.assert_called_once_with(inc)


class TestIsNewAssigneeRequired:
    """Tests for the _is_new_assignee_required function."""

    def test_pending_state_requires_assignee(self, sample_incident, fixed_time):
        """Test that PENDING state always requires a new assignee."""
        assert incidents._is_new_assignee_required(fixed_time, sample_incident)

    @patch("incidents.config.ESCALATION_DELAY", timedelta(minutes=15))
    def test_assigned_state_requires_escalation_after_delay(
        self, sample_incident, fixed_time
    ):
        """Test that ASSIGNED state requires escalation after delay."""
        inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assigned_at=fixed_time - timedelta(minutes=20),
        )
        assert incidents._is_new_assignee_required(fixed_time, inc)

    @patch("incidents.config.ESCALATION_DELAY", timedelta(minutes=15))
    def test_assigned_state_no_escalation_before_delay(
        self, sample_incident, fixed_time
    ):
        """Test that ASSIGNED state does not require escalation before delay."""
        inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assigned_at=fixed_time - timedelta(minutes=10),
        )
        assert not incidents._is_new_assignee_required(fixed_time, inc)

    def test_assigned_state_no_assigned_at(self, sample_incident, fixed_time):
        """Test ASSIGNED state with no assigned_at timestamp."""
        inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assigned_at=None,
        )
        assert not incidents._is_new_assignee_required(fixed_time, inc)

    def test_in_progress_state_no_escalation(self, sample_incident, fixed_time):
        """Test that IN_PROGRESS state does not require escalation."""
        inc = replace(sample_incident, state=IncidentState.IN_PROGRESS)
        assert not incidents._is_new_assignee_required(fixed_time, inc)

    def test_resolved_state_no_escalation(self, sample_incident, fixed_time):
        """Test that RESOLVED state does not require escalation."""
        inc = replace(sample_incident, state=IncidentState.RESOLVED)
        assert not incidents._is_new_assignee_required(fixed_time, inc)

    def test_error_state_no_escalation(self, sample_incident, fixed_time):
        """Test that ERROR state does not require escalation."""
        inc = replace(sample_incident, state=IncidentState.ERROR)
        assert not incidents._is_new_assignee_required(fixed_time, inc)


class TestAssign:
    """Tests for the _assign function."""

    @patch("incidents._notify")
    @patch("incidents.store.get_contact_by_name")
    def test_assign_success(
        self, mock_get_contact, mock_notify, sample_incident, sample_contact, fixed_time
    ):
        """Test successful assignment."""
        mock_get_contact.return_value = sample_contact

        inc = incidents._assign(
            fixed_time, sample_incident, "alice@example.com", "manual assignment"
        )

        assert inc.state == IncidentState.ASSIGNED
        assert inc.assignee == "alice@example.com"
        assert inc.assigned_at == fixed_time
        assert inc.comment == "manual assignment"

        mock_get_contact.assert_called_once_with("alice@example.com")
        mock_notify.assert_called_once_with(sample_contact, sample_incident)

    @patch("incidents.store.get_contact_by_name")
    def test_assign_contact_not_found(
        self, mock_get_contact, sample_incident, fixed_time
    ):
        """Test assignment when contact is not found."""
        mock_get_contact.return_value = None

        inc = incidents._assign(
            fixed_time, sample_incident, "unknown@example.com", "auto-assigned"
        )

        assert inc.state == IncidentState.ERROR
        assert "unknown@example.com" in inc.comment
        assert "not found" in inc.comment


class TestAutoAssign:
    """Tests for the _auto_assign function."""

    @patch("incidents._assign")
    @patch("incidents.config.FAIL_ON_NO_ASSIGNEE", True)
    def test_auto_assign_no_schedule(self, mock_assign, sample_incident, fixed_time):
        """Test auto-assignment when no schedule is available."""
        inc = incidents._auto_assign(fixed_time, sample_incident, None)

        assert inc.state == IncidentState.ERROR
        assert inc.comment == "no schedule set"
        mock_assign.assert_not_called()

    @patch("incidents.config.FAIL_ON_NO_ASSIGNEE", False)
    def test_auto_assign_no_schedule_no_fail(self, sample_incident, fixed_time):
        """Test auto-assignment when FAIL_ON_NO_ASSIGNEE is False."""
        inc = incidents._auto_assign(fixed_time, sample_incident, None)

        assert inc.state == IncidentState.PENDING
        assert inc.comment == "no schedule set"

    @patch("incidents._assign")
    @patch("incidents.config.FAIL_ON_NO_ASSIGNEE", True)
    def test_auto_assign_empty_schedule(
        self, mock_assign, sample_incident, sample_schedule, fixed_time
    ):
        """Test auto-assignment when schedule has no assignees."""
        empty_schedule = replace(sample_schedule, assignees=[])
        inc = incidents._auto_assign(fixed_time, sample_incident, empty_schedule)

        assert inc.state == IncidentState.ERROR
        assert inc.comment == "schedule has no assignees"
        mock_assign.assert_not_called()

    @patch("incidents._assign")
    def test_auto_assign_success(
        self, mock_assign, sample_incident, sample_schedule, fixed_time
    ):
        """Test successful auto-assignment."""
        expected_inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="alice@example.com",
        )
        mock_assign.return_value = expected_inc

        inc = incidents._auto_assign(fixed_time, sample_incident, sample_schedule)

        mock_assign.assert_called_once_with(
            fixed_time, sample_incident, "alice@example.com", "auto-assigned"
        )
        assert inc == expected_inc

    @patch("incidents._assign")
    def test_auto_assign_next_in_rotation(
        self, mock_assign, sample_incident, sample_schedule, fixed_time
    ):
        """Test auto-assignment gets next person in rotation."""
        inc_with_assignee = replace(sample_incident, assignee="alice@example.com")
        expected_inc = replace(
            inc_with_assignee,
            state=IncidentState.ASSIGNED,
            assignee="bob@example.com",
        )
        mock_assign.return_value = expected_inc

        incidents._auto_assign(fixed_time, inc_with_assignee, sample_schedule)

        mock_assign.assert_called_once_with(
            fixed_time, inc_with_assignee, "bob@example.com", "auto-assigned"
        )


class TestHandleWebhookResponse:
    """Tests for the _handle_webhook_response function."""

    def test_ack_action(self, sample_incident):
        """Test acknowledgement action."""
        form = {"action": "ack"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.IN_PROGRESS
        assert "ack'd via webhook" in inc.comment

    def test_ack_action_short_form(self, sample_incident):
        """Test acknowledgement action using short form."""
        form = {"action": "a"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.IN_PROGRESS

    def test_ack_with_user(self, sample_incident):
        """Test acknowledgement with user information."""
        form = {"action": "ack"}
        user = {"email": "alice@example.com"}
        inc = incidents._handle_webhook_response(form, user, sample_incident)

        assert inc.state == IncidentState.IN_PROGRESS
        assert "alice@example.com" in inc.comment

    def test_resolve_action(self, sample_incident):
        """Test resolve action."""
        form = {"action": "resolve"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.RESOLVED
        assert "resolved via webhook" in inc.comment

    def test_resolve_action_short_form(self, sample_incident):
        """Test resolve action using short form."""
        form = {"action": "r"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.RESOLVED

    def test_escalate_action(self, sample_incident):
        """Test escalate action."""
        form = {"action": "escalate"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.PENDING
        assert "escalated" in inc.comment

    def test_escalate_action_short_form(self, sample_incident):
        """Test escalate action using short form."""
        form = {"action": "e"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert inc.state == IncidentState.PENDING

    @patch("incidents._assign")
    @patch("incidents._now")
    def test_take_action(self, mock_now, mock_assign, sample_incident, fixed_time):
        """Test take action with user."""
        mock_now.return_value = fixed_time
        expected_inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="alice@example.com",
        )
        mock_assign.return_value = expected_inc

        form = {"action": "take"}
        user = {"email": "alice@example.com"}
        inc = incidents._handle_webhook_response(form, user, sample_incident)

        mock_assign.assert_called_once()
        assert inc == expected_inc

    def test_take_action_no_user(self, sample_incident):
        """Test take action without user information."""
        form = {"action": "take"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert "take attempted but no user info" in inc.comment

    @patch("incidents._assign")
    @patch("incidents._now")
    def test_assign_action(self, mock_now, mock_assign, sample_incident, fixed_time):
        """Test manual assignment action."""
        mock_now.return_value = fixed_time
        expected_inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="bob@example.com",
        )
        mock_assign.return_value = expected_inc

        form = {"action": "assign", "assignee": "bob@example.com"}
        incidents._handle_webhook_response(form, None, sample_incident)

        mock_assign.assert_called_once_with(
            fixed_time,
            sample_incident,
            "bob@example.com",
            "manually assigned via webhook",
        )

    def test_assign_action_no_assignee(self, sample_incident):
        """Test manual assignment without assignee."""
        form = {"action": "assign"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert "assign: no assignee given" in inc.comment

    @patch("incidents._notify")
    @patch("incidents.store.get_contact_by_name")
    def test_notify_action(
        self, mock_get_contact, mock_notify, sample_incident, sample_contact
    ):
        """Test notify action."""
        inc_with_assignee = replace(sample_incident, assignee="alice@example.com")
        mock_get_contact.return_value = sample_contact

        form = {"action": "notify"}
        inc = incidents._handle_webhook_response(form, None, inc_with_assignee)

        mock_get_contact.assert_called_once_with("alice@example.com")
        mock_notify.assert_called_once_with(sample_contact, inc_with_assignee)
        assert "notified assignee via webhook" in inc.comment

    def test_notify_action_no_assignee(self, sample_incident):
        """Test notify action without assignee."""
        form = {"action": "notify"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert "notify: no assignee set" in inc.comment

    @patch("incidents.store.get_contact_by_name")
    def test_notify_action_contact_not_found(self, mock_get_contact, sample_incident):
        """Test notify action when contact is not found."""
        inc_with_assignee = replace(sample_incident, assignee="unknown@example.com")
        mock_get_contact.return_value = None

        form = {"action": "notify"}
        inc = incidents._handle_webhook_response(form, None, inc_with_assignee)

        assert "not found in contacts" in inc.comment

    def test_unknown_action(self, sample_incident):
        """Test unknown action."""
        form = {"action": "unknown_action"}
        inc = incidents._handle_webhook_response(form, None, sample_incident)

        assert "unknown action 'unknown_action'" in inc.comment


class TestRun:
    """Tests for the run function."""

    @patch("incidents.subscribe")
    @patch("incidents.next_event")
    @patch("incidents.store.update_incident")
    @patch("incidents.store.get_schedule_row")
    @patch("incidents._auto_assign")
    @patch("incidents._is_new_assignee_required")
    @patch("incidents._now")
    def test_run_auto_assign_then_resolve(
        self,
        mock_now,
        mock_is_new_assignee,
        mock_auto_assign,
        mock_get_schedule,
        mock_update,
        mock_next_event,
        mock_subscribe,
        sample_incident,
        sample_schedule,
        fixed_time,
    ):
        """Test run function with auto-assignment followed by resolution."""
        # Setup
        mock_now.return_value = fixed_time
        mock_subscription = Mock()
        mock_subscribe.return_value = mock_subscription

        # First iteration: auto-assign
        assigned_inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="alice@example.com",
            assigned_at=fixed_time,
        )

        # Second iteration: resolve via webhook
        resolved_inc = replace(assigned_inc, state=IncidentState.RESOLVED)

        mock_is_new_assignee.side_effect = [True, False]
        mock_get_schedule.return_value = sample_schedule
        mock_auto_assign.return_value = assigned_inc

        webhook_data = Mock()
        webhook_data.body.form = {"action": "resolve"}
        webhook_data.get.return_value = {"email": "alice@example.com"}

        mock_next_event.side_effect = [None, webhook_data]

        # Patch _handle_webhook_response to return resolved incident
        with patch("incidents._handle_webhook_response", return_value=resolved_inc):
            incidents.run(sample_incident)

        # Verify subscription
        mock_subscribe.assert_called_once()
        assert "incident_dashboard_webhook" in mock_subscribe.call_args[0]
        assert sample_incident.unique_id in mock_subscribe.call_args[1]["filter"]

        # Verify store updates
        assert mock_update.call_count == 2
        mock_update.assert_any_call(assigned_inc)
        mock_update.assert_any_call(resolved_inc)

    @patch("incidents.subscribe")
    @patch("incidents.next_event")
    @patch("incidents.store.update_incident")
    @patch("incidents.store.get_schedule_row")
    @patch("incidents._auto_assign")
    @patch("incidents._is_new_assignee_required")
    @patch("incidents._now")
    def test_run_escalation_timeout(
        self,
        mock_now,
        mock_is_new_assignee,
        mock_auto_assign,
        mock_get_schedule,
        mock_update,
        mock_next_event,
        mock_subscribe,
        sample_incident,
        sample_schedule,
        fixed_time,
    ):
        """Test run function with escalation after timeout."""
        mock_now.return_value = fixed_time
        mock_subscription = Mock()
        mock_subscribe.return_value = mock_subscription

        # First iteration: assign to alice
        assigned_alice = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="alice@example.com",
            assigned_at=fixed_time,
        )

        # Second iteration: escalate to bob
        assigned_bob = replace(
            assigned_alice,
            assignee="bob@example.com",
        )

        # Third iteration: resolve
        resolved_inc = replace(assigned_bob, state=IncidentState.RESOLVED)

        mock_is_new_assignee.side_effect = [True, True, False]
        mock_get_schedule.return_value = sample_schedule
        mock_auto_assign.side_effect = [assigned_alice, assigned_bob]

        webhook_data = Mock()
        webhook_data.body.form = {"action": "resolve"}
        webhook_data.get.return_value = None

        mock_next_event.side_effect = [None, None, webhook_data]

        with patch("incidents._handle_webhook_response", return_value=resolved_inc):
            incidents.run(sample_incident)

        # Verify both escalations occurred
        assert mock_auto_assign.call_count == 2
        assert mock_update.call_count == 3

    @patch("incidents.subscribe")
    @patch("incidents.next_event")
    @patch("incidents.store.update_incident")
    @patch("incidents.store.get_schedule_row")
    @patch("incidents._auto_assign")
    @patch("incidents._is_new_assignee_required")
    @patch("incidents._now")
    def test_run_immediate_error(
        self,
        mock_now,
        mock_is_new_assignee,
        mock_auto_assign,
        mock_get_schedule,
        mock_update,
        mock_next_event,
        mock_subscribe,
        sample_incident,
        fixed_time,
    ):
        """Test run function when auto-assignment fails immediately."""
        mock_now.return_value = fixed_time
        mock_subscription = Mock()
        mock_subscribe.return_value = mock_subscription

        error_inc = replace(
            sample_incident,
            state=IncidentState.ERROR,
            comment="no schedule set",
        )

        mock_is_new_assignee.return_value = True
        mock_get_schedule.return_value = None
        mock_auto_assign.return_value = error_inc

        incidents.run(sample_incident)

        # Should update once with error state and then exit
        mock_update.assert_called_once_with(error_inc)
        # next_event should not be called since state is not active
        mock_next_event.assert_not_called()

    @patch("incidents.subscribe")
    @patch("incidents.next_event")
    @patch("incidents.store.update_incident")
    @patch("incidents._is_new_assignee_required")
    @patch("incidents._now")
    def test_run_webhook_only_no_assignment(
        self,
        mock_now,
        mock_is_new_assignee,
        mock_update,
        mock_next_event,
        mock_subscribe,
        sample_incident,
        fixed_time,
    ):
        """Test run function with webhook response without auto-assignment."""
        mock_now.return_value = fixed_time
        mock_subscription = Mock()
        mock_subscribe.return_value = mock_subscription

        # Incident is already assigned, no new assignee needed
        assigned_inc = replace(
            sample_incident,
            state=IncidentState.ASSIGNED,
            assignee="alice@example.com",
        )

        resolved_inc = replace(assigned_inc, state=IncidentState.RESOLVED)

        mock_is_new_assignee.return_value = False

        webhook_data = Mock()
        webhook_data.body.form = {"action": "resolve"}
        webhook_data.get.return_value = None

        mock_next_event.return_value = webhook_data

        with patch("incidents._handle_webhook_response", return_value=resolved_inc):
            incidents.run(assigned_inc)

        # Should only update once with resolved state
        mock_update.assert_called_once_with(resolved_inc)
