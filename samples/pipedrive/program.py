"""Demonstrates AutoKitteh's Pipedrive integration for managing deals.

This sample shows how to create deals in Pipedrive
and retrieve deal information.

API details:
- Pipedrive API: https://developers.pipedrive.com/
- Python client library: https://github.com/pipedrive/client-python

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

from autokitteh.pipedrive import pipedrive_client


pipedrive = pipedrive_client("pipedrive_conn")


def create_deal(event):
    """Create a new deal in Pipedrive."""
    form = event.data.body.form
    deal_title = form.get("title", "AutoKitteh Deal")
    deal_value = form.get("value", "1000")

    # Create a new deal
    response = pipedrive.deals.create_deal(
        {
            "title": deal_title,
            "value": deal_value,
        }
    )

    if "success" in response and response["success"]:
        deal = response["data"]
        deal_id = deal["id"]
        deal_title = deal["title"]
        print(f"Deal '{deal_title}' created successfully!")
        print(f"Deal ID: {deal_id}")
        print(f"Value: {deal.get('value')} {deal.get('currency')}")
    else:
        print(f"Error creating deal: {response}")


def fetch_all_deals(_):
    """Retrieve information about all Pipedrive deals."""
    response = pipedrive.deals.get_all_deals()
    deals = response["data"]
    for deal in deals:
        print(deal["title"], "(worth", deal["value"], deal["currency"] + ")")
