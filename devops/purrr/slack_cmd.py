"""Handler for Slack slash-command events."""

import collections

import data_helper
import slack_helper


slack = slack_helper.shared_client


def on_slack_slash_command(event):
    """Entry-point for AutoKitteh sessions triggered by Slack slash-command events.

    - /purrr help
    - /purrr opt-in
    - /purrr opt-out
    - /purrr list
    - /purrr status [PR]
    - /purrr approve [PR]

    About slash commands: https://api.slack.com/interactivity/slash-commands
    See also: https://api.slack.com/interactivity/handling#message_responses

    Args:
        event: Slack event data.
    """
    # Split the command into normalized arguments.
    data = event.data
    args = str(data.text).lower().split()

    # Route further processing to the appropriate command handler.
    if not args or "help" in args:
        _help(data, args)
        return

    if args[0] in _COMMANDS:
        _COMMANDS[args[0]].handler(data, args)
        return

    error = f"Error: unrecognized Purrr command: `{args[0]}`"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=error)


def _error(data, cmd: str, msg: str):
    """Send a private error message to the user about their command."""
    error = f"Error in `{data.command} {cmd}`: {msg}"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=error)


def _help(data, args: list[str]):
    """Send a private message to the user to list all the available Purrr commands."""
    if len(args) > 2:
        # TODO: Support per-command help too, in the future.
        _error(data, "help", "this command doesn't accept extra arguments")
        return

    # General help message: a list of all the available commands.
    text = _help_text(data)
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=text)


def _help_text(data) -> str:
    text = ":wave: *GitHub Pull Request Review Reminder (Purrr)* :wave:\n\n"
    text += "Available slash commands:"
    for cmd in _COMMANDS.values():
        text += f"\n  •  `{data.command} {cmd.label}` - {cmd.description}"
    return text


def _opt_in(data, args: list[str]):
    """User opt-in command handler (this is the default user state)."""
    if len(args) > 1:
        _error(data, args[0], "this command doesn't accept extra arguments")
        return

    if not data_helper.slack_opted_out(data.user_id):
        msg = ":bell: You're already opted into Purrr"
        slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=msg)
        return

    data_helper.slack_opt_in(data.user_id)
    msg = ":bell: You are now opted into Purrr"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=msg)


def _opt_out(data, args: list[str]):
    """User opt-out: don't use Purrr even in a Slack workspace that installed it."""
    if len(args) > 1:
        _error(data, args[0], "this command doesn't accept extra arguments")
        return

    opt_out_time = data_helper.slack_opted_out(data.user_id)
    if opt_out_time:
        msg = f":no_bell: You're already opted out of Purrr since: {opt_out_time}"
        slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=msg)
        return

    data_helper.slack_opt_out(data.user_id)
    msg = ":no_bell: You are now opted out of Purrr"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=msg)


def _list(data, args: list[str]):
    """PR list command handler."""
    if len(args) > 1:
        _error(data, args[0], "this command doesn't accept extra arguments")
        return

    error = "Sorry, this command is not implemented yet"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=error)


def _status(data, args: list[str]):
    """PR status command handler."""
    # TODO: If the Slack channel belongs to a PR, the arg is optional.
    if len(args) != 2:
        msg = "when called outside of a PR channel, this command requires exactly "
        msg += "1 argument - an ID of a GitHub PR (`<org>/<repo>/<number>`), "
        _error(data, args[0], msg + "or the PR's full URL")
        return

    error = "Sorry, this command is not implemented yet"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=error)


def _approve(data, args: list[str]):
    """Approve command."""
    # TODO: If the Slack channel belongs to a PR, the arg is optional.
    if len(args) != 2:
        msg = "when called outside of a PR channel, this command requires exactly "
        msg += "1 argument - an ID of a GitHub PR (`<org>/<repo>/<number>`), "
        _error(data, args[0], msg + "or the PR's full URL")
        return

    error = "Sorry, this command is not implemented yet"
    slack.chat_postEphemeral(channel=data.channel_id, user=data.user_id, text=error)


_Command = collections.namedtuple("Command", ["label", "handler", "description"])

_COMMANDS = {
    "opt-in": _Command("opt-in", _opt_in, "Opt into receiving notifications"),
    "opt-out": _Command("opt-out", _opt_out, "Opt out of receiving notifications"),
    "list": _Command("list", _list, "List all PRs you should pay attention to"),
    "status": _Command("status [PR]", _status, "Check the status of a specific PR"),
    "approve": _Command("approve [PR]", _approve, "Approve a specific PR"),
}
