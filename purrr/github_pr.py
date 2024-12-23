"""Handler for GitHub "pull_request" events."""

import autokitteh

import slack_channel


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
            _on_pr_opened(data)
        # A pull request was closed.
        case "closed":
            _on_pr_closed(data)
        # A previously closed pull request was reopened.
        case "reopened":
            _on_pr_reopened(data)

        # A pull request was converted to a draft.
        case "converted_to_draft":
            _on_pr_converted_to_draft(data)
        # A draft pull request was marked as ready for review.
        case "ready_for_review":
            _on_pr_ready_for_review(data)

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

        # The title or body of a pull request was edited, or the base branch was changed.
        case "edited":
            _on_pr_edited(data)
        # A pull request's head branch was updated.
        case "synchronize":
            _on_pr_synchronized(data)

        # TODO: locked, unlocked

        # Ignored actions:
        # - auto_merge_enabled, auto_merge_disabled
        # - enqueued, dequeued
        # - labeled, unlabeled
        # - milestoned, demilestoned


def _on_pr_opened(data) -> None:
    """A new pull request was created (or reopened, or marked as ready for review).

    See also the functions "_on_pr_reopened" and "_on_pr_ready_for_review".

    Args:
        data: GitHub event data.
    """
    # Ignore drafts until they're marked as ready for review.
    if data.pull_request.draft:
        return

    slack_channel.initialize_for_github_pr(data.action, data.pull_request)

    # Keep an AutoKitteh session running as long as the PR is alive.
    github_subs = autokitteh.subscribe(
        "github_conn", filter="event_type == 'pull_request'"
    )
    while True:
        data = autokitteh.next_event([github_subs])
        print("Received GitHub PR event:", data.action)
        if data.action in ("closed", "converted_to_draft"):
            _parse_github_pr_event(data)
            autokitteh.unsubscribe(github_subs)
            break


def _on_pr_closed(data) -> None:
    """A pull request (possibly a draft) was closed.

    If "merged" is false in the webhook payload, the pull request was
    closed with unmerged commits. If "merged" is true in the webhook
    payload, the pull request was merged.

    Args:
        data: GitHub event data.
    """
    # Ignore drafts - they don't have an active Slack channel anyway.
    if data.pull_request.draft:
        return

    pass  # TODO: Implement this function.


def _on_pr_reopened(data) -> None:
    """A previously closed pull request (possibly a draft) was reopened.

    Slack bug alert from https://api.slack.com/methods/conversations.unarchive:
    bot tokens ("xoxb-...") cannot currently be used to unarchive conversations.
    For now, please use a user token ("xoxp-...") to unarchive the conversation
    rather than a bot token.

    Args:
        data: GitHub event data.
    """
    # Ignore drafts - they don't have an active Slack channel anyway.
    if data.pull_request.draft:
        return

    # Workaround for the Slack unarchive bug: treat this as a new PR.
    _on_pr_opened(data)


def _on_pr_converted_to_draft(data) -> None:
    """A pull request was converted to a draft.

    For more information, see "Changing the stage of a pull request":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request

    Args:
        data: GitHub event data.
    """
    pass  # TODO: Implement this function.


def _on_pr_ready_for_review(data) -> None:
    """A draft pull request was marked as ready for review.

    For more information, see "Changing the stage of a pull request":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request

    Slack bug alert from https://api.slack.com/methods/conversations.unarchive:
    bot tokens ("xoxb-...") cannot currently be used to unarchive conversations.
    For now, please use a user token ("xoxp-...") to unarchive the conversation
    rather than a bot token.

    Args:
        data: GitHub event data.
    """
    # Workaround for the Slack unarchive bug: treat this as a new PR.
    _on_pr_opened(data)


def _on_pr_review_requested(data) -> None:
    """Review by a person or team was requested for a pull request.

    For more information, see "Requesting a pull request review":
    https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.


def _on_pr_review_requested_person(data, channel_id: str) -> None:
    """Review by a person was requested for a pull request.

    Args:
        data: GitHub event data.
        channel_id: PR's Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _on_pr_review_requested_team(data, channel_id: str) -> None:
    """Review by a team was requested for a pull request.
    Args:
        data: GitHub event data.
        channel_id: PR's Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _on_pr_review_request_removed(data) -> None:
    """A request for review by a person or team was removed from a pull request.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.


def _on_pr_review_request_removed_person(data, channel_id: str) -> None:
    """A request for review by a person was removed from a pull request.

    Args:
        data: GitHub event data.
        channel_id: PR's Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _on_pr_review_request_removed_team(data, channel_id: str) -> None:
    """A request for review by a team was removed from a pull request.

    Args:
        data: GitHub event data.
        channel_id: PR's Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _on_pr_assigned(data) -> None:
    """A pull request was assigned to a user.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.


def _on_pr_unassigned(data) -> None:
    """A user was unassigned from a pull request.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.


def _on_pr_edited(data) -> None:
    """The title or body of a pull request was edited, or the base branch was changed.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.


def _on_pr_synchronized(data) -> None:
    """A pull request's head branch was updated.

    For example, the head branch was updated from the base
    branch or new commits were pushed to the head branch.

    Args:
        data: GitHub event data.
    """
    # Don't do anything if there isn't an active Slack channel anyway.
    if data.pull_request.draft or data.pull_request.state != "open":
        return

    pass  # TODO: Implement this function.
