"""Handlers for github issue bot"""

from autokitteh import Event
from autokitteh.github import github_client


github = github_client("github")


def on_assign_issue_comment(event: Event) -> None:
    """Handle /assign commands in issue comments"""
    data = event.data

    comment = data["comment"]
    cmd = comment["body"].strip().split()

    print(f"command: {cmd!r}")

    if cmd[0] != "/assign":
        print("irrelevant command")
        return

    assignees = [a.removeprefix("@") for a in cmd[1:]]

    repo = github.get_repo(data["repository"]["full_name"])
    issue = repo.get_issue(number=data["issue"]["number"])

    who = comment["user"]["login"]
    if not repo.has_in_assignees(who):
        _respond(
            issue,
            comment,
            "confused",
            f"user @{who} is not allowed to be an assignee",
        )
        return

    if not assignees:
        print("assigning to self")
        assignees = [who]
    else:
        nopes = [a for a in assignees if not repo.has_in_assignees(a)]
        if nopes:
            _respond(
                issue,
                comment,
                "confused",
                f"users @{', @'.join(nopes)} are not allowed to be assignees",
            )
            return

    issue.add_to_assignees(*assignees)

    _respond(
        issue,
        comment,
        "+1",
        f"assigned to @{', @'.join(assignees)}",
    )


def on_unassign_issue_comment(event: Event) -> None:
    """Handle /unassign commands in issue comments"""
    data = event.data

    comment = data["comment"]
    cmd = comment["body"].strip().split()

    print(f"command: {cmd!r}")

    if cmd[0] != "/unassign":
        print("irrelevant command")
        return

    assignees = [a.removeprefix("@") for a in cmd[1:]]

    repo = github.get_repo(data["repository"]["full_name"])
    issue = repo.get_issue(number=data["issue"]["number"])

    who = comment["user"]["login"]
    if not repo.has_in_assignees(who):
        _respond(
            issue,
            comment,
            "confused",
            f"user @{who} is not allowed to unassign",
        )
        return

    if not assignees:
        print("unassigning self")
        assignees = [who]

    issue.remove_from_assignees(*assignees)

    _respond(
        issue,
        comment,
        "+1",
        f"unassigned @{', @'.join(assignees)}",
    )


def _respond(issue, comment, emoji: str, msg: str) -> None:
    print(f"{emoji}: {msg}")
    issue.create_comment(msg)
    issue.get_comment(comment["id"]).create_reaction(emoji)
