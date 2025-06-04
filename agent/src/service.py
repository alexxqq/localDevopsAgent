# chatbot.py
from langchain_core.messages import HumanMessage
from agent.graph import build_graph
import asyncio

app = build_graph()
state = {
    "messages": [],
    "agent_outcome": None,
    "tool_output": None,
    "validation_passed": None,
    "pending_command": None
}

async def get_chat_response(user_input: str):
    global state
    state["messages"].append(HumanMessage(content=user_input))
    state = await app.ainvoke(state)
    last_msg = state["messages"][-1]
    return last_msg.content
