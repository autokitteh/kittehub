"""Create and manage Slack channels."""

import json
import time

from autokitteh.slack import normalize_channel_name
from slack_sdk.errors import SlackApiError

import data_helper
import debug
import slack_helper
import text_utils
import users


# Character limit for topics and descriptions of Slack channels.
_MAX_METADATA_LENGTH = 250

# Wait for a few seconds to handle other asynchronous events
# (e.g. a PR closure comment) before archiving the channel.
_PR_CLOSE_DELAY = 5


slack = slack_helper.shared_client


def initialize_for_github_pr(action: str, pr, sender) -> str:
    """Initialize a Slack channel that represents a GitHub PR.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user object of the PR sender.

    Returns:
        ID of the created Slack channel.
    """
    print(f"Creating Slack channel for {pr.html_url} (PR event action: {action})")
    print(json.dumps(pr, indent=4, sort_keys=True))

    name = f"{pr.number}_{normalize_channel_name(pr.title)}"
    channel_id = slack_helper.create_channel(name)
    if not channel_id:
        _report_creation_error(pr, sender.login)

    _set_topic(pr, channel_id)
    _set_description(pr, channel_id)
    _set_bookmarks(pr, channel_id)
    _post_messages(action, pr, sender, channel_id)

    # TODO: Map between the GitHub PR and the Slack channel ID, for 2-way event syncs.

    add_users(channel_id, users.github_pr_participants(pr))
    return channel_id


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
        debug.log(f"{error}: `{e.response['error']}`")


def _set_description(pr, channel_id: str) -> None:
    """Set the description of a Slack channel to a GitHub PR title."""
    title = f"`{pr.title}`"
    if len(title) > _MAX_METADATA_LENGTH:
        title = title[: _MAX_METADATA_LENGTH - 4] + "`..."
    try:
        slack.conversations_setPurpose(channel=channel_id, purpose=title)
    except SlackApiError as e:
        error = f"Failed to set the purpose of <#{channel_id}> to `{title}`"
        debug.log(f"{error}: `{e.response['error']}`")


def _set_bookmarks(pr, channel_id: str) -> None:
    """Set the bookmarks of a Slack channel to important GitHub PR links.

    Bookmark titles are also updated later based on relevant GitHub events.
    """
    pass  # TODO: Implement this function.


def _post_messages(action: str, pr, sender, channel_id: str) -> None:
    """Post initial messages to a Slack channel, describing a GitHub PR."""
    if action == "ready_for_review":
        action = "marked as ready for review"

    msg = f"{{}} {action} {pr.html_url}: `{pr.title}`"

    if pr.body:
        msg += "\n\n" + text_utils.github_to_slack(pr.body, pr.html_url)

    slack_helper.mention_in_message(channel_id, sender, msg)

    # TODO: Also post a message summarizing check states (updated
    # later based on "workflow_job" and "workflow_run" events).


def add_users(channel_id: str, github_users: list[str]) -> None:
    """Invite all the participants in a GitHub PR to a Slack channel."""
    slack_users = [users.github_username_to_slack_user_id(u) for u in github_users]
    slack_users = [user for user in slack_users if user]  # Ignore unrecognized users.

    # Also ignore users who opted out of Purrr. They will still be mentioned
    # in the channel, but as non-members they won't be notified about it.
    slack_users = [u for u in slack_users if not data_helper.slack_opted_out(u)]
    if not slack_users:
        return

    # Limit the number of users per https://api.slack.com/methods/conversations.invite
    if len(slack_users) > 1000:
        slack_users = slack_users[:1000]

    user_ids = ",".join(slack_users)
    try:
        slack.conversations_invite(channel=channel_id, users=user_ids, force=True)
    except SlackApiError as e:
        if e.response["error"] == "already_in_channel":
            return

        error = f"Failed to add {len(slack_users)} Slack user(s) to channel "
        error += f"<#{channel_id}>: `{e.response['error']}`"
        for err in e.response.get("errors", []):
            error += f"\n- <@{err.user}> - `{err.error}`"
        debug.log(error)


def archive(action: str, pr, sender) -> None:
    """Archive a Slack channel that represents a GitHub PR.

    This function is called when a PR is closed or converted to a draft.

    Args:
        action: GitHub PR event action.
        pr: GitHub PR data.
        sender: GitHub user who triggered the event.
    """
    channel_id = slack_helper.lookup_channel(pr.html_url, action)
    if not channel_id:
        # Unrecoverable error, but no need to report/debug it:
        # if we're not tracking it, there's nothing to fix.
        return

    # Wait for a few seconds to handle other asynchronous events
    # (e.g. a PR closure comment) before archiving the channel.
    time.sleep(_PR_CLOSE_DELAY)

    if action == "closed this PR":
        if pr.merged:
            action = "merged this PR"
    else:
        action = "converted this PR to a draft"

    slack_helper.mention_in_message(channel_id, sender, f"{{}} {action}")

    try:
        slack.conversations_archive(channel=channel_id)
    except SlackApiError as e:
        action = action.replace(" this PR", "")
        error = f"{pr.html_url} is `{action}`, but failed to archive <#{channel_id}>"
        debug.log(f"{error}: `{e.response['error']}`")
