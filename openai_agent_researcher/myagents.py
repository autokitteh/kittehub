from agents import Agent
from agents import Runner


_cats_agent = Agent(
    name="Cats Agent",
    handoff_description="Specialist agent for questions about cats",
    instructions="You provide help questions about cats",
)

_dogs_agent = Agent(
    name="Dogs Agent",
    handoff_description="Specialist agent for questions about dogs",
    instructions="You provide help questions about dogs",
)


_triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's question",
    handoffs=[_cats_agent, _dogs_agent],
)


def run(history, q):
    return Runner.run_sync(
        _triage_agent,
        history + [{"role": "user", "content": q}],
    )
