"""Demonstration of AutoKitteh's HubSpot integration.

This script showcases two basic operations with the HubSpot API:
creating a new contact and listing all deals.
"""

from autokitteh.hubspot import hubspot_client
from hubspot.crm.contacts import SimplePublicObjectInputForCreate
from hubspot.crm.contacts.exceptions import ApiException


hubspot = hubspot_client("hubspot_conn")


def create_contact(event):
    contact_properties = {
        "email": "meow@autokitteh.com",
        "firstname": "Kitty",
        "lastname": "Meowington",
    }
    try:
        contact_input = SimplePublicObjectInputForCreate(properties=contact_properties)

        # Send a request to HubSpot to create the contact
        response = hubspot.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=contact_input
        )

        print(f"Contact created with ID: {response.id}")
    except ApiException as e:
        print(e)


def list_deals(event):
    for deal in hubspot.crm.deals.get_all():
        print(f"Deal ID: {deal.id}, deal name: {deal.properties.get('dealname')}")
