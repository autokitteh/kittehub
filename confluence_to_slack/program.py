"""A real-life workflow that integrates Confluence and Slack.

Workflow:
    1. Trigger: a new page is created in Confluence
    2. Static filter: the page is in a specific Confluence space
       (specified in the "autokitteh.yaml" manifest file)
    3. Runtime filter: check if the page has a specific label
    4. Notify: send a message to a Slack channel with a snippet of the page
"""

import os

import autokitteh
from autokitteh.atlassian import confluence_client
from autokitteh.slack import slack_client


def on_confluence_page_created(event):
    """Workflow's entry-point."""

    confluence = confluence_client(os.getenv("AK_CONFLUENCE_CONNECTION"))
    page_id = event.data.page.id

    # Ignore pages without the specified label.
    labels = confluence.get_page_labels(page_id)["results"]
    if not any(label["name"] == os.getenv("CONFLUENCE_LABEL") for label in labels):
        return

    # Read the page body.
    res = confluence.get_page_by_id(page_id, expand="body.view, include-labels")
    html_body = res["body"]["view"]["value"]

    _send_slack_message(event.data.page, html_body)


def _send_slack_message(page, html_body):
    slack = slack_client(os.getenv("AK_SLACK_CONNECTION"))
    snippet_length = int(os.getenv("SNIPPET_LENGTH"))
    message = f"""
    A new page has been created in the `{page.spaceKey}` space.
    *Title*: {page.title}
    *Snippet*: ```{html_body[:snippet_length]}\n```
    <{page.self}|Link to page>
    """
    slack.chat_postMessage(channel=os.getenv("SLACK_CHANNEL"), text=message)
