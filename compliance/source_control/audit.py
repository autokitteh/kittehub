"""Audit compliance controls related to source control systems."""

from datetime import datetime
import os

from autokitteh.github import github_client
from github.Commit import Commit
from github.PullRequest import PullRequest
from github.Repository import Repository

import sheets


GITHUB_ORG_NAME = os.getenv("github_conn__target_name", "")
GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "")
GITHUB_BRANCH_NAME = os.getenv("GITHUB_BRANCH_NAME", "")

START_TIME = datetime.fromisoformat(os.getenv("START_TIME", "1970-01-01T00:00:00Z"))
END_TIME = datetime.fromisoformat(os.getenv("END_TIME", "2099-12-31T00:00:00Z"))

gh = github_client("github_conn")


def on_trigger(_) -> None:
    repo = gh.get_repo(f"{GITHUB_ORG_NAME}/{GITHUB_REPO_NAME}")
    all_commits = _merged_commits(repo)
    print(f"Total commits to {GITHUB_BRANCH_NAME!r}: {len(all_commits)}")
    all_prs = _merged_prs(repo)
    print("Total merged PRs: ", len(all_prs))

    prs = list(merged_prs_with_unverified_commits(all_prs))
    sheets.save_violations("Unverified commits", prs)

    commits = list(commits_directly_to_main_branch_without_pr(all_commits))
    sheets.save_violations("Commits without PRs", commits)

    prs = list(merged_prs_without_approval(all_prs))
    sheets.save_violations("Unapproved PRs", prs)

    commits = list(merged_prs_with_failing_tests(all_commits))
    sheets.save_violations("Failing tests", commits)


def merged_prs_with_unverified_commits(prs: list[PullRequest]):
    for pr in prs:
        if any(not _is_verified(commit) for commit in pr.get_commits()):
            yield pr


def commits_directly_to_main_branch_without_pr(commits: list[Commit]):
    for commit in commits:
        if commit.get_pulls().totalCount == 0:
            yield commit


def merged_prs_without_approval(prs: list[PullRequest]):
    for pr in prs:
        if not any(review.state == "APPROVED" for review in pr.get_reviews()):
            yield pr


def merged_prs_with_failing_tests(commits: list[Commit]):
    # Note: this checks the commit that merged the PR into the main branch,
    # not the PR's pre-merge checks. This is a choice, not a limitation.
    for commit in commits:
        if any(check.conclusion == "failure" for check in commit.get_check_suites()):
            yield commit


def _is_verified(commit: Commit) -> bool:
    return commit.commit.raw_data["verification"]["verified"]


def _merged_commits(repo: Repository) -> list[Commit]:
    commits = repo.get_commits(sha=GITHUB_BRANCH_NAME, since=START_TIME, until=END_TIME)
    return sorted(commits, key=lambda commit: commit.commit.last_modified)


def _merged_prs(repo: Repository) -> list[PullRequest]:
    all_prs = repo.get_pulls(
        state="closed",
        sort="updated",
        direction="desc",  # Important for the optimization below.
        base=GITHUB_BRANCH_NAME,
    )
    relevant_prs = []
    for pr in all_prs:
        if pr.updated_at < START_TIME:
            break  # Runtime performance optimization.
        if pr.merged and START_TIME <= pr.merged_at < END_TIME:
            relevant_prs.append(pr)

    return sorted(relevant_prs, key=lambda pr: pr.merged_at)
