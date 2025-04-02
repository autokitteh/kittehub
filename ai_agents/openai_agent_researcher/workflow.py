"""Main workflow logic."""

from os import getenv

import ai
import data
import slack


_prefix = f"!{getenv('INVOCATION_CMD', 'research')} "


def workflow(q: str):
    """Run the entire interaction with the user.

    There are three phases:
    1. Plan the search.
    2. Execute the search.
    3. Report the results.
    """
    # Plan the search.
    search_plan = ai.plan(q)

    # Iterate over all tasks in the plan and execute them.
    slack.send("Now I will execute on the plan.\n")
    tasks: dict[str, data.ResearchItem] = {}
    for t in search_plan.tasks:
        match type(t):
            case data.SearchResearchItem:
                slack.send(f"🔍 Searching for: {t.query}...")
                tasks[f"Search query result for {t.query}"] = ai.search(t)
            case data.AskSomeoneResearchItem:
                slack.send(f"💬 Asking {t.who} the question: {t.question}...")
                who, answer = slack.ask(t.question, t.who, t.wait_time_in_seconds)
                if who:
                    if not answer:
                        slack.send(f"{who['real_name']} did not answer the question.")
                        answer = "No answer"

                    tasks[f"According to the user {who['real_name']}"] = answer
                else:
                    tasks[f"According to the user {t.who}"] = (
                        f"could not figure out which user is {t.who}"
                    )

    # Summarize and report the results.
    slack.send("All tasks complete, summarizing results...")
    ai.report(search_plan.question, tasks)


def on_slack_message(event):
    text = event.data.text

    if not text.startswith(_prefix):
        print("irrelevant")
        return

    slack.init(event.data.channel, event.data.ts)

    q = text.removeprefix(_prefix)
    print(f"Q: {q}")

    workflow(q)
