"""Listen for GitHub pull requests and meow at random people.

This program listens for GitHub pull request events and posts a message
to a Slack channel when a pull request is opened or reopened. It then polls
the pull request until it is closed or merged, updating the message with the
current state of the pull request. Every 15 seconds, it also reads a random
name from a Google Sheet and pages that person in the Slack channel.
"""

from datetime import datetime, UTC
import os
import random
import time

from autokitteh.github import github_client
from autokitteh.google import google_sheets_client
from autokitteh.slack import slack_client


CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID", "")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
ORG_DOMAIN = os.getenv("ORG_DOMAIN", "")

github = github_client("github_conn")
googlesheets = google_sheets_client("googlesheets_conn").spreadsheets().values()
slack = slack_client("slack_conn")


def on_github_pull_request(event):
    """Workflow's entry-point."""
    pr = event.data.pull_request
    msg = f"{pr.html_url} [{pr.state}]"
    ts = slack.chat_postMessage(channel=CHANNEL_ID, text=msg)["ts"]

    i = 0

    while pr.state not in ("closed", "merged"):
        _log(f"Polling #{i}")
        time.sleep(5)

        repo = github.get_repo(event.data.repository.full_name)
        pr = repo.get_pull(pr.number)
        msg = f"{pr.html_url} meow [{pr.state}]"
        slack.chat_update(channel=CHANNEL_ID, ts=ts, text=msg)

        i += 1

        if i % 3 == 0:
            # Spreadsheet contains a list of usernames.
            result = googlesheets.get(spreadsheetId=SHEET_ID, range="A1:A5").execute()
            rows = result.get("values", [])
            the_chosen_one = random.choice(rows)[0]
            _log(f"Meowing at {the_chosen_one}")

            user_email = f"{the_chosen_one}@{ORG_DOMAIN}"
            user = slack.users_lookupByEmail(email=user_email)["user"]
            msg = f"Paging <@{user['id']}>"
            slack.chat_postMessage(channel=CHANNEL_ID, text=msg, thread_ts=ts)


def _log(msg):
    print(f"[{datetime.now(UTC)}] {msg}")
