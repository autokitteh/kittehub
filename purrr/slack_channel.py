"""Create and manage Slack channels."""

import json

from slack_sdk.errors import SlackApiError

import data_helper
import debug
import markdown
import slack_helper
import users


_MAX_METADATA_LENGTH = 250  # Characters.


slack = slack_helper.shared_client


def initialize_for_github_pr(action: str, pr, sender) -> str:
    """Initialize a dedicated Slack channel for a GitHub PR.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user object of the PR sender.

    Returns:
        ID of the created Slack channel.
    """
    print(f"Creating Slack channel for {pr.html_url} (PR event action: {action})")
    print(json.dumps(pr, indent=2, sort_keys=True))

    name = f"{pr.number}_{slack_helper.normalize_channel_name(pr.title)}"
    channel = slack_helper.create_channel(name)
    if not channel:
        _report_creation_error(pr, sender.login)

    _set_topic(pr, channel)
    _set_description(pr, channel)
    _set_bookmarks(pr, channel)
    _post_messages(action, pr, sender, channel)

    # TODO: Map between the GitHub PR and the Slack channel ID, for 2-way event syncs.

    # TODO: Finally, add all the participants in the PR to this channel.

    return channel


def _report_creation_error(pr, github_username) -> None:
    """Report to the PR sender that a Slack channel wasn't created for it, and abort."""
    error = "Failed to create Slack channel for " + pr.html_url
    debug.log(error)

    user_id = users.github_username_to_slack_user_id(github_username)
    if user_id and not data_helper.slack_opted_out(user_id):
        slack.chat_postMessage(channel=user_id, text=error)

    raise RuntimeError(error)


def _set_topic(pr, channel_id: str) -> None:
    """Set the topic of a Slack channel to a GitHub PR URL."""
    topic = pr.html_url
    if len(topic) > _MAX_METADATA_LENGTH:
        topic = topic[: _MAX_METADATA_LENGTH - 4] + " ..."
    try:
        slack.conversations_setTopic(channel=channel_id, topic=topic)
    except SlackApiError as e:
        error = f"Failed to set the topic of <#{channel_id}> to `{topic}`"
        debug.log(error + f": `{e.response['error']}`")


def _set_description(pr, channel_id: str) -> None:
    """Set the description of a Slack channel to a GitHub PR title."""
    title = f"`{pr.title}`"
    if len(title) > _MAX_METADATA_LENGTH:
        title = title[: _MAX_METADATA_LENGTH - 4] + "`..."
    try:
        slack.conversations_setPurpose(channel=channel_id, purpose=title)
    except SlackApiError as e:
        error = f"Failed to set the purpose of <#{channel_id}> to `{title}`"
        debug.log(error + f": `{e.response['error']}`")


def _set_bookmarks(pr, channel_id: str) -> None:
    """Set the bookmarks of a Slack channel to important PR links.

    Bookmark titles are also updated later based on relevant GitHub events.

    Args:
        pr: GitHub PR data.
        channel_id: Slack channel ID.
    """
    pass  # TODO: Implement this function.


def _post_messages(action: str, pr, sender, channel_id: str) -> None:
    """Post initial messages to a Slack channel, describing a GitHub PR."""
    if action == "ready_for_review":
        action = "marked as ready for review"

    msg = f"{{}} {action} {pr.html_url}: `{pr.title}`"

    if pr.body:
        msg += "\n\n" + markdown.github_to_slack(pr.body, pr.html_url)

    slack_helper.mention_in_message(channel_id, sender, msg)

    # TODO: Also post a message summarizing check states (updated
    # later based on "workflow_job" and "workflow_run" events).
