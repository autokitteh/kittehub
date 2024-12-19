"""This program adds new Auth0 users to HubSpot as contacts."""

import datetime
import os

from autokitteh.auth0 import auth0_client
from autokitteh.hubspot import hubspot_client
from hubspot.crm.contacts import SimplePublicObjectInput

auth0 = auth0_client("auth0_conn")
hubspot = hubspot_client("hubspot_conn")

LOOKUP_HOURS = int(os.getenv("HOURS"))


def check_for_new_users(event):
    """Workflow entrypoint.

    Looks up new Auth0 users in the last `HOURS` hours and adds them to HubSpot as contacts.
    """
    time_range = _get_time_range(LOOKUP_HOURS)
    query = f"created_at:[{time_range['start']} TO {time_range['end']}]"

    response = auth0.users.list(q=query, search_engine="v3")
    add_new_users(response["users"])


def _get_time_range(hours):
    """Calculate start and end times for user lookup."""
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(hours=hours)

    return {"start": start_time.isoformat() + "Z", "end": now.isoformat() + "Z"}


def add_new_users(users):
    """Add new Auth0 users to HubSpot as contacts."""
    for user in users:
        contact = _create_hubspot_contact(user)
        hubspot.crm.contacts.basic_api.create(contact)


def _create_hubspot_contact(user):
    """Convert Auth0 user data to HubSpot contact format."""
    user_data = {
        "email": user["email"],
        "firstname": user["given_name"],
        "lastname": user["family_name"],
    }
    return SimplePublicObjectInput(properties=user_data)
