"""Unit tests for the "slack_cmd" module."""

from datetime import datetime, UTC

import autokitteh
from autokitteh import github, slack
import pytest


MIN_UTC = datetime.min.replace(tzinfo=UTC)


@pytest.fixture(autouse=True)
def setup_mock_github_and_slack_clients(mocker):
    mocker.patch.object(github, "github_client", autospec=True)
    mocker.patch.object(slack, "slack_client", autospec=True)


@pytest.fixture
def mock_data_helper(mocker):
    import slack_cmd

    return mocker.patch.object(slack_cmd, "data_helper", autospec=True)


fake_data = {
    "channel_id": "purr-debug",
    "user_id": "user",
    "command": "/purrr",
}


def test_help_text():
    import slack_cmd

    data = autokitteh.AttrDict(fake_data)
    text = slack_cmd._help_text(data)

    for cmd in slack_cmd._COMMANDS.values():
        assert cmd.label in text
        assert cmd.description in text


def test_on_slack_slash_command_without_text():
    import slack_cmd

    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": ""}})
    slack_cmd.on_slack_slash_command(event)

    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=slack_cmd._help_text(event.data),
    )


def test_on_slack_slash_command_with_help():
    import slack_cmd

    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": "help"}})
    slack_cmd.on_slack_slash_command(event)

    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=slack_cmd._help_text(event.data),
    )


def test_on_slack_slash_command_with_noop_opt_in(mock_data_helper):
    import slack_cmd

    mock_data_helper.slack_opted_out.return_value = ""
    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-in"}})
    slack_cmd.on_slack_slash_command(event)

    mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
    mock_data_helper.slack_opt_in.assert_not_called()
    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=":bell: You're already opted into Purrr",
    )


def test_on_slack_slash_command_with_actual_opt_in(mock_data_helper):
    import slack_cmd

    mock_data_helper.slack_opted_out.return_value = MIN_UTC
    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-in"}})
    slack_cmd.on_slack_slash_command(event)

    mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
    mock_data_helper.slack_opt_in.assert_called_once_with(event.data.user_id)
    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=":bell: You are now opted into Purrr",
    )


def test_on_slack_slash_command_with_noop_opt_out(mock_data_helper):
    import slack_cmd

    mock_data_helper.slack_opted_out.return_value = MIN_UTC
    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-out"}})
    slack_cmd.on_slack_slash_command(event)

    mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
    mock_data_helper.slack_opt_out.assert_not_called()
    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=":no_bell: You're already opted out of Purrr since: "
        "0001-01-01 00:00:00+00:00",
    )


def test_on_slack_slash_command_with_second_opt_out(mock_data_helper):
    import slack_cmd

    mock_data_helper.slack_opted_out.return_value = ""
    slack_cmd.slack.chat_postEphemeral.reset_mock()

    event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-out"}})
    slack_cmd.on_slack_slash_command(event)

    mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
    mock_data_helper.slack_opt_out.assert_called_once_with(event.data.user_id)
    slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
        channel=event.data.channel_id,
        user=event.data.user_id,
        text=":no_bell: You are now opted out of Purrr",
    )
