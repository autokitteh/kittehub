"""Thin layer of logic on top of the GitHub API."""

import os

from autokitteh.github import github_client


ORG_NAME = os.getenv("github_conn__target_name", "")

shared_client = github_client("github_conn")
