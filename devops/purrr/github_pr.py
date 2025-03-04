"""Handler for GitHub "pull_request" events."""

import autokitteh
from autokitteh.slack import normalize_channel_name

import data_helper
import slack_channel
import slack_helper
import text_utils
import users


def on_github_pull_request(event) -> None:
    """Entry-point for AutoKitteh sessions triggered by GitHub "pull_request" events.

    Args:
        event: GitHub event data.
    """
    _parse_github_pr_event(event.data)


def _parse_github_pr_event(data) -> None:
    """Parse a GitHub "pull_request" event and dispatch the appropriate handler.

    About GitHub pull requests and these events:
    - https://docs.github.com/webhooks/webhook-events-and-payloads#pull_request
    - https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests

    Args:
        data: GitHub event data.
    """
    match data.action:
        # A new pull request was created.
        case "opened":
            _on_pr_opened(data.action, data.pull_request, data.sender)
        # A pull request was closed.
        case "closed":
            _on_pr_closed(data.action, data.pull_request, data.sender)
        # A previously closed pull request was reopened.
        case "reopened":
            _on_pr_reopened(data.action, data.pull_request, data.sender)

        # A pull request was converted to a draft.
        case "converted_to_draft":
            _on_pr_converted_to_draft(data.action, data.pull_request, data.sender)
        # A draft pull request was marked as ready for review.
        case "ready_for_review":
            _on_pr_ready_for_review(data.action, data.pull_request, data.sender)

        # Review by a person or team was requested for a pull request.
        case "review_requested":
            _on_pr_review_requested(data)
        # A request for review by a person or team was removed from a pull request.
        case "review_request_removed":
            _on_pr_review_request_removed(data)

        # A pull request was assigned to a user.
        case "assigned":
            _on_pr_assigned(data)
        # A user was unassigned from a pull request.
        case "unassigned":
            _on_pr_unassigned(data)

        # The title or body of a pull request was edited,
        # or the base branch was changed.
        case "edited":
            _on_pr_edited(data.action, data.pull_request, data.changes, data.sender)
        # A pull request's head branch was updated.
        case "synchronize":
            _on_pr_synchronized(data.action, data.pull_request, data.sender)

        # TODO: locked, unlocked

        # Ignored actions:
        # - auto_merge_enabled, auto_merge_disabled
        # - enqueued, dequeued
        # - labeled, unlabeled
        # - milestoned, demilestoned


def _on_pr_opened(action: str, pr, sender) -> None:
    """A new pull request was created (or reopened, or marked as ready for review).

    See also the functions "_on_pr_reopened" and "_on_pr_ready_for_review".

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    # Ignore drafts until they're marked as ready for review.
    if pr.draft:
        return

    channel = slack_channel.initialize_for_github_pr(action, pr, sender)

    # Intercept relevant GitHub and Slack events.
    filter = f"event_type == 'pull_request' && data.number == {pr.number}"
    subs = [autokitteh.subscribe("github_conn", filter=filter)]

    filter = "(event_type == 'message' || event_type.startswith('member_'))"
    filter += f" && data.event.channel == {channel}"
    subs.append(autokitteh.subscribe("slack_conn", filter=filter))

    filter = f"event_type == 'reaction_added' && data.event.item.channel == {channel}"
    subs.append(autokitteh.subscribe("slack_conn", filter=filter))

    # Keep this AutoKitteh session running to handle them until the PR is closed.
    while True:
        data = autokitteh.next_event(subs)

        # GitHub PR event.
        if hasattr(data, "action"):
            print("Received GitHub PR event:", data.action)
            if data.action in ("closed", "converted_to_draft"):
                for sub in subs:
                    autokitteh.unsubscribe(sub)
                break

        # Slack event.
        else:
            print("Received Slack event:", data.event.type)


def _on_pr_closed(action: str, pr, sender) -> None:
    """A pull request (possibly a draft) was closed.

    If "merged" is false in the webhook payload, the pull request was
    closed with unmerged commits. If "merged" is true in the webhook
    payload, the pull request was merged.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    # Ignore drafts - they don't have an active Slack channel anyway.
    if pr.draft:
        return

    slack_channel.archive(action, pr, sender)


def _on_pr_reopened(action: str, pr, sender) -> None:
    """A previously closed pull request (possibly a draft) was reopened.

    Slack bug alert from https://api.slack.com/methods/conversations.unarchive:
    bot tokens ("xoxb-...") cannot currently be used to unarchive conversations.
    For now, please use a user token ("xoxp-...") to unarchive the conversation
    rather than a bot token.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    # Ignore drafts - they don't have an active Slack channel anyway.
    if pr.draft:
        return

    # Workaround for the Slack unarchive bug: treat this as a new PR.
    _on_pr_opened(action, pr, sender)


def _on_pr_converted_to_draft(action: str, pr, sender) -> None:
    """A pull request was converted to a draft.

    For more information, see "Changing the stage of a pull request":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    slack_channel.archive(action, pr, sender)


def _on_pr_ready_for_review(action: str, pr, sender) -> None:
    """A draft pull request was marked as ready for review.

    For more information, see "Changing the stage of a pull request":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request

    Slack bug alert from https://api.slack.com/methods/conversations.unarchive:
    bot tokens ("xoxb-...") cannot currently be used to unarchive conversations.
    For now, please use a user token ("xoxp-...") to unarchive the conversation
    rather than a bot token.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    # Workaround for the Slack unarchive bug: treat this as a new PR.
    _on_pr_opened(action, pr, sender)


def _on_pr_review_requested(data) -> None:
    """Review by a person or team was requested for a pull request.

    For more information, see "Requesting a pull request review":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(data.pull_request, data.action)
    if not channel:
        return

    if data.requested_reviewer:
        reviewer = data.requested_reviewer
        _on_pr_review_requested_person(reviewer, data.sender, channel, "reviewer")
    if data.requested_team:
        _on_pr_review_requested_team(data.requested_team, data.sender, channel)


def _on_pr_review_requested_person(reviewer, sender, channel: str, role: str) -> None:
    """Review by a person was requested for a pull request.

    Args:
        reviewer: GitHub user requested as a reviewer.
        sender: GitHub user who triggered the event.
        channel: PR's Slack channel ID.
        role: "reviewer" or "assignee".
    """
    slack_reviewer = users.format_github_user_for_slack(reviewer)
    self_added = reviewer.login == sender.login
    person = "themselves" if self_added else slack_reviewer
    article = "a" if role == "reviewer" else "an"  # "assignee"

    msg = f"{{}} added {person} as {article} {role}"
    slack_helper.mention_in_message(channel, sender, msg)

    if not slack_reviewer.startswith("<@"):
        return  # Not a real Slack user ID.

    # Remove the "<@" and ">" affixes from the Slack user mention to get the user ID.
    slack_reviewer = slack_reviewer[2:-1]

    if data_helper.slack_opted_out(slack_reviewer):
        return

    slack_channel.add_users(channel, [reviewer.login])

    if self_added:
        return

    # DM the reviewer a reference to the Slack channel.
    msg = f"{{}} added you as {article} {role} to a PR: <#{channel}>"
    slack_helper.mention_in_message(slack_reviewer, sender, msg)


def _on_pr_review_requested_team(team, sender, channel: str) -> None:
    """Review by a team was requested for a pull request.

    Args:
        team: GitHub team requested as a reviewer.
        sender: GitHub user who triggered the event.
        channel: PR's Slack channel ID.
    """
    msg = f"{{}} added the <{team.html_url}|{team.name}> team as a reviewer"
    slack_helper.mention_in_message(channel, sender, msg)


def _on_pr_review_request_removed(data) -> None:
    """A request for review by a person or team was removed from a pull request.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(data.pull_request, data.action)
    if not channel:
        return

    if data.requested_reviewer:
        reviewer = data.requested_reviewer
        _on_pr_review_request_removed_person(reviewer, data.sender, channel, "reviewer")
    if data.requested_team:
        _on_pr_review_request_removed_team(data.requested_team, data.sender, channel)


def _on_pr_review_request_removed_person(
    reviewer, sender, channel: str, role: str
) -> None:
    """A request for review by a person was removed from a pull request.

    Args:
        reviewer: GitHub user requested as a reviewer.
        sender: GitHub user who triggered the event.
        channel: PR's Slack channel ID.
        role: "reviewer" or "assignee".
    """
    slack_reviewer = users.format_github_user_for_slack(reviewer)
    self_added = reviewer.login == sender.login
    person = "themselves" if self_added else slack_reviewer
    article = "a" if role == "reviewer" else "an"  # "assignee"

    msg = f"{{}} removed {person} as {article} {role}"
    slack_helper.mention_in_message(channel, sender, msg)

    if not slack_reviewer.startswith("<@"):
        return  # Not a real Slack user ID.

    # Remove the "<@" and ">" affixes from the Slack user mention to get the user ID.
    slack_reviewer = slack_reviewer[2:-1]

    if data_helper.slack_opted_out(slack_reviewer):
        return

    # TODO: Remove the reviewer from the Slack channel.

    # TODO: Remove the review request DM.


def _on_pr_review_request_removed_team(team, sender, channel: str) -> None:
    """A request for review by a team was removed from a pull request.

    Args:
        team: GitHub team that was requested as a reviewer.
        sender: GitHub user who triggered the event.
        channel: PR's Slack channel ID.
    """
    msg = f"removed the <{team.html_url}|{team.name}> team as a reviewer"
    slack_helper.mention_in_message(channel, sender, "{} " + msg)


def _on_pr_assigned(data) -> None:
    """A pull request was assigned to a user.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(data.pull_request, data.action)
    if not channel:
        return

    _on_pr_review_requested_person(data.assignee, data.sender, channel, "assignee")


def _on_pr_unassigned(data) -> None:
    """A user was unassigned from a pull request.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(data.pull_request, data.action)
    if not channel:
        return

    assignee, sender = data.assignee, data.sender
    _on_pr_review_request_removed_person(assignee, sender, channel, "assignee")


def _on_pr_edited(action: str, pr, changes, sender) -> None:
    """The title or body of a pull request was edited, or the base branch was changed.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        changes: Changed title/body in the PR.
        sender: GitHub user who triggered the event.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(pr, action)
    if not channel:
        return

    # PR base branch was changed.
    if "base" in changes:
        msg = "{} changed the base branch from "
        msg += "`{changes.base.ref}` to `{pr.base.ref}`"
        slack_helper.mention_in_message(channel, sender, msg)

    # PR description was changed.
    if "body" in changes:
        if pr.body:
            msg = "{} updated the PR description:\n\n"
            msg += text_utils.github_to_slack(pr.body, pr.html_url)
        else:
            msg = "{} deleted the PR description"

        slack_helper.mention_in_message(channel, sender, msg)

    # PR title was changed.
    if "title" in changes:
        msg = f"{{}} edited the PR title to: `{pr.title}`"
        slack_helper.mention_in_message(channel, sender, msg)

        name = f"{pr.number}_{normalize_channel_name(pr.title)}"
        slack_helper.rename_channel(channel, name)


def _on_pr_synchronized(action: str, pr, sender) -> None:
    """A pull request's head branch was updated.

    For example, the head branch was updated from the base
    branch or new commits were pushed to the head branch.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    channel = _lookup_channel(pr, action)
    if not channel:
        return

    msg = "{} updated the head branch (see the [PR commits]({pr.url}/commits))"
    slack_helper.mention_in_message(channel, sender, msg)


def _lookup_channel(pr, action: str) -> str | None:
    """Return the ID of a Slack channel that represents a GitHub PR.

    Return None the PR is inactive or the channel ID is not found.
    """
    if pr.draft or pr.state != "open":
        return None

    return slack_helper.lookup_channel(pr.html_url, action)
