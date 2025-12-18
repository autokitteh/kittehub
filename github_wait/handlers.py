"""Handlers for github issue bot"""

from github import Issue
from github import PullRequest

from autokitteh import Event
from autokitteh.github import github_client


github = github_client("github")


# waiting only for push.
_waiting_push_label = "waiting"

# waiting for either push or comment.
_waiting_any_label = "waiting:any"

_IssueOrPR = Issue.Issue | PullRequest.PullRequest


# Can be called on either issue comments, pr review comments, or pr review submitted.
def on_command(event: Event) -> None:
    match event.data.command.name:
        case "wait":
            add, remove = _waiting_push_label, _waiting_any_label
        case "wait-any":
            add, remove = _waiting_any_label, _waiting_push_label
        case _:
            print("unhandled command")
            return

    data = event.data.actual_data

    repo = github.get_repo(data.repository.full_name)

    if data.get("issue"):
        issue: _IssueOrPR = repo.get_issue(number=data.issue.number)
    elif data.get("pull_request"):
        issue = repo.get_pull(number=data.pull_request.number)

    _label(issue, adds=[add], removes=[remove])

    if data.get("comment"):
        issue.get_comment(data.comment.id).create_reaction("+1")


def on_pull_request_sync(event: Event) -> None:
    data = event.data

    repo = github.get_repo(data.repository.full_name)
    pr = repo.get_pull(data.number)

    _label(pr, adds=[], removes=[_waiting_push_label, _waiting_any_label])


def on_issue_comment(event: Event) -> None:
    data = event.data

    if not any(
        label["name"] in [_waiting_any_label, _waiting_push_label]
        for label in data.issue.labels
    ):
        print("not waiting, ignored")
        return

    if data.slash_commands and any(
        cmd["name"] in ["wait", "wait-any"] for cmd in data.slash_commands
    ):
        # Don't remove labels if this comment is a command.
        print("comment contains wait command, ignored")
        return

    repo = github.get_repo(data.repository.full_name)
    issue = repo.get_issue(data.issue.number)

    # Remove only wait-any label on new comment.
    _label(issue, adds=[], removes=[_waiting_any_label])


def on_pull_request_review_comment(event: Event) -> None:
    data = event.data

    if not any(
        label["name"] in [_waiting_any_label, _waiting_push_label]
        for label in data.pull_request.labels
    ):
        print("not waiting, ignored")
        return

    if data.slash_commands and any(
        cmd["name"] in ["wait", "wait-any"] for cmd in data.slash_commands
    ):
        # Don't remove labels if this comment is a command.
        print("comment contains wait command, ignored")
        return

    repo = github.get_repo(data.repository.full_name)
    pr = repo.get_pull(data.pull_request.number)

    # Remove only wait-any label on new comment.
    _label(pr, adds=[], removes=[_waiting_any_label])


def on_pull_request_review(event: Event) -> None:
    data = event.data

    if not any(
        label["name"] in [_waiting_any_label, _waiting_push_label]
        for label in data.pull_request.labels
    ):
        print("not waiting, ignored")
        return

    if data.slash_commands and any(
        cmd["name"] in ["wait", "wait-any"] for cmd in data.slash_commands
    ):
        # Don't remove labels if this comment is a command.
        print("comment contains wait command, ignored")
        return

    repo = github.get_repo(data.repository.full_name)
    pr = repo.get_pull(data.pull_request.number)

    # Remove only wait-any label on new comment.
    _label(pr, adds=[], removes=[_waiting_any_label])


def _label(issue: _IssueOrPR, adds: list[str], removes: list[str]) -> None:
    labels = {label.name for label in issue.get_labels()}

    for remove in removes:
        if remove in labels:
            print(f"removing label {remove}")
            issue.remove_from_labels(remove)

    for add in adds:
        if add not in labels:
            print(f"adding label {add}")
            issue.add_to_labels(add)
