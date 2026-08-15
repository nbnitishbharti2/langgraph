from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages, BaseMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv(override=True)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "TracingProject")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "true")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "TracingProject")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "")

## Intialize LLM
from langchain_groq import ChatGroq

llm= ChatGroq(model="qwen/qwen3.6-27b")

## Create state
class State(TypedDict):
  messages: Annotated[list[BaseMessage], add_messages]

## Graph with tool call




def make_tool_graph():
    """
    Make tool graph
    """

    @tool
    def add(a: float, b: float):
      """Add two number"""
      return a + b

    tools = [add]
    llm_with_tools = llm.bind_tools(tools)

    ## Node defnition
    def call_llm_model(state: State):
        return {"messages": [llm_with_tools.invoke(state['messages'])]}


    ## Create G raph
    builder = StateGraph(State)

    ## Add nodes
    builder.add_node("chatbot", call_llm_model)

    tool_node = ToolNode(tools=tools)
    builder.add_node("tools", tool_node)

    ## Add Edges
    builder.add_edge(START, "chatbot")
    builder.add_conditional_edges(
      "chatbot",
      tools_condition
    )
    builder.add_edge("tools", "chatbot")


    ## Compile the graph
    graph = builder.compile()
    return graph

tool_agent = make_tool_graph()