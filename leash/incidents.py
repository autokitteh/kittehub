"""Core incident management logic and workflow orchestration.

This module implements the incident lifecycle management including creation,
assignment, escalation, and resolution. It handles the automatic escalation
workflow, on-call schedule rotation, notification delivery, and processing
of user actions from the incident dashboard.
"""

from dataclasses import replace
from datetime import datetime, timedelta
import secrets
from typing import cast

from model import Incident
from model import IncidentState
from model import ScheduleRow
from notifications import notify
import store

from autokitteh import next_event, subscribe
import config


def _now() -> datetime:
    return datetime.now(tz=config.TZ)


def create(details: str) -> Incident:
    """Create a new incident and store it."""
    t = _now()

    inc = Incident(
        id=store.next_incident_id(),
        details=details,
        state=IncidentState.PENDING,
        started_at=t,
        unique_id=secrets.token_urlsafe(16),
    )

    store.add_incident(inc)

    return inc


def run(inc: Incident) -> None:
    """Run the incident management loop in a durable workflow."""
    # Subscribe to incident dashboard webhooks for this incident id.
    webhook_response_subscription = subscribe(
        "incident_dashboard_webhook",
        filter=(
            f"data.method == 'POST' && data.url.query.unique_id == '{inc.unique_id}'"
        ),
    )

    # Escalation loop.
    while inc.state.is_active:
        now = _now()

        if _is_new_assignee_required(now, inc):
            schedule = store.get_schedule_row(now)

            inc = _auto_assign(now, inc, schedule)

            store.update_incident(inc)

            if not inc.state.is_active:
                continue

        data = next_event(webhook_response_subscription, timeout=timedelta(minutes=1))
        if data:
            inc = _handle_webhook_response(data.body.form, data.get("user"), inc)
            store.update_incident(inc)

    print(f"incident {inc.id} no longer active.")


def _is_new_assignee_required(t: datetime, inc: Incident) -> bool:
    match inc.state:
        case IncidentState.PENDING:
            return True
        case IncidentState.ASSIGNED:
            return (
                (t - inc.assigned_at) > config.ESCALATION_DELAY
                if inc.assigned_at
                else False
            )
        case _:
            return False


def _notify(contact: store.Contact, inc: Incident) -> None:
    notify(
        contact,
        subject="[LEASH] New incident assigned",
        message=f"""Incident details:
{inc.details}
ID: {inc.id}
Respond: {inc.dashboard_url}""",
    )


def _assign(t: datetime, inc: Incident, assignee: str, comment: str) -> Incident:
    contact = store.get_contact_by_name(assignee)
    if contact is None:
        return replace(
            inc,
            state=IncidentState.ERROR,
            comment=f"assignee '{assignee}' not found in contacts",
        )

    _notify(contact, inc)

    return replace(
        inc,
        state=IncidentState.ASSIGNED,
        assigned_at=t,
        assignee=assignee,
        comment=comment,
    )


def _auto_assign(t: datetime, inc: Incident, schedule: ScheduleRow | None) -> Incident:
    fail_state = (
        IncidentState.ERROR if config.FAIL_ON_NO_ASSIGNEE else IncidentState.PENDING
    )

    if not schedule:
        return replace(inc, state=fail_state, comment="no schedule set")

    assignee = schedule.get_next_assignee(inc.assignee)
    if not assignee:
        return replace(inc, state=fail_state, comment="schedule has no assignees")

    return _assign(t, inc, assignee, "auto-assigned")


def _handle_webhook_response(
    form: dict[str, str],
    user: dict | None,
    inc: Incident,
) -> Incident:
    """Handle a webhook response event."""
    print(f"webhook response: {form}")

    action = form.get("action")

    by = ""
    if user:
        by = f" by {user.get('email')}"

    match action:
        case "ack" | "a":
            return replace(
                inc,
                state=IncidentState.IN_PROGRESS,
                comment=f"ack'd via webhook{by}",
            )

        case "resolve" | "r":
            return replace(
                inc,
                state=IncidentState.RESOLVED,
                comment=f"resolved via webhook{by}",
            )

        case "escalate" | "e":
            return replace(inc, state=IncidentState.PENDING, comment=f"escalated{by}")

        case "take" | "t":
            if not user:
                return replace(
                    inc, comment="take attempted but no user info in webhook"
                )

            return _assign(
                _now(),
                inc,
                cast(str, user.get("email")),
                f"taken via webhook{by}",
            )

        case "assign" | "g":
            assignee = form.get("assignee")
            if not assignee:
                return replace(inc, comment="assign: no assignee given")

            return _assign(_now(), inc, assignee, f"manually assigned via webhook{by}")

        case "notify" | "n":
            if not inc.assignee:
                return replace(inc, comment="notify: no assignee set")

            contact = store.get_contact_by_name(inc.assignee)
            if not contact:
                return replace(
                    inc,
                    comment=f"notify: assignee '{inc.assignee}' not found in contacts",
                )

            _notify(contact, inc)

            return replace(inc, comment=f"notified assignee via webhook{by}")

        case _:
            return replace(inc, comment=f"unknown action '{action}' received{by}")
