"""Demonstration of AutoKitteh's HubSpot integration.

This script showcases two basic operations with the HubSpot API:
creating a new contact and listing all deals.
"""

from autokitteh.hubspot import hubspot_client
from hubspot.crm.contacts import SimplePublicObjectInputForCreate


hubspot = hubspot_client("hubspot_conn")


def create_contact(event):
    email = event.data.url.query.get("email", "meow@autokitteh.com")
    firstname = event.data.url.query.get("firstname", "Kitty")
    lastname = event.data.url.query.get("lastname", "Meowington")

    contact_properties = {
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
    }
    contact_input = SimplePublicObjectInputForCreate(properties=contact_properties)

    response = hubspot.crm.contacts.basic_api.create(
        simple_public_object_input_for_create=contact_input
    )

    print(f"Contact created with ID: {response.id}")


def list_deals(event):
    for deal in hubspot.crm.deals.get_all():
        print(f"Deal ID: {deal.id}, deal name: {deal.properties.get('dealname')}")
