"""Demonstrates AutoKitteh's Notion integration for managing pages.

This sample shows how to create pages in a Notion database
and retrieve page information.

API details:
- Notion API: https://developers.notion.com/
- Python client library: https://github.com/ramnes/notion-sdk-py

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

import os

from autokitteh.notion import notion_client
from notion_client.errors import APIResponseError


notion = notion_client("notion_conn")

DATABASE_ID = os.getenv("DATABASE_ID", "")


def create_page(event):
    """Create a new page in a Notion database.

    This function creates a page with a title from the form data.

    Example usage:
    - URL: "http://localhost:9980/webhooks/<webhook_slug>"
    - Curl command:
      curl -X POST "<URL>" -d "title=My New Page"

    Args:
        event: The HTTP event containing request data.
    """
    form = event.data.body.form
    page_title = form.get("title", "AutoKitteh Page")

    try:
        new_page = notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Name": {"title": [{"text": {"content": page_title}}]},
            },
        )
        page_id = new_page["id"]
        page_url = new_page["url"]
        print(f"Page '{page_title}' created successfully!")
        print(f"Page ID: {page_id}")
        print(f"Page URL: {page_url}")
    except APIResponseError as e:
        print(f"Error: {e}")


def get_page(event):
    """Retrieve information about a Notion page.

    This function retrieves page details using a page ID from query parameters.

    Example usage:
    - URL: "http://localhost:9980/webhooks/<webhook_slug>"
    - Curl command:
      curl "<URL>?page_id=<PAGE_ID>"

    Args:
        event: The HTTP event containing request data.
    """
    page_id = event.data.url.query.get("page_id")

    if not page_id:
        print("Error: page_id parameter is required")
        return

    try:
        # Retrieve the page
        page = notion.pages.retrieve(page_id)

        # Extract and display page information
        print(f"Page ID: {page['id']}")
        print(f"Created time: {page['created_time']}")
        print(f"Last edited: {page['last_edited_time']}")
        print(f"Page URL: {page['url']}")

        # Display properties if available
        if "properties" in page:
            print(f"\nPage properties: {page['properties']}")
    except APIResponseError as e:
        print(f"Error: {e}")
