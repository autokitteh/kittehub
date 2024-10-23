"""This program demonstrates AutoKitteh's GitHub integration.

This program implements multiple entry-point functions that are triggered by
various GitHub webhook events, which are defined in the "autokitteh.yaml"
manifest file. It also executes various GitHub API calls.

API details:
- REST API referene: https://docs.github.com/en/rest
- PyGitHub library: https://pygithub.readthedocs.io/en/latest/index.html

This program isn't meant to cover all available functions and events.
It merely showcases a few illustrative, annotated, reusable examples.
"""

import random

from autokitteh.github import github_client

# https://docs.github.com/en/rest/reactions/reactions#about-reactions
REACTIONS = ["+1", "-1", "laugh", "confused", "heart", "hooray", "rocket", "eyes"]


def on_github_issue_comment(event):
    """https://docs.github.com/en/rest/overview/github-event-types#issuecommentevent

    Based on the filter in the "autokitteh.yaml" manifest file,
    handle only *new* issue comments in this sample code
    (FYI, the other options are "edited" and "deleted").

    Args:
        event: GitHub event data.
    """
    g = github_client("github_conn")
    repo = g.get_repo(event.data.repository.full_name)
    issue = repo.get_issue(event.data.issue.number)
    comment = issue.get_comment(event.data.comment.id)
    comment.create_reaction(random.choice(REACTIONS))
