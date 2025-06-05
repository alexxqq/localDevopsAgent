from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import call_llm_agent


def build_graph():
    """Simplified graph with single node"""
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_llm_agent)
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    return workflow.compile()
