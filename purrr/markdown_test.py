"""Unit tests for the "markdown" module."""

import collections
import unittest
from unittest import mock

import markdown
import users


class MarkdownGithubToSlackTest(unittest.TestCase):
    """Unit tests for the "github_to_slack" function."""

    def test_trivial(self):
        self.assertEqual(markdown.github_to_slack("", ""), "")

    def test_headers(self):
        self.assertEqual(
            markdown.github_to_slack("# Title 1\n\nFoo\n\n## Subtitle 2\nBar", ""),
            "*Title 1*\n\nFoo\n\n*Subtitle 2*\nBar",
        )

    def test_text_style(self):
        self.assertEqual(markdown.github_to_slack("_italic_", ""), "_italic_")
        self.assertEqual(markdown.github_to_slack("*italic*", ""), "_italic_")
        self.assertEqual(markdown.github_to_slack("__bold__", ""), "*bold*")
        self.assertEqual(markdown.github_to_slack("**bold**", ""), "*bold*")
        self.assertEqual(markdown.github_to_slack("***both***", ""), "_*both*_")
        self.assertEqual(
            markdown.github_to_slack("**this _is_ nested**", ""), "*this _is_ nested*"
        )
        self.assertEqual(
            markdown.github_to_slack("**this *is* nested**", ""), "*this _is_ nested*"
        )
        self.assertEqual(
            markdown.github_to_slack("__this _is_ nested__", ""), "*this _is_ nested*"
        )
        self.assertEqual(
            markdown.github_to_slack("_this **is** nested_", ""), "_this *is* nested_"
        )
        # TODO: self.assertEqual(
        #     markdown.github_to_slack("*this **is** nested*", ""), "_this *is* nested_"
        # )
        self.assertEqual(
            markdown.github_to_slack("~~strikethrough~~", ""), "~strikethrough~"
        )

    def test_text_blocks(self):
        # Quotes.
        self.assertEqual(
            markdown.github_to_slack("111\n>222\n> 333\n444", ""),
            "111\n>222\n> 333\n444",
        )
        # Code.
        self.assertEqual(markdown.github_to_slack("`inline`", ""), "`inline`")
        self.assertEqual(
            markdown.github_to_slack("```\nmulti\nline\n```", ""),
            "```\nmulti\nline\n```",
        )

    def test_links(self):
        self.assertEqual(markdown.github_to_slack("[text](url)", ""), "<url|text>")
        self.assertEqual(
            markdown.github_to_slack("!<url maybe with text>", ""),
            "Image: <url maybe with text>",
        )

    def test_simple_lists(self):
        self.assertEqual(
            markdown.github_to_slack("- 111\n- 222\n- 333", ""),
            "  •  111\n  •  222\n  •  333",
        )
        # TODO: self.assertEqual(
        #     markdown.github_to_slack("* 111\n* 222\n* 333", ""),
        #     "  •  111\n  •  222\n  •  333",
        # )
        self.assertEqual(
            markdown.github_to_slack("+ 111\n+ 222\n+ 333", ""),
            "  •  111\n  •  222\n  •  333",
        )

    def test_nested_lists(self):
        self.assertEqual(
            markdown.github_to_slack("- 111\n  - 222\n  - 333\n- 444", ""),
            "  •  111\n          ◦   222\n          ◦   333\n  •  444",
        )
        # TODO: self.assertEqual(
        #     markdown.github_to_slack("* 111\n  * 222\n  * 333\n* 444", ""),
        #     "  •  111\n          ◦   222\n          ◦   333\n  •  444",
        # )
        self.assertEqual(
            markdown.github_to_slack("+ 111\n  + 222\n  + 333\n+ 444", ""),
            "  •  111\n          ◦   222\n          ◦   333\n  •  444",
        )

    @mock.patch.object(users, "github_username_to_slack_user_id", autospec=True)
    def test_user_mentions(self, mock_func):
        mock_func.side_effect = ["U123", None, None]

        # Slack user found.
        self.assertEqual(
            markdown.github_to_slack("@user", "https://github.com/org/repo/pull/123"),
            "<@U123>",
        )
        # Slack user not found.
        self.assertEqual(
            markdown.github_to_slack("@user", "https://github.com/org/repo/pull/123"),
            "<https://github.com/user|@user>",
        )
        # Team not found.
        self.assertEqual(
            markdown.github_to_slack(
                "@org/team", "https://github.com/org/repo/pull/123"
            ),
            "<https://github.com/org/teams/team|@org/team>",
        )

    def test_pr_references(self):
        self.assertEqual(
            markdown.github_to_slack("#123", "https://github.com/org/repo/pull/987"),
            "<https://github.com/org/repo/pull/123|#123>",
        )

    def test_html_comments(self):
        self.assertEqual(
            markdown.github_to_slack("Blah\n<!-- hidden -->\nBlah blah", ""),
            "Blah\n\nBlah blah",
        )


class MarkdownSlackToGithubTest(unittest.TestCase):
    """Unit tests for the "slack_to_github" function."""

    def test_trivial(self):
        self.assertEqual(markdown.slack_to_github(""), "")

    def test_text_style(self):
        self.assertEqual(markdown.slack_to_github("_italic_"), "_italic_")
        self.assertEqual(markdown.slack_to_github("*bold*"), "**bold**")
        self.assertEqual(markdown.slack_to_github("_*both*_"), "***both***")
        self.assertEqual(
            markdown.slack_to_github("~strikethrough~"), "~~strikethrough~~"
        )

        # Not needed, but good to have just in case someone
        # sends a non-Slack-markdown message programmatically:
        self.assertEqual(markdown.slack_to_github("__italic__"), "_italic_")
        self.assertEqual(markdown.slack_to_github("**bold**"), "**bold**")
        self.assertEqual(markdown.slack_to_github("*_both_*"), "***both***")
        self.assertEqual(markdown.slack_to_github("***both***"), "***both***")
        self.assertEqual(
            markdown.slack_to_github("~~strikethrough~~"), "~~strikethrough~~"
        )

    def test_text_blocks(self):
        # Quotes.
        self.assertEqual(
            markdown.slack_to_github("111\n&gt;222\n&gt; 333\n444"),
            "111\n>222\n> 333\n444",
        )
        self.assertEqual(
            markdown.slack_to_github("111\n>222\n> 333\n444"),
            "111\n>222\n> 333\n444",
        )
        # Code.
        self.assertEqual(markdown.slack_to_github("`inline`"), "`inline`")
        self.assertEqual(
            markdown.slack_to_github("```multi\nline```"), "```\nmulti\nline\n```"
        )

    def test_lists(self):
        self.assertEqual(markdown.slack_to_github("• X\n• Y\n• Z"), "- X\n- Y\n- Z")
        self.assertEqual(
            markdown.slack_to_github(
                "• X\n    ◦ Y\n        ▪︎ Z\n            • A\n                ◦ B"
            ),
            "- X\n  - Y\n    - Z\n      - A\n        - B",
        )

    def test_links(self):
        self.assertEqual(markdown.slack_to_github("<url|text>"), "[text](url)")
        self.assertEqual(markdown.slack_to_github("<url|>"), "[](url)")
        self.assertEqual(markdown.slack_to_github("<url>"), "<url>")

    @mock.patch.object(markdown, "_slack_team_id", autospec=True)
    @mock.patch.object(markdown, "_slack_channel_name", autospec=True)
    def test_channel(self, mock_channel_name, mock_team_id):
        mock_channel_name.return_value = "channel"
        mock_team_id.return_value = "TEAM_ID"

        self.assertEqual(
            markdown.slack_to_github("<#C123>"),
            "[#channel](slack://channel?team=TEAM_ID&id=C123)",
        )
        self.assertEqual(
            markdown.slack_to_github("<#C123|>"),
            "[#channel](slack://channel?team=TEAM_ID&id=C123)",
        )
        self.assertEqual(
            markdown.slack_to_github("<#C123|custom-name>"),
            "[#custom-name](slack://channel?team=TEAM_ID&id=C123)",
        )


FakeGithubUser = collections.namedtuple("FakeGithubUser", ["name", "login"])


@mock.patch.object(users, "_slack_user_info", autospec=True)
@mock.patch.object(users, "_github_users", autospec=True)
@mock.patch.object(users, "_email_to_github_user_id", autospec=True)
class MarkdownSlackToGithubUserMentionsTest(unittest.TestCase):
    """Unit tests for user mentions in the "slack_to_github" function."""

    def test_slack_user_info_error(self, mock_email, mock_github, mock_slack):
        mock_slack.return_value = {}
        self.assertEqual(markdown.slack_to_github("<@U123>"), "Someone")

    def test_email_and_name_not_found_in_slack_profile(
        self, mock_email, mock_github, mock_slack
    ):
        mock_slack.return_value = {"profile": {"foo": "bar"}}
        self.assertEqual(markdown.slack_to_github("<@U123>"), "Someone")

    def test_named_and_unnamed_slack_apps(self, mock_email, mock_github, mock_slack):
        mock_slack.side_effect = [
            {"is_bot": True, "profile": {"real_name": "Mr. Robot"}},
            {"is_bot": True},
        ]
        self.assertEqual(markdown.slack_to_github("<@U123>"), "Mr. Robot")
        self.assertEqual(markdown.slack_to_github("<@U123>"), "Some Slack app")

    def test_match_by_email(self, mock_email, mock_github, mock_slack):
        mock_slack.return_value = {"profile": {"email": "me@test.com"}}
        mock_email.return_value = "username"
        self.assertEqual(markdown.slack_to_github("<@U123>"), "@username")

    def test_match_by_name(self, mock_email, mock_github, mock_slack):
        mock_slack.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        mock_email.return_value = ""
        mock_github.return_value = [FakeGithubUser("John Doe", "username")]
        self.assertEqual(markdown.slack_to_github("<@U123>"), "@username")

    def test_no_matches_by_name(self, mock_email, mock_github, mock_slack):
        mock_slack.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        mock_email.return_value = ""
        mock_github.return_value = []
        self.assertEqual(markdown.slack_to_github("<@U123>"), "John Doe")

    def test_too_many_matches_by_name(self, mock_email, mock_github, mock_slack):
        mock_slack.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        mock_email.return_value = ""
        mock_github.return_value = [
            FakeGithubUser("John Doe", "username1"),
            FakeGithubUser("john doe", "username2"),
            FakeGithubUser("JOHN DOE", "username3"),
        ]
        self.assertEqual(markdown.slack_to_github("<@U123>"), "John Doe")


if __name__ == "__main__":
    unittest.main()
