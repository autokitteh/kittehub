"""Agent tools for the OpenAI agent."""

from agents import function_tool
from data import Report

from slack import send


@function_tool
async def send_slack_report(r: Report, user: str) -> None:
    """Send a slack report to the given user."""
    send(r, user)
