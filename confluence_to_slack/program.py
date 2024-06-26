"""
When a new Confluence page is created in a specific space, if the page has
a certain label, parse the page body and send certain fields to Slack.
Then, send a webhook request to a public URL.
"""

import autokitteh
from autokitteh.slack import slack_client


AK_SLACK_CONNECTION = "my_slack"


def on_confluence_page_created(event):
    """Workflow's entry-point, triggered by an incoming Confluence event."""
    # TODO: Check to make sure that the page is created in a specific space.
    # If not, ignore the event. OR is this something that can be setup in the
    # trigger?

    # TODO: Check for specific label on the page. If not present, ignore the
    # event.

    # TODO: Extract the necessary fields from the page body.

    # TODO: Send the extracted fields to Slack.
    _send_slack_message(fields=None)


def _send_slack_message(fields):
    slack = slack_client(AK_SLACK_CONNECTION)
    text = "Hello, world!"
    slack.chat_postMessage(channel="pasha-test", text=text)
