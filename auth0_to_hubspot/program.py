"""This program adds new Auth0 users to HubSpot as contacts."""

from datetime import datetime, timedelta, UTC
import os

from autokitteh.auth0 import auth0_client
from autokitteh.hubspot import hubspot_client
from hubspot.crm.contacts import SimplePublicObjectInput


LOOKUP_HOURS = int(os.getenv("HOURS", "24"))

auth0 = auth0_client("auth0_conn")
hubspot = hubspot_client("hubspot_conn")


def check_for_new_users(event):
    """Workflow entrypoint.

    Looks up new Auth0 users in the last `HOURS` hours,
    and adds them to HubSpot as contacts.
    """
    start, end = _get_time_range(LOOKUP_HOURS)
    query = f"created_at:[{start} TO {end}]"
    response = auth0.users.list(q=query, search_engine="v3")
    add_new_users(response["users"])


def _get_time_range(hours):
    """Calculate start and end times for user lookup."""
    now = datetime.now(UTC)
    start_time = now - timedelta(hours=hours)

    start_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_formatted = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return (start_formatted, end_formatted)


def add_new_users(users):
    """Add new Auth0 users to HubSpot as contacts."""
    for user in users:
        contact = _create_hubspot_contact(user)
        try:
            hubspot.crm.contacts.basic_api.create(contact)
            print(f"Added to HubSpot: {user['email']}")
        except Exception as e:
            # TODO: Replace "Exception" with a specific error for
            # conflicts, i.e. don't ignore other types of errors.
            # print(f"Contact already exists in HubSpot: {user['email']}")
            print(f"Failed to add {user['email']} to HubSpot: {e}")
            continue


def _create_hubspot_contact(user):
    """Convert Auth0 user data to HubSpot contact format."""
    first_name = user.get("given_name") or user.get("name", "").split(" ")[0]
    last_name = user.get("family_name") or " ".join(user.get("name", "").split(" ")[1:])

    user_data = {
        "email": user["email"],
        "firstname": first_name,
        "lastname": last_name,
    }
    return SimplePublicObjectInput(properties=user_data)
