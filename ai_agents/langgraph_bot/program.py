"""LangGraph Bot for Slack using LangGraph, Google Gemini LLM, and Google Sheet API."""

from typing import Annotated, TypedDict

from autokitteh.google import google_sheets_client
from autokitteh.slack import slack_client
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition


slack = slack_client("slack_conn")
sheet = google_sheets_client("sheets_conn").spreadsheets().values()


SYSTEM_ROLE = (
    "You are a helpful assistant. Answer the user's questions clearly and concisely. "
    "If you don't know something, you may use a search engine to find "
    "reliable information."
)


@tool
def write_to_sheet(sheet_id: str, table: str):
    """Write into a specified Google Sheet. Provide rows as a CSV-style string."""
    rows = [row.strip().split(",") for row in table.strip().split("\n")]

    sheet.update(
        spreadsheetId=sheet_id,
        range="Sheet1!A1:B7",
        valueInputOption="USER_ENTERED",
        body={"values": rows},
    ).execute()

    return {"status": "success", "message": "wrote to sheet successfully!"}


class State(TypedDict):
    """State of the LangGraph bot."""

    messages: Annotated[list, add_messages]


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
search_tool = TavilySearch(max_results=2)
tools = [search_tool, write_to_sheet]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    """Chat interaction using the LLM and available tools."""
    messages = [{"role": "system", "content": SYSTEM_ROLE}] + state["messages"]
    return {"messages": [llm_with_tools.invoke(messages)]}


# Compile the LangGraph here instead of inside an autokitteh activity.
# Returning builder.compile() directly from an activity causes a pickle error
# due to non-deterministic objects.

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
builder.add_node("tools", tool_node)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()


def on_app_mention(event):
    """Handle incoming Slack messages and respond using the LangGraph bot."""
    initial_state = {"messages": [{"role": "user", "content": event.data.text}]}
    result = graph.invoke(initial_state)

    ai_message = result["messages"][-1]

    slack.chat_postMessage(channel=event.data.channel, text=ai_message.content)
