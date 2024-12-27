from datetime import datetime
import unittest
from unittest.mock import MagicMock

import autokitteh

import slack_cmd


class SlackCmdTest(unittest.TestCase):
    """Unit tests for the "slack_cmd" module."""

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.data = {
            "channel_id": "purr-debug",
            "user_id": "user",
            "command": "/purrr",
        }

    def setUp(self):
        slack_cmd.slack = MagicMock()
        slack_cmd.data_helper = MagicMock()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_help_text(self):
        data = autokitteh.AttrDict(self.data)
        text = slack_cmd._help_text(data)

        for cmd in slack_cmd._COMMANDS.values():
            self.assertIn(cmd.label, text)
            self.assertIn(cmd.description, text)

    def test_on_slack_slash_command_without_text(self):
        event = autokitteh.AttrDict({"data": self.data | {"text": ""}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=slack_cmd._help_text(event.data),
        )

    def test_on_slack_slash_command_with_help(self):
        event = autokitteh.AttrDict({"data": self.data | {"text": "help"}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=slack_cmd._help_text(event.data),
        )

    def test_on_slack_slash_command_with_noop_opt_in(self):
        slack_cmd.data_helper.slack_opted_out.return_value = ""

        event = autokitteh.AttrDict({"data": self.data | {"text": "opt-in"}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.data_helper.slack_opted_out.assert_called_once_with(
            event.data.user_id
        )
        slack_cmd.data_helper.slack_opt_in.assert_not_called()
        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":bell: You're already opted into Purrr",
        )

    def test_on_slack_slash_command_with_actual_opt_in(self):
        slack_cmd.data_helper.slack_opted_out.return_value = datetime.min

        event = autokitteh.AttrDict({"data": self.data | {"text": "opt-in"}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.data_helper.slack_opted_out.assert_called_once_with(
            event.data.user_id
        )
        slack_cmd.data_helper.slack_opt_in.assert_called_once_with(event.data.user_id)
        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":bell: You are now opted into Purrr",
        )

    def test_on_slack_slash_command_with_noop_opt_out(self):
        slack_cmd.data_helper.slack_opted_out.return_value = datetime.min

        event = autokitteh.AttrDict({"data": self.data | {"text": "opt-out"}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.data_helper.slack_opted_out.assert_called_once_with(
            event.data.user_id
        )
        slack_cmd.data_helper.slack_opt_out.assert_not_called()
        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":no_bell: You're already opted out of Purrr since: 0001-01-01 00:00:00",
        )

    def test_on_slack_slash_command_with_second_opt_out(self):
        slack_cmd.data_helper.slack_opted_out.return_value = ""

        event = autokitteh.AttrDict({"data": self.data | {"text": "opt-out"}})
        slack_cmd.on_slack_slash_command(event)

        slack_cmd.data_helper.slack_opted_out.assert_called_once_with(
            event.data.user_id
        )
        slack_cmd.data_helper.slack_opt_out.assert_called_once_with(event.data.user_id)
        slack_cmd.slack.chat_postEphemeral.assert_called_once_with(
            channel=event.data.channel_id,
            user=event.data.user_id,
            text=":no_bell: You are now opted out of Purrr",
        )


if __name__ == "__main__":
    unittest.main()
