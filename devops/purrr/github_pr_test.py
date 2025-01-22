"""Unit tests for the "github_pr" module."""

import collections

from autokitteh import github, slack
import pytest


@pytest.fixture(autouse=True)
def setup_mock_github_and_slack_clients(mocker):
    mocker.patch.object(github, "github_client", autospec=True)
    mocker.patch.object(slack, "slack_client", autospec=True)


@pytest.fixture
def mock_slack_user_id(mocker):
    import users

    return mocker.patch.object(users, "github_username_to_slack_user_id", autospec=True)


FakeGithubUser = collections.namedtuple("FakeGithubUser", ["login"])


class TestOnPRReviewRequestedPerson:
    """Unit tests for the "_on_pr_review_requested_person" function."""

    def test_reviewer(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = [
            "reviewer",  # _on_pr_review_requested_person: message to channel
            "sender",  # mention_in_reply: mention in message to channel
            "reviewer",  # add_users: invite reviewer to channel
            "sender",  # mention_in_reply: mention in DM to reviewer
        ]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_requested_person(
            FakeGithubUser("reviewer"), FakeGithubUser("sender"), "C987", "reviewer"
        )

        slack_helper.shared_client.chat_postMessage.assert_any_call(
            channel="C987",
            text="<@sender> added <@reviewer> as a reviewer",
            thread_ts=None,
        )
        slack_helper.shared_client.chat_postMessage.assert_called_with(
            channel="reviewer",
            text="<@sender> added you as a reviewer to a PR: <#C987>",
            thread_ts=None,
        )

    def test_self_reviewer(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = ["U123", "U123", "U123"]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_requested_person(
            FakeGithubUser("sender"), FakeGithubUser("sender"), "C987", "reviewer"
        )

        slack_helper.shared_client.chat_postMessage.assert_called_with(
            channel="C987",
            text="<@U123> added themselves as a reviewer",
            thread_ts=None,
        )

    def test_assignee(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = [
            "assignee",  # _on_pr_review_requested_person: message to channel
            "sender",  # mention_in_reply: mention in message to channel
            "assignee",  # add_users: invite reviewer to channel
            "sender",  # mention_in_reply: mention in DM to reviewer
        ]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_requested_person(
            FakeGithubUser("assignee"), FakeGithubUser("sender"), "C987", "assignee"
        )

        slack_helper.shared_client.chat_postMessage.assert_any_call(
            channel="C987",
            text="<@sender> added <@assignee> as an assignee",
            thread_ts=None,
        )
        slack_helper.shared_client.chat_postMessage.assert_called_with(
            channel="assignee",
            text="<@sender> added you as an assignee to a PR: <#C987>",
            thread_ts=None,
        )

    def test_self_assignee(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = ["U123", "U123", "U123"]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_requested_person(
            FakeGithubUser("sender"), FakeGithubUser("sender"), "C987", "assignee"
        )

        slack_helper.shared_client.chat_postMessage.assert_called_once_with(
            channel="C987",
            text="<@U123> added themselves as an assignee",
            thread_ts=None,
        )


class TestOnPRReviewRequestRemovedPerson:
    """Unit tests for the "_on_pr_review_request_removed_person" function."""

    def test_reviewer(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = [
            "reviewer",  # _on_pr_review_requested_person: message to channel
            "sender",  # mention_in_reply: mention in message to channel
        ]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_request_removed_person(
            FakeGithubUser("reviewer"), FakeGithubUser("sender"), "C987", "reviewer"
        )

        slack_helper.shared_client.chat_postMessage.assert_any_call(
            channel="C987",
            text="<@sender> removed <@reviewer> as a reviewer",
            thread_ts=None,
        )

    def test_self_reviewer(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = ["U123", "U123"]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_request_removed_person(
            FakeGithubUser("sender"), FakeGithubUser("sender"), "C987", "reviewer"
        )

        slack_helper.shared_client.chat_postMessage.assert_called_with(
            channel="C987",
            text="<@U123> removed themselves as a reviewer",
            thread_ts=None,
        )

    def test_assignee(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = [
            "assignee",  # _on_pr_review_requested_person: message to channel
            "sender",  # mention_in_reply: mention in message to channel
        ]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_request_removed_person(
            FakeGithubUser("assignee"), FakeGithubUser("sender"), "C987", "assignee"
        )

        slack_helper.shared_client.chat_postMessage.assert_any_call(
            channel="C987",
            text="<@sender> removed <@assignee> as an assignee",
            thread_ts=None,
        )

    def test_self_assignee(self, mock_slack_user_id):
        import github_pr
        import slack_helper

        mock_slack_user_id.side_effect = ["U123", "U123"]
        slack_helper.shared_client.chat_postMessage.reset_mock()

        github_pr._on_pr_review_request_removed_person(
            FakeGithubUser("sender"), FakeGithubUser("sender"), "C987", "assignee"
        )

        slack_helper.shared_client.chat_postMessage.assert_called_once_with(
            channel="C987",
            text="<@U123> removed themselves as an assignee",
            thread_ts=None,
        )
