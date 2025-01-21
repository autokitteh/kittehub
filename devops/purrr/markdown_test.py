"""Unit tests for the "markdown" module."""

import collections

from autokitteh import github, slack
import pytest


@pytest.fixture(autouse=True)
def setup_mock_github_and_slack_clients(mocker):
    mocker.patch.object(github, "github_client", autospec=True)
    mocker.patch.object(slack, "slack_client", autospec=True)


class TestGithubToSlack:
    """Unit tests for the "github_to_slack" function."""

    def test_trivial(self):
        import markdown

        assert markdown.github_to_slack("", "") == ""

    def test_basic_headers(self):
        import markdown

        assert markdown.github_to_slack("# H1", "") == "*H1*"
        assert markdown.github_to_slack("## H2", "") == "*H2*"
        assert markdown.github_to_slack("### H3", "") == "*H3*"

    def test_multiple_headers(self):
        import markdown

        actual = markdown.github_to_slack("# Title 1\n\nFoo\n\n## Subtitle 2\nBar", "")
        assert actual == "*Title 1*\n\nFoo\n\n*Subtitle 2*\nBar"

    def test_basic_text_style(self):
        import markdown

        assert markdown.github_to_slack("_italic_", "") == "_italic_"
        assert markdown.github_to_slack("*italic*", "") == "_italic_"
        assert markdown.github_to_slack("__bold__", "") == "*bold*"
        assert markdown.github_to_slack("**bold**", "") == "*bold*"
        assert markdown.github_to_slack("~~strikethrough~~", "") == "~strikethrough~"

    def test_advanced_text_style(self):
        import markdown

        assert markdown.github_to_slack("***both***", "") == "_*both*_"
        actual = markdown.github_to_slack("**this _is_ nested**", "")
        assert actual == "*this _is_ nested*"
        actual = markdown.github_to_slack("**this *is* nested**", "")
        assert actual == "*this _is_ nested*"
        actual = markdown.github_to_slack("__this _is_ nested__", "")
        assert actual == "*this _is_ nested*"
        actual = markdown.github_to_slack("_this **is** nested_", "")
        assert actual == "_this *is* nested_"
        # TODO:
        # actual = markdown.github_to_slack("*this **is** nested*", "")
        # assert actual == "_this *is* nested_"

    def test_quote_blocks(self):
        import markdown

        actual = markdown.github_to_slack("111\n>222\n> 333\n444", "")
        assert actual == "111\n>222\n> 333\n444"

    def test_code_blocks(self):
        import markdown

        assert markdown.github_to_slack("`inline`", "") == "`inline`"
        actual = markdown.github_to_slack("```\nmulti\nline\n```", "")
        assert actual == "```\nmulti\nline\n```"

    def test_links(self):
        import markdown

        assert markdown.github_to_slack("[text](url)", "") == "<url|text>"
        actual = markdown.github_to_slack("!<url maybe with text>", "")
        assert actual == "Image: <url maybe with text>"

    def test_simple_lists(self):
        import markdown

        expected = "  •  111\n  •  222\n  •  333"
        assert markdown.github_to_slack("- 111\n- 222\n- 333", "") == expected
        assert markdown.github_to_slack("+ 111\n+ 222\n+ 333", "") == expected
        # TODO: assert markdown.github_to_slack("* 111\n* 222\n* 333", "") == expected

    def test_nested_lists(self):
        import markdown

        expect = "  •  111\n          ◦   222\n          ◦   333\n  •  444"
        assert markdown.github_to_slack("- 111\n  - 222\n  - 333\n- 444", "") == expect
        assert markdown.github_to_slack("+ 111\n  + 222\n  + 333\n+ 444", "") == expect
        # TODO:
        # assert markdown.github_to_slack("* 111\n  * 222\n  * 333\n* 444", "") == expec

    def test_user_mentions(self, mocker):
        import markdown
        import users

        pr = "https://github.com/org/repo/pull/123"
        id = mocker.patch.object(
            users, "github_username_to_slack_user_id", autospec=True
        )
        id.side_effect = ["U123", None, None]

        # Slack user found.
        assert markdown.github_to_slack("@user", pr) == "<@U123>"
        # Slack user not found.
        actual = markdown.github_to_slack("@user", pr)
        assert actual == "<https://github.com/user|@user>"
        # Team not found.
        actual = markdown.github_to_slack("@org/team", pr)
        assert actual == "<https://github.com/org/teams/team|@org/team>"

    def test_pr_references(self):
        import markdown

        pr = "https://github.com/org/repo/pull/987"
        actual = markdown.github_to_slack("#123", pr)
        assert actual == "<https://github.com/org/repo/pull/123|#123>"

    def test_html_comments(self):
        import markdown

        actual = markdown.github_to_slack("Blah\n<!-- hidden -->\nBlah blah", "")
        assert actual == "Blah\n\nBlah blah"


class TestSlackToGithub:
    """Unit tests for the "slack_to_github" function."""

    def test_trivial(self):
        import markdown

        assert markdown.slack_to_github("") == ""

    def test_text_style(self):
        import markdown

        assert markdown.slack_to_github("_italic_") == "_italic_"
        assert markdown.slack_to_github("*bold*") == "**bold**"
        assert markdown.slack_to_github("_*both*_") == "***both***"
        assert markdown.slack_to_github("~strikethrough~") == "~~strikethrough~~"

        # Not needed, but good to have just in case someone
        # sends a non-Slack-markdown message programmatically:
        assert markdown.slack_to_github("__italic__") == "_italic_"
        assert markdown.slack_to_github("**bold**") == "**bold**"
        assert markdown.slack_to_github("*_both_*") == "***both***"
        assert markdown.slack_to_github("***both***") == "***both***"
        assert markdown.slack_to_github("~~strikethrough~~") == "~~strikethrough~~"

    def test_quote_blocks(self):
        import markdown

        actual = markdown.slack_to_github("111\n&gt;222\n&gt; 333\n444")
        assert actual == "111\n>222\n> 333\n444"
        actual = markdown.slack_to_github("111\n>222\n> 333\n444")
        assert actual == "111\n>222\n> 333\n444"

    def test_code_blocks(self):
        import markdown

        assert markdown.slack_to_github("`inline`") == "`inline`"
        assert markdown.slack_to_github("```multi\nline```") == "```\nmulti\nline\n```"

    def test_lists(self):
        import markdown

        assert markdown.slack_to_github("• X\n• Y\n• Z") == "- X\n- Y\n- Z"
        actual = markdown.slack_to_github(
            "• X\n    ◦ Y\n        ▪︎ Z\n            • A\n                ◦ B"
        )
        assert actual == "- X\n  - Y\n    - Z\n      - A\n        - B"

    def test_links(self):
        import markdown

        assert markdown.slack_to_github("<url|text>") == "[text](url)"
        assert markdown.slack_to_github("<url|>"), "[](url)"
        assert markdown.slack_to_github("<url>"), "<url>"

    def test_channel(self, mocker):
        import markdown

        channel = mocker.patch.object(markdown, "_slack_channel_name", autospec=True)
        channel.return_value = "CHANNEL_NAME"
        team = mocker.patch.object(markdown, "_slack_team_id", autospec=True)
        team.return_value = "TEAM_ID"

        expected = "[#CHANNEL_NAME](slack://channel?team=TEAM_ID&id=C123)"
        assert markdown.slack_to_github("<#C123>") == expected
        assert markdown.slack_to_github("<#C123|>") == expected

        actual = markdown.slack_to_github("<#C123|custom-name>")
        assert actual == "[#custom-name](slack://channel?team=TEAM_ID&id=C123)"


FakeGithubUser = collections.namedtuple("FakeGithubUser", ["name", "login"])


class TestSlackToGithubUserMentions:
    """Unit tests for user mentions in the "slack_to_github" function."""

    @pytest.fixture
    def mock_github_user_id(self, mocker):
        import users

        return mocker.patch.object(users, "_email_to_github_user_id", autospec=True)

    @pytest.fixture
    def mock_github_users(self, mocker):
        import users

        return mocker.patch.object(users, "_github_users", autospec=True)

    @pytest.fixture
    def mock_slack_user_info(self, mocker):
        import users

        return mocker.patch.object(users, "_slack_user_info", autospec=True)

    def test_slack_user_info_error(self, mock_slack_user_info):
        import markdown

        mock_slack_user_info.return_value = {}
        assert markdown.slack_to_github("<@U123>") == "Someone"

    def test_email_and_name_not_found_in_slack_profile(self, mock_slack_user_info):
        import markdown

        mock_slack_user_info.return_value = {"profile": {"foo": "bar"}}
        assert markdown.slack_to_github("<@U123>") == "Someone"

    def test_named_and_unnamed_slack_apps(self, mock_slack_user_info):
        import markdown

        mock_slack_user_info.side_effect = [
            {"is_bot": True, "profile": {"real_name": "Mr. Robot"}},
            {"is_bot": True},
        ]
        assert markdown.slack_to_github("<@U123>") == "Mr. Robot"
        assert markdown.slack_to_github("<@U123>") == "Some Slack app"

    def test_match_by_email(self, mock_github_user_id, mock_slack_user_info):
        import markdown

        mock_github_user_id.return_value = "username"
        mock_slack_user_info.return_value = {"profile": {"email": "me@test.com"}}
        assert markdown.slack_to_github("<@U123>") == "@username"

    def test_match_by_name(
        self, mock_github_user_id, mock_github_users, mock_slack_user_info
    ):
        import markdown

        mock_github_user_id.return_value = ""
        mock_github_users.return_value = [FakeGithubUser("John Doe", "username")]
        mock_slack_user_info.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        assert markdown.slack_to_github("<@U123>") == "@username"

    def test_no_matches_by_name(
        self, mock_github_user_id, mock_github_users, mock_slack_user_info
    ):
        import markdown

        mock_github_user_id.return_value = ""
        mock_github_users.return_value = []
        mock_slack_user_info.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        assert markdown.slack_to_github("<@U123>") == "John Doe"

    def test_too_many_matches_by_name(
        self, mock_github_user_id, mock_github_users, mock_slack_user_info
    ):
        import markdown

        mock_github_user_id.return_value = ""
        mock_github_users.return_value = [
            FakeGithubUser("John Doe", "username1"),
            FakeGithubUser("john doe", "username2"),
            FakeGithubUser("JOHN DOE", "username3"),
        ]
        mock_slack_user_info.return_value = {
            "profile": {"email": "me@test.com", "real_name": "John Doe"}
        }
        assert markdown.slack_to_github("<@U123>") == "John Doe"