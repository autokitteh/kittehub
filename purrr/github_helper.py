"""Thin layer of logic on top of the GitHub API."""

from autokitteh.github import github_client


shared_client = github_client("github_conn")
