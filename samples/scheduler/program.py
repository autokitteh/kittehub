"""This program demonstrates AutoKitteh's scheduler capabilities.

It implements a single entry-point function, configured in the "autokitteh.yaml"
file to receive "scheduler" events, and uses constant values defined in the
"autokitteh.yaml" manifest for each AutoKitteh environment.
"""

from datetime import datetime, timedelta, UTC
import os

from autokitteh.github import github_client


# Set in "autokitteh.yaml"
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")
OPENED_CUTOFF = os.getenv("OPENED_CUTOFF")
UPDATE_CUTOFF = os.getenv("UPDATE_CUTOFF")

github = github_client("github_conn")


def on_cron_trigger(_):
    """Handles the AutoKitteh cron schedule trigger."""
    # Fetch open pull requests that are not drafts or WIP
    repo = github.get_repo(f"{GITHUB_OWNER}/{GITHUB_REPO}")
    active_prs = [
        pr
        for pr in repo.get_pulls(state="open")
        if not pr.draft
        and "draft" not in pr.title.lower()
        and "wip" not in pr.title.lower()
    ]

    now = datetime.now(UTC)
    opened_cutoff = now - timedelta(days=int(OPENED_CUTOFF))
    update_cutoff = now - timedelta(days=int(UPDATE_CUTOFF))

    msg = "Daily reminder about stalled PRs:"

    for pr in active_prs:
        stalled_details = _get_stalled_pr_details(pr, now, opened_cutoff, update_cutoff)

        if stalled_details:
            print(f"PR {pr.number} is stalled")
            msg += f"\nPR: `{pr.title}`\n  {pr.url}\n  {stalled_details}\n"
            print(msg)


def _get_stalled_pr_details(pr, now, opened_cutoff, update_cutoff):
    """Returns details if a PR is stalled, otherwise returns an empty string."""
    details = []

    if pr.created_at < opened_cutoff:
        details.append(f"opened {_hours_ago(now, pr.created_at)}h ago")
    if pr.updated_at < update_cutoff:
        details.append(f"last updated {_hours_ago(now, pr.updated_at)}h ago")

    return ", ".join(details)


def _hours_ago(now, past_time):
    """Returns the number of hours between now and a past datetime."""
    delta = now - past_time
    return delta.total_seconds() // 3600
