"""Forward GitHub Marketplace webhook notifications to a Slack channel.

GitHub API documentation:
- https://docs.github.com/en/apps/github-marketplace/listing-an-app-on-github-marketplace/configuring-a-webhook-to-notify-you-of-plan-changes
- https://docs.github.com/en/webhooks/webhook-events-and-payloads#marketplace_purchase
- https://docs.github.com/en/webhooks/webhook-events-and-payloads#ping
"""

import hashlib
import hmac
import json
import os

import autokitteh
from autokitteh.slack import slack_client


def on_webhook_notification(event):
    """Handle GitHub Marketplace webhook notifications.

    Args:
        event: Incoming HTTP request data.
    """
    headers = event.data.headers

    secret = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    signature = headers.get("X-Hub-Signature-256", "")
    _verify_signature(event.data.body.bytes, secret, signature)

    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#delivery-headers
    msg = f"*GitHub Marketplace event:* `{headers.get('X-Github-Event', '???')}`\n"
    msg += f"(Resource ID `{headers.get('X-Github-Hook-Installation-Target-Id')}`, "
    msg += f"webhook ID `{headers.get('X-Github-Hook-Id')}`, "
    msg += f"event ID `{headers.get('X-Github-Delivery')}`)\n"

    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#marketplace_purchase
    # https://docs.github.com/en/webhooks/webhook-events-and-payloads#ping
    msg += f"```{json.dumps(event.data.body.json, indent=4)}```"

    channel = os.getenv("SLACK_CHANNEL_NAME_OR_ID", "")
    slack_client("slack_conn").chat_postMessage(channel=channel, text=msg)


@autokitteh.activity
def _verify_signature(payload: bytes, secret: str, signature: str):
    """Verify that the payload was sent from GitHub by validating its SHA-256 signature.

    Based on:
    https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries

    Args:
        payload: Original request body to verify.
        secret: GitHub Marketplace webhook secret of the GitHub app.
        signature: HTTP header received from GitHub ("X-Hub-Signature-256").

    Raises:
        RuntimeError: If the signature is missing or doesn't match the expected value.
    """
    if not signature:
        raise RuntimeError("'X-Hub-Signature-256' HTTP header is missing!")

    hash = hmac.new(secret.encode("utf-8"), msg=payload, digestmod=hashlib.sha256)
    expected = "sha256=" + hash.hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise RuntimeError("Request signatures didn't match!")
