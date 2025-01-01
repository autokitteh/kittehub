"""Markdown-related helper functions across GitHub and Slack."""

import collections
import re
from urllib.parse import urlparse

from slack_sdk.errors import SlackApiError

import debug
import slack_helper
import users


_GithubUser = collections.namedtuple("GithubUser", ["login", "html_url"])
_SlackChannel = collections.namedtuple("SlackChannel", ["name", "id"])
_SlackUser = collections.namedtuple("SlackUser", ["link", "id"])


slack = slack_helper.shared_client


def github_to_slack(text: str, pr_url: str) -> str:
    """Convert GitHub markdown text to Slack markdown text.

    References:
    - https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax
    - https://api.slack.com/reference/surfaces/formatting

    Args:
        text: Text body, possibly containing GitHub markdown.
        pr_url: URL of the PR we're working on, used to convert
            other PR references in the text ("#123") to links.

    Returns:
        Slack markdown text.
    """
    # Header lines --> bold lines.
    text = re.sub(r"^#+\s+(.+)", r"**\1**", text, flags=re.MULTILINE)

    # Bold and italic text together: "*** ... ***" --> "_* ... *_".
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"_**\1**_", text)

    # Italic text: "*" --> "_" ("_" -> "_" is a no-op).
    text = re.sub(r"(^|[^*])\*([^*]+?)\*", r"\1_\2_", text)

    # Bold text: "**" or "__" --> "*".
    text = re.sub(r"\*\*(.+?)\*\*", r"*\1*", text)
    text = re.sub(r"__(.+?)__", r"*\1*", text)

    # Strikethrough text: "~~" --> "~" ("~" -> "~" is a no-op).
    text = re.sub(r"~~(.+?)~~", r"~\1~", text)

    # Links: "[text](url)" --> "<url|text>".
    # Images: "![text](url)" --> "!<url|text>" --> "Image: <url|text>".
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"<\2|\1>", text)
    text = re.sub(r"!<(.*?)>", r"Image: <\1>", text)

    # Lists (up to 2 levels): "-" or "*" or "+" --> "•" and "◦".
    for bullet in ("-", r"\+"):
        text = re.sub(rf"^{bullet}\s*", "  •  ", text, flags=re.MULTILINE)
        text = re.sub(
            rf"^\s{{2,4}}{bullet}\s*", r"          ◦   ", text, flags=re.MULTILINE
        )

    # Mentions: "@user" --> "<@U123>" or "<https://github.com/user|@user>",
    # "@org/team" --> "<https://github.com/org/teams/team|@org/team>".
    for github_user in re.findall(r"@[\w/-]+", text):
        parsed = urlparse(pr_url)
        url_suffix = github_user[1:]
        if "/" in url_suffix:
            url_suffix = url_suffix.replace("/", "/teams/")
        profile_link = f"{parsed.scheme}://{parsed.netloc}/{url_suffix}"
        user_obj = _GithubUser(login=github_user[1:], html_url=profile_link)
        slack_user = users.format_github_user_for_slack(user_obj)
        text = text.replace(github_user, slack_user)

    # PR references: "#123" --> "<PR URL|#123>" (works for issues too).
    url_base = re.sub(r"/pull/\d+$", "/pull", pr_url)
    text = re.sub(r"#(\d+)", rf"<{url_base}/\1|#\1>", text)

    # Hide HTML comments.
    text = re.sub(r"<!--.+?-->", "", text, flags=re.DOTALL)

    return text


def slack_to_github(text: str) -> str:
    """Convert Slack markdown text to GitHub markdown text.

    References:
    - https://api.slack.com/reference/surfaces/formatting
    - https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

    Args:
        text: Text body, possibly containing Slack markdown.

    Returns:
        GitHub markdown text.
    """
    # Bold and italic text together: "_*" or "*_" --> "***".
    text = re.sub(r"_\*(.+?)\*_", r"***\1***", text)
    text = re.sub(r"\*_(.+?)_\*", r"***\1***", text)

    # Bold text: "*" --> "**" (italic text is a no-op: "_" --> "_").
    text = re.sub(r"(^|[^*])\*([^*]+?)\*", r"\1**\2**", text)

    # Italic text: "__" --> "_".
    text = re.sub(r"__(.+?)__", r"_\1_", text)

    # Strikethrough text: "~" --> "~~" ("~~" -> "~~" is a no-op).
    text = re.sub(r"(^|[^~])~([^~]+?)~", r"\1~~\2~~", text)

    # Block quotes: "&gt; aaa" --> "> aaa".
    text = re.sub(r"^&gt;(.*)", r">\1", text, flags=re.MULTILINE)

    # Multiline code blocks: ```aaa\nbbb``` --> ```\naaa\nbbb\n```.
    text = re.sub(r"```(.+?)```", r"```\n\1\n```", text, flags=re.DOTALL)

    # Lists (up to 5 levels): "•", "◦", and "▪︎" --> "-".
    text = re.sub(r"^•", "-", text, flags=re.MULTILINE)
    text = re.sub(r"^    ◦", "  -", text, flags=re.MULTILINE)
    text = re.sub(r"^        ▪︎", "    -", text, flags=re.MULTILINE)
    text = re.sub(r"^            •", "      -", text, flags=re.MULTILINE)
    text = re.sub(r"^                ◦", "        -", text, flags=re.MULTILINE)

    # Links: "<url|text>" or "<@...>" or "<#...>" --> "[text](url)".
    text = re.sub(r"<(.*?)\|(.*?)>", r"[\2](\1)", text)
    text = re.sub(r"<([@#][A-Z0-9]+)>", r"[](\1)", text)

    # Channel references: "<#...>" or "<#...|name>" --> "[name](#...)" -->
    # "[#name](slack://channel?team={TEAM_ID}&id={CHANNEL_ID})"
    # (see https://api.slack.com/reference/deep-linking).
    for channel in re.findall(r"\[(.*?)\]\(#([A-Z0-9]+)\)", text):
        channel = _SlackChannel(*channel)
        old = f"[{channel.name}](#{channel.id})"
        if not channel.name:
            channel = _SlackChannel(_slack_channel_name(channel.id), channel.id)
        team_id = _slack_team_id()
        new = f"[#{channel.name}](slack://channel?team={team_id}&id={channel.id})"
        text = text.replace(old, new)

    # User mentions: "<@...>" --> "[](@...)" --> "@github-user" or "Full Name".
    for slack_user in re.findall(r"(\[.*?\]\(@([A-Z0-9]+)\))", text):
        slack_user = _SlackUser(*slack_user)
        github_user = users.format_slack_user_for_github(slack_user.id)
        text = text.replace(slack_user.link, github_user)

    return text


def _slack_channel_name(id: str) -> str:
    """Return the name of a Slack channel based on its ID."""
    try:
        resp = slack.conversations_info(channel=id)
        return resp.get("channel", {}).get("name", "")
    except SlackApiError as e:
        error = f"Failed to get Slack channel info for <#{id}>"
        debug.log(f"{error}: `{e.response['error']}`")
        return ""


def _slack_team_id() -> str:
    """Return the Slack app's team ID."""
    try:
        return slack.auth_test().get("team_id", "")
    except SlackApiError as e:
        debug.log(f"Slack auth test failed: `{e.response['error']}`")
        return ""
