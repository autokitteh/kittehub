"""Audit compliance controls related to issue tracking systems."""

from datetime import datetime
import os

from autokitteh.github import github_client
from github.PullRequest import PullRequest


GITHUB_ORG_NAME = os.getenv("github_conn__target_name", "")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "")
GITHUB_BRANCH_NAME = os.getenv("GITHUB_BRANCH_NAME", "")

START_TIME = datetime.fromisoformat(os.getenv("START_TIME", "1970-01-01T00:00:00Z"))
END_TIME = datetime.fromisoformat(os.getenv("END_TIME", "2099-12-31T00:00:00Z"))

gh = github_client("github_conn")


def on_trigger(_) -> None:
    pass  # TODO: Implement this function.


def merged_prs_linked_to_issues(prs: list[PullRequest]):
    pass  # TODO: Implement this function.


def done_issues_linked_to_prs():
    pass  # TODO: Implement this function.
