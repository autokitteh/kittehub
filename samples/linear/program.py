"""Demonstrates AutoKitteh's Linear integration for managing issues.

This sample shows how to create issues in Linear and retrieve issue information.

This program isn't meant to cover all available functions and events.
It merely showcases various illustrative, annotated, reusable examples.
"""

import os

from autokitteh.linear import linear_client
import queries


linear = linear_client("linear_conn")

TEAM_ID = os.getenv("TEAM_ID", "")  # Must be UUID type.


def create_issue(event):
    """Create a new issue in Linear.

    This function creates an issue with a title and optional description from form data.

    Args:
        event: The HTTP event containing request data.
    """
    if not TEAM_ID:
        print("Error: TEAM_ID environment variable is not set")
        return

    form = event.data.body.form
    issue_title = form.get("title", "AutoKitteh Issue")
    description = form.get("description", "Created by AutoKitteh")

    variables = {"teamId": TEAM_ID, "title": issue_title, "description": description}

    response = linear.post(
        "https://api.linear.app/graphql/",
        json={"query": queries.CREATE_ISSUE_QUERY, "variables": variables},
    )
    response.raise_for_status()

    result = response.json()
    print(result)

    if "data" in result and result["data"] is not None:
        issue = result["data"]["issueCreate"]["issue"]
        issue_id = issue["id"]
        issue_url = issue["url"]

        print(f"Issue '{issue_title}' created successfully!")
        print(f"Issue ID: {issue_id}")
        print(f"Issue URL: {issue_url}")
    else:
        print("Failed to create issue.")
        print("Error:", result.get("errors"))


def get_issue(event):
    """Retrieve information about a Linear issue.

    This function retrieves issue details using an issue ID from query parameters.

    Args:
        event: The HTTP event containing request data.
    """
    issue_id = event.data.url.query.get("issue_id")
    if not issue_id:
        print("Error: issue_id parameter is required")
        return

    variables = {"id": issue_id}
    response = linear.post(
        "https://api.linear.app/graphql/",
        json={"query": queries.GET_ISSUE_QUERY, "variables": variables},
    )
    response.raise_for_status()

    result = response.json()
    print(result)

    if "data" in result and result["data"] is not None:
        issue = result["data"]["issue"]
        print(f"""Issue ID: {issue["id"]}
Title: {issue["title"]}
Description: {issue["description"]}
State: {issue["state"]["name"]}
Priority: {issue["priority"]}
Created: {issue["createdAt"]}
Updated: {issue["updatedAt"]}
URL: {issue["url"]}""")

        if issue["assignee"]:
            print(f"Assignee: {issue['assignee']['name']}")
    else:
        print("Failed to retrieve issue.")
        print("Error:", result.get("errors"))


def update_issue(event):
    """Update an existing Linear issue.

    This function updates an issue's title and/or state.

    Args:
        event: The HTTP event containing request data.
    """
    form = event.data.body.form
    issue_id = form.get("issue_id")
    new_title = form.get("title")
    state_id = form.get("state_id")

    if not issue_id:
        print("Error: issue_id parameter is required")
        return

    # Build update payload.
    update_data = {}
    if new_title:
        update_data["title"] = new_title
    if state_id:
        update_data["stateId"] = state_id

    variables = {"id": issue_id, "input": update_data}
    response = linear.post(
        "https://api.linear.app/graphql/",
        json={"query": queries.UPDATE_ISSUE_QUERY, "variables": variables},
    )
    response.raise_for_status()

    result = response.json()
    print(result)

    if "data" in result and result["data"] is not None:
        issue = result["data"]["issueUpdate"]["issue"]
        print(f"Issue {issue_id} updated successfully!")
        print(f"New title: {issue['title']}")
    else:
        print("Failed to update issue.")
        print("Error:", result.get("errors"))
