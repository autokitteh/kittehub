"""Demonstrates AutoKitteh’s Auth0 integration for managing tasks via the Auth0 API."""

from datetime import datetime, timedelta, UTC
import os

from autokitteh.auth0 import auth0_client


ROLE_ID = os.getenv("ROLE_ID", "")

auth0 = auth0_client("auth_conn")


def assign_role(event):
    """Entry-point function for a webhook-based workflow assigning a role to a user."""
    user = event.data.body.form.get("user_id", "")
    auth0.roles.add_users(ROLE_ID, [user])
    print(f"Assigned role {ROLE_ID!r} to user {user!r}")


def weekly_user_growth(_):
    """Fetch and display the number of users created in the past week."""
    # Remove the unit suffix ("d") and parse as an integer.
    interval_days = int((os.getenv("TIME_INTERVAL", "7d"))[:-1])
    end_time = datetime.now(UTC).replace(second=0, microsecond=0)
    start_time = end_time - timedelta(minutes=interval_days)

    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    query = f"created_at:[{start_time_iso} TO {end_time_iso}]"

    response = auth0.users.list(q=query, search_engine="v3")
    new_users = response.get("users", [])

    print(f"New users in the past week: {len(new_users)}")
    for user in new_users:
        print(f"- {user['email']} (created at: {user['created_at']})")
