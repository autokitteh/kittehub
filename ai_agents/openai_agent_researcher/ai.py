"""AI Agents definitions."""

import asyncio
from time import sleep

from agents import Agent
from agents import Runner
from agents import WebSearchTool
from agents.model_settings import ModelSettings
from agents.run import RunConfig
from autokitteh import activity
from openai import RateLimitError

from data import Report
from data import ResearchPlan
from data import SearchResearchItem
from slack import next_input
from slack import send
from tools import send_slack_report


_plan_agent = Agent(
    name="PlannerAgent",
    instructions="""
You are a helpful research assistant. Given a query, come up with a set of tasks
to perform to best answer the query. Output between 3 and 10 tasks to perform.
A task can be either:
- A search task: search the web for a specific term and summarize the results.
- An ask someone task: ask a specific person a question and summarize the answer.
  If a user explicitly specifies a time limit for a specific user, set it as such.
  Do this only if the user explicitly specifies a person to ask.
For each task result, if applicable, default max tokens to None, unless user explicitly
specified otherwise. User cannot be allowed to specify max tokens below 16.
You can also modify an existing plan, by adding or removing searches.
Always provide the complete plan as output along with an indication if the user
considers it final.
Consider the plan as final only if the user explicitly specifies so.
""",
    model="gpt-4o",
    output_type=ResearchPlan,
)

_search_agent = Agent(
    name="SearchAgent",
    instructions="""
You are a research assistant. Given a search term, you search the web for that term and
produce a concise summary of the results. The summary must 2-3 paragraphs and less than
300 words. Capture the main points. Write succinctly, no need to have complete sentences
or good grammar. This will be consumed by someone synthesizing a report, so its vital
you capture the essence and ignore any fluff. Do not include any additional commentary
other than the summary itself.
""",
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=str,
)

_report_agent = Agent(
    name="ReporterAgent",
    instructions="""
Given a question and a set of search results, write a short summary of the findings.
Refine the report per user's feedback.
If the user wishes to send a slack report, use the appropriate tools to send the slack
report to the desired user.
""",
    model="gpt-4o",
    tools=[send_slack_report],
    output_type=Report | str,
)


@activity
def _run(agent: Agent, history: list, q: str, rc: RunConfig) -> tuple[str, list]:
    """Run the agent with the given query and history."""
    send("🤔")

    while True:
        try:
            response = asyncio.run(
                Runner.run(
                    agent,
                    history + [{"role": "user", "content": q}],
                    run_config=rc,
                )
            )

            return response.final_output, response.to_input_list()
        except RateLimitError as e:
            # In case of a rate limit error, retry after waiting for 5 seconds.
            send(f"Rate limit error: {e}\n\nWaiting 5 seconds and retrying...")
            sleep(5)


def _chat(agent, is_final, q: str):
    """Chat with the agent until the response is final.

    An interaction using this function can span some back and forth
    between the user and the agent.

    Args:
        agent: The agent to chat with.
        is_final: A function to check if the response is final.
        q: The initial query.
    """
    history = []
    response = None

    while not (response and is_final(response)):
        if not q:
            q = next_input()

        response, history = _run(agent, history, q, RunConfig())

        send(response)

        q = None

    return response


def plan(q: str) -> ResearchPlan:
    """Plan agent driver."""
    return _chat(_plan_agent, lambda x: x.is_final, q)


def search(q: SearchResearchItem) -> str:
    """Search agent driver."""
    return _run(
        _search_agent,
        [],
        q.query,
        RunConfig(
            model_settings=ModelSettings(
                tool_choice="required",
                max_tokens=q.max_tokens,
            ),
        ),
    )[0]


def report(q: str, tasks: dict[str, str]):
    """Report agent driver."""
    q = f"Question: {q}\n\n\nTasks results: \n"
    for key, value in tasks.items():
        q += f"- {key}: {value}\n\n"

    return _chat(_report_agent, lambda _: False, q)
