"""AI Agents definitions."""

import asyncio

from agents import Agent
from agents import Runner
from agents import WebSearchTool


_cats_agent = Agent(
    name="Cats Agent",
    handoff_description="""Specialist agent for questions about cats.
Always include the word 'meow' in your responses.
""",
    instructions="You provide help questions about cats",
)

_dogs_agent = Agent(
    name="Dogs Agent",
    handoff_description="""Specialist agent for questions about dogs.
Always include the word 'woof' in your responses.
""",
    instructions="You provide help questions about dogs",
)

_search_agent = Agent(
    name="Search Agent",
    handoff_description="""Specialist agent for web searches.
Explicitly say you found your answer on the web and which url you found it at.
""",
    instructions="""You search the web for answers to queries.
""",
    tools=[WebSearchTool()],
)

_triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's question.",
    handoffs=[_cats_agent, _dogs_agent, _search_agent],
)


def run(history, q):
    return asyncio.run(
        Runner.run(
            _triage_agent,
            history + [{"role": "user", "content": q}],
        )
    )
