"""Leash handlers."""

from dataclasses import replace

from autokitteh import Event, http_outcome
import incidents
from model import IncidentState
import store


def on_new_incident_webhook(event: Event):
    details = event.data.body.text.strip()

    print(f"new incident, details={details}")

    inc = incidents.create(details)

    http_outcome(status_code=201, json={"incident_id": inc.id})

    try:
        incidents.run(inc)
    except Exception as e:
        store.update_incident(
            replace(
                inc,
                state=incidents.IncidentState.ERROR,
                comment=str(e),
            )
        )
        raise


def on_incident_dashboard_webhook(event: Event):
    data = event.data
    user = data.get("user")

    id = data.url.query.incident_id
    if not id:
        http_outcome(status_code=400, json={"error": "missing incident_id"})
        return

    inc = store.get_incident(id)
    if not inc:
        http_outcome(status_code=404, json={"error": "incident not found"})
        return

    match data.method:
        case "GET":
            # Handle GET below.
            pass

        case "POST":
            http_outcome(
                status_code=303,
                headers={"Location": f"{inc.dashboard_url + '&msg=notified'}"},
            )

        case _:
            http_outcome(status_code=405, json={"error": "method not allowed"})
            return

    take = '<button name="action" value="take">Take</button>'
    ack = '<button name="action" value="ack">Ack</button>'
    esc = '<button name="action" value="escalate">Escalate</button>'
    resolve = '<button name="action" value="resolve">Resolve</button>'
    notify = '<button name="action" value="notify">Notify</button>'

    form = f"""
        <form method="POST" action="?incident_id={inc.id}">
            {ack if inc.state == IncidentState.ASSIGNED else ""}
            {resolve}
            {take if user else ""}
            {esc if inc.state in (IncidentState.IN_PROGRESS, IncidentState.ASSIGNED) else ""}
            {notify}
        </form>
    """  # noqa: E501

    user = data.get("user")
    msg = data.url.query.get("msg")

    http_outcome(
        status_code=200,
        body=f"""<html>
    <body>
        <h1>Incident {inc.id}</h1>

        {f"<p style='color: green;'>{msg}</p>" if msg else ""}

        <p>State: <b>{inc.state}</b></p>
        <p>Details: <pre>{inc.details}</pre></p>
        <p>Comment: <pre>{inc.comment or "none"}</pre></p>
        <p>Assignee: {inc.assignee or "none"}</p>
        <p>Assigned at: {inc.assigned_at}</p>

        {form if inc.state.is_active else "<p>Incident is no longer active.</p>"}

        <p>You are {user.email if user else "anonymous"}.</p>
    </body>
</html>""",
    )


def init(_):
    """Run this function manually once to initialize the system."""
    print("initialized.")
