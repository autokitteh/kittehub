"""A real-life workflow that integrates Confluence and Slack.

Workflow:
    1. Trigger: a new page is created in Confluence
    2. Static filter: the page is in a specific Confluence space
       (specified in the "autokitteh.yaml" manifest file)
    3. Runtime filter: check if the page has a specific label
    4. Notify: send a message to a Slack channel with a snippet of the page
"""

import autokitteh
from autokitteh.atlassian import confluence_client
from autokitteh.slack import slack_client


AK_CONFLUENCE_CONNECTION = "my_confluence"
AK_SLACK_CONNECTION = "my_slack"

CONFLUENCE_LABEL = ""  # TODO: Replace with your Confluence label name
SLACK_CHANNEL = ""  # TODO: Replace with your Slack channel name or ID
SNIPPET_LENGTH = 150


def on_confluence_page_created(event):
    """Workflow's entry-point."""

    confluence = confluence_client(AK_CONFLUENCE_CONNECTION)
    page_id = event.data.page.id

    # Ignore pages without the specified label.
    labels = confluence.get_page_labels(page_id)["results"]
    if not any(label["name"] == CONFLUENCE_LABEL for label in labels):
        return

    # Read the page body.
    res = confluence.get_page_by_id(page_id, expand="body.view, include-labels")
    html_body = res["body"]["view"]["value"]

    page = autokitteh.AttrDict(
        {
            "snippet": f"```{html_body[:SNIPPET_COUNT]}\n```",
            "link": event.data.page.self,
            "space": event.data.page.spaceKey,
            "title": event.data.page.title,
        }
    )

    _send_slack_message(page)


def _send_slack_message(page):
    slack = slack_client(AK_SLACK_CONNECTION)
    message = f"""
    A new page has been created in the `{page.space}` space.
    *Title*: {page.title}
    *Snippet*: {page.snippet}
    <{page.link}|Link to page>
    """
    slack.chat_postMessage(channel=SLACK_CHANNEL, text=message)
