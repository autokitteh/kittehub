"""Agent tools for the OpenAI agent."""

from agents import function_tool

import data
import slack


@function_tool
async def send_slack_report(r: data.Report, user: str) -> None:
    """Send a Slack report to the given user."""
    slack.send(r, user)
