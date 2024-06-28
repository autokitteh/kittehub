"""A real-life workflow that integrates Confluence and Slack."""

import autokitteh
from autokitteh.atlassian import confluence_client
from autokitteh.slack import slack_client


AK_CONFLUENCE_CONNECTION = "my_confluence"
AK_SLACK_CONNECTION = "my_slack"

SLACK_CHANNEL = ""  # TODO: Replace with your Slack channel name or ID
SNIPPET_COUNT = 150


def on_confluence_page_created(event):
    """Workflow's entry-point."""

    # get the page body
    confluence = confluence_client(AK_CONFLUENCE_CONNECTION)
    res = confluence.get_page_by_id(event.data.page.id, expand="body.view")
    html_body = res["body"]["view"]["value"]

    page = autokitteh.AttrDict(
        {
            "snippet": "```" + html_body[:SNIPPET_COUNT] + "\n```",
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
