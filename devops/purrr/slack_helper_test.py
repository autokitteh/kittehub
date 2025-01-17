"""Unit tests for the "slack_helper" module."""

from autokitteh import github, slack


def test_normalize_channel_name(mocker):
    mocker.patch.object(github, "github_client", autospec=True)
    mocker.patch.object(slack, "slack_client", autospec=True)
    import slack_helper

    assert slack_helper.normalize_channel_name("") == ""
    assert slack_helper.normalize_channel_name('"isn\'t"') == "isnt"
    assert slack_helper.normalize_channel_name("TEST") == "test"
    assert slack_helper.normalize_channel_name("1  2--3__4") == "1-2-3-4"
    assert slack_helper.normalize_channel_name("a `~!@#$%^&*() 1") == "a-1"
    assert slack_helper.normalize_channel_name("b -_=+ []{}|\\ 2") == "b-2"
    assert slack_helper.normalize_channel_name("c ;:'\" ,.<>/? 3") == "c-3"
    assert slack_helper.normalize_channel_name("-foo ") == "foo"
