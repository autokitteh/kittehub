"""Demonstrates AutoKitteh’s Auth0 integration for managing tasks via the Auth0 API."""

from datetime import datetime, timedelta, UTC
import os

from autokitteh.auth0 import auth0_client


auth0 = auth0_client("auth_conn")

ROLE_ID = os.getenv("ROLE_ID", "")


def assign_role(event):
    user = event.data.body.form.get("user_id")
    auth0.roles.add_users(ROLE_ID, [user])
    print(f"Assigned role {ROLE_ID!r} to user {user!r}")


def weekly_user_growth(_):
    """Fetch and display the number of users created in the past week."""
    one_week_ago = (datetime.now(UTC) - timedelta(days=7)).isoformat()
    query = f"created_at:[{one_week_ago} TO *]"

    response = auth0.users.list(q=query, search_engine="v3")
    new_users = response.get("users", [])

    print(f"New Users in the Past Week: {len(new_users)}")
    for user in new_users:
        print(f"- {user['email']} (Created At: {user['created_at']})")
