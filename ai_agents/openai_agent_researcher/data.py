"""AI Agents data definitions."""

from pydantic import BaseModel


class ResearchItemCommon(BaseModel):
    """Common fields for research items.

    This is not use as a base class since there are some issues with
    openai agents and polymorphism.
    """

    id: int
    "The id of the search item"

    reason: str
    "Your reasoning for why this search is important to the query."

    def __str__(self):
        return f"🔍 {self.id}. {self.reason.removesuffix('.')}:\n"


class SearchResearchItem(BaseModel):
    """Search the web for a specific query."""

    max_tokens: int | None
    "The maximum number of tokens to generate for the search result."

    query: str
    "The search term to use for the web search."

    common: ResearchItemCommon
    "Common fields for research items"

    def __str__(self):
        return f"""{self.common}Search Query: "{self.query}"
{f"Max Tokens: {self.max_tokens}" if self.max_tokens else ""}"""


class AskSomeoneResearchItem(BaseModel):
    """Ask someone for additional information."""

    wait_time_in_seconds: int
    "The time to wait for a response from the person."

    question: str
    "The question to ask someone."

    who: str
    "Who to ask the question to."

    common: ResearchItemCommon
    "Common fields for research items"

    def __str__(self):
        time_limit = ""
        if self.wait_time_in_seconds:
            time_limit = f"Time Limit: {self.wait_time_in_seconds} seconds"

        return f"""{self.common}Person: {self.who}
Question: "{self.question}"
{time_limit}"""


class ResearchPlan(BaseModel):
    """A plan for a research report."""

    question: str
    """What is the question the report needs to answer."""

    tasks: list[SearchResearchItem | AskSomeoneResearchItem]
    """A list of tasks to perform to best answer the query."""

    is_final: bool
    """If the plan is final or not"""

    explanation: str
    """Explanation of the plan"""

    def __str__(self):
        text = f"""{self.explanation}

Q: {self.question}

{"Final" if self.is_final else "Draft"} Plan:
"""
        for task in self.tasks:
            text += f"{task}\n"

        return text


class Report(BaseModel):
    """A report summarizing the findings of the research."""

    question: str
    """The question the report is answering."""

    result: str
    """The result of the report."""

    def __str__(self):
        return f"""\nFinal Report:
Q: {self.question}
A: {self.result}
"""
