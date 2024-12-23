"""Create and manage Slack channels."""

import json

from slack_sdk.errors import SlackApiError

import slack_helper
import users


_MAX_METADATA_LENGTH = 250  # Characters.


slack = slack_helper.shared_client


def initialize_for_github_pr(action: str, pr) -> None:
    """Initialize a dedicated Slack channel for a GitHub PR.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
    """
    # Sanity check the GitHub PR event action.
    if action not in ("opened", "reopened", "ready_for_review"):
        error = "Unexpected GitHub PR event action for initializing a Slack channel"
        slack_helper.debug(f"{error}: `{action}`")
        raise ValueError(f"{error}: `{action}`")

    print(f"Creating Slack channel for {pr.html_url} (PR event action: {action})")
    print(json.dumps(pr, indent=2, sort_keys=True))

    name = f"{pr.number}_{slack_helper.normalize_channel_name(pr.title)}"
    channel_id = slack_helper.create_channel(name)
    if not channel_id:
        _report_creation_error(pr)
        return

    _set_topic(pr, channel_id)
    _set_description(pr, channel_id)
    _set_bookmarks(pr, channel_id)

    # TODO: Post an introduction message to the new channel, describing the PR.

    # TODO: Also post a message summarizing check states (updated
    # later based on "workflow_job" and "workflow_run" events).

    # TODO: In case this is a replacement Slack channel, say so.

    # TODO: Map between the GitHub PR and the Slack channel ID, for 2-way event syncs.

    # TODO: Finally, add all the participants in the PR to this channel.


def _report_creation_error(pr) -> None:
    github_username = pr.user.login
    github_org = pr.base.repo.owner.login
    user_id = users.github_username_to_slack_user_id(github_username, github_org)

    error = "Failed to create Slack channel for " + pr.html_url
    slack_helper.debug(error)
    try:
        slack.chat_postMessage(channel=user_id, text=error)
    except SlackApiError as e:
        error = f"Failed to notify <@{user_id}> (`{github_username}` in GitHub)"
        error += " about failing to create Slack channel for "
        error += f"{pr.html_url}: `{e.response["error"]}`"
        slack_helper.debug(error)
    return


def _set_bookmarks(pr, channel_id: str) -> None:
    """Set the bookmarks of a Slack channel to important PR links.

    Bookmark titles should be updated later based on relevant GitHub events.

    Args:
        pr: GitHub PR event data.
        channel_id: Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _set_description(pr, channel_id: str) -> None:
    """Set the description of a Slack channel to a GitHub PR title.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR event data.
        channel_id: Slack channel ID.
    """
    title = f"`{pr.title}`"
    if len(title) > _MAX_METADATA_LENGTH:
        title = title[: _MAX_METADATA_LENGTH - 4] + "`..."
    try:
        slack.conversations_setPurpose(channel=channel_id, purpose=title)
    except SlackApiError as e:
        error = f"Failed to set the purpose of <#{channel_id}> to `{title}`"
        slack_helper.debug(error + f": `{e.response['error']}`")


def _set_topic(pr, channel_id: str) -> None:
    """Set the topic of a Slack channel to a GitHub PR URL.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR event data.
        channel_id: Slack channel ID.
    """
    topic = pr.html_url
    if len(topic) > _MAX_METADATA_LENGTH:
        topic = topic[: _MAX_METADATA_LENGTH - 4] + " ..."
    try:
        slack.conversations_setTopic(channel=channel_id, topic=topic)
    except SlackApiError as e:
        error = f"Failed to set the topic of <#{channel_id}> to `{topic}`"
        slack_helper.debug(error + f": `{e.response['error']}`")
