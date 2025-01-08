"""Unit tests for the "slack_cmd" module."""

from datetime import datetime
import unittest
from unittest import mock

import autokitteh
from slack_sdk.web.client import WebClient

import slack_cmd


fake_data = {
    "channel_id": "purr-debug",
    "user_id": "user",
    "command": "/purrr",
}


@mock.patch.object(slack_cmd, "slack", spec=WebClient)
@mock.patch.object(slack_cmd, "data_helper", autospec=True)
class SlackCmdTest(unittest.TestCase):
    """Unit tests for the "slack_cmd" module."""

    def test_help_text(self, *_):
        data = autokitteh.AttrDict(fake_data)
        text = slack_cmd._help_text(data)

        for cmd in slack_cmd._COMMANDS.values():
            self.assertIn(cmd.label, text)
            self.assertIn(cmd.description, text)

    def test_on_slack_slash_command_without_text(self, _, mock_slack):
        event = autokitteh.AttrDict({"data": fake_data | {"text": ""}})
        slack_cmd.on_slack_slash_command(event)

        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=slack_cmd._help_text(event.data),
        )

    def test_on_slack_slash_command_with_help(self, _, mock_slack):
        event = autokitteh.AttrDict({"data": fake_data | {"text": "help"}})
        slack_cmd.on_slack_slash_command(event)

        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=slack_cmd._help_text(event.data),
        )

    def test_on_slack_slash_command_with_noop_opt_in(
        self, mock_data_helper, mock_slack
    ):
        mock_data_helper.slack_opted_out.return_value = ""

        event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-in"}})
        slack_cmd.on_slack_slash_command(event)

        mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
        mock_data_helper.slack_opt_in.assert_not_called()
        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":bell: You're already opted into Purrr",
        )

    def test_on_slack_slash_command_with_actual_opt_in(
        self, mock_data_helper, mock_slack
    ):
        mock_data_helper.slack_opted_out.return_value = datetime.min

        event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-in"}})
        slack_cmd.on_slack_slash_command(event)

        mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
        mock_data_helper.slack_opt_in.assert_called_once_with(event.data.user_id)
        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":bell: You are now opted into Purrr",
        )

    def test_on_slack_slash_command_with_noop_opt_out(
        self, mock_data_helper, mock_slack
    ):
        mock_data_helper.slack_opted_out.return_value = datetime.min

        event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-out"}})
        slack_cmd.on_slack_slash_command(event)

        mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
        mock_data_helper.slack_opt_out.assert_not_called()
        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=(
                ":no_bell: You're already opted out of Purrr since: 0001-01-01 00:00:00"
            ),
        )

    def test_on_slack_slash_command_with_second_opt_out(
        self, mock_data_helper, mock_slack
    ):
        mock_data_helper.slack_opted_out.return_value = ""

        event = autokitteh.AttrDict({"data": fake_data | {"text": "opt-out"}})
        slack_cmd.on_slack_slash_command(event)

        mock_data_helper.slack_opted_out.assert_called_once_with(event.data.user_id)
        mock_data_helper.slack_opt_out.assert_called_once_with(event.data.user_id)
        mock_slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":no_bell: You are now opted out of Purrr",
        )


if __name__ == "__main__":
    unittest.main()
