from autokitteh.slack import slack_client
from slack_sdk.errors import SlackApiError


client = slack_client("slack")


def send(*args, **kwargs) -> None:
    """Send a message to a Slack channel."""
    try:
        client.chat_postMessage(*args, **kwargs)
    except SlackApiError as e:
        print(f"Error posting to Slack {args} {kwargs}: {e.response['error']}")
