"""Common code to chat with the agent."""

from os import getenv

import data

from ai import plan
from ai import report
from ai import search
import slack
from slack import ask
from slack import send


_prefix = f"!{getenv('INVOCATION_CMD', 'research')} "


def workflow(q: str):
    """Run the entire interaction with the user.

    There are three phases:
    1. Plan the search.
    2. Execute the search.
    3. Report the results.
    """
    # Plan the search.
    search_plan = plan(q)

    send("Now I will execute on the plan.\n")

    tasks: dict[str, data.ResearchItem] = {}

    # Iterate over all tasks in the plan and execute them.
    for t in search_plan.tasks:
        match type(t):
            case data.SearchResearchItem:
                send(f"🔍 Searching for: {t.query}...")
                tasks[f"Search query result for {t.query}"] = search(t)
            case data.AskSomeoneResearchItem:
                send(f"💬 Asking {t.who} the question: {t.question}...")
                who, answer = ask(t.question, t.who, t.wait_time_in_seconds)
                if who:
                    if not answer:
                        send(f"{t.who} did not answer the question.")
                        answer = "No answer"

                    tasks[f"According to the user {who}"] = answer
                else:
                    tasks[f"According to the user {who}"] = (
                        f"could not figure out which user is {who}"
                    )

    # Summarize and report the results.
    send("All tasks complete, summarizing results...")

    report(search_plan.question, tasks)


def on_slack_message(event):
    text = event.data.text

    if not text.startswith(_prefix):
        print("irrelevant")
        return

    slack.init(event.data.channel, event.data.ts)

    q = text.removeprefix(_prefix)

    print(f"Q: {q}")

    workflow(q)
