"""MCPClient integration with Anthropic and Slack.

This module provides an MCPClient class that connects to a server.
Processes queries using Anthropic's API, and posts results to a Slack channel.
"""

import asyncio
from contextlib import AsyncExitStack
import os

from anthropic import Anthropic
import autokitteh
from autokitteh.slack import slack_client
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


slack = slack_client("slack_conn")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERVER_URL = os.getenv("SERVER_URL")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")  # ID or name.


class MCPClient:
    """Client for MCP server queries using Anthropic, with results posted to Slack."""

    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)

    @autokitteh.activity
    async def connect_to_server(self, server_url: str):
        transport = await self.exit_stack.enter_async_context(
            streamablehttp_client(server_url)
        )
        self.read, self.write, _ = transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.read, self.write)
        )
        await self.session.initialize()
        print(f"\nConnected to server at {server_url}")

    @autokitteh.activity
    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]
        tools = (await self.session.list_tools()).tools
        available_tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema,
            }
            for t in tools
        ]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
        )

        for content in response.content:
            if content.type == "text":
                slack.chat_postMessage(channel=SLACK_CHANNEL, text=content.text)
            elif content.type == "tool_use":
                result = await self.session.call_tool(content.name, content.input)
                if result.content:
                    text = f"tool result: {result.content[0].text}\n"
                    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)
                else:
                    text = "Tool returned no content."
                    slack.chat_postMessage(channel=SLACK_CHANNEL, text=text)

    async def cleanup(self):
        await self.exit_stack.aclose()


async def handle_mcp_request(query):
    """Handle a request to the MCP server with the given query."""
    client = MCPClient()
    try:
        await client.connect_to_server(SERVER_URL)
        await client.process_query(query)
    except (ConnectionError, RuntimeError, ValueError) as e:
        print(f"\nError: {str(e)}")
    finally:
        await client.cleanup()


def start_workflow(event):
    """Entrypoint for the MCPClient workflow."""
    query = event.data.text
    asyncio.run(handle_mcp_request(query))
