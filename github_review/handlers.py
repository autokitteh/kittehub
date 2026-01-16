"""Handlers for github issue bot"""

from autokitteh import Event
from autokitteh.github import github_client


github = github_client("github")


def on_review_issue_comment(event: Event) -> None:
    """Handle /review commands in issue comments"""
    reviewers = [a.removeprefix("@") for a in event.data.command.args]
    data = event.data.actual_data
    comment = data["comment"]

    repo = github.get_repo(data["repository"]["full_name"])
    n = data["issue"]["number"]
    issue = repo.get_issue(number=n)

    who = comment["user"]["login"]
    if not repo.has_in_collaborators(who):
        _respond(
            issue,
            comment,
            "confused",
            f"user @{who} is not a collaborator",
        )
        return

    if not reviewers:
        _respond(
            issue,
            comment,
            "confused",
            "no reviewers specified",
        )
        return

    nopes = [a for a in reviewers if not repo.has_in_collaborators(a)]
    if nopes:
        _respond(
            issue,
            comment,
            "confused",
            f"users @{', @'.join(nopes)} are not collaborators",
        )
        return

    pr = repo.get_pull(number=n)
    pr.create_review_request(reviewers=reviewers)

    _respond(
        issue,
        comment,
        "+1",
        f"@{', @'.join(reviewers)} added to reviewers",
    )


def on_unreview_issue_comment(event: Event) -> None:
    """Handle /unreview commands in issue comments"""
    reviewers = [a.removeprefix("@") for a in event.data.command.args]
    data = event.data.actual_data
    comment = data["comment"]

    repo = github.get_repo(data["repository"]["full_name"])
    n = data["issue"]["number"]
    issue = repo.get_issue(number=n)

    who = comment["user"]["login"]
    if not repo.has_in_collaborators(who):
        _respond(
            issue,
            comment,
            "confused",
            f"user @{who} is not a collaborator",
        )
        return

    if not reviewers:
        print("unreviewing self")
        reviewers = [who]

    pr = repo.get_pull(number=n)
    pr.delete_review_request(reviewers=reviewers)

    _respond(
        issue,
        comment,
        "+1",
        f"@{', @'.join(reviewers)} removed from reviewers",
    )


def _respond(issue, comment, emoji: str, msg: str) -> None:
    print(f"{emoji}: {msg}")
    issue.create_comment(msg)
    issue.get_comment(comment["id"]).create_reaction(emoji)
