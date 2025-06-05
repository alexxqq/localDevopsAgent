from langchain_core.messages import HumanMessage
import asyncio

from agent.graph import build_graph


def main():
    print("Local DevOps Agent CLI")
    app = build_graph()
    state = {
        "messages": [],
        "agent_outcome": None,
        "tool_output": None,
    }

    async def run_loop():
        nonlocal state
        while True:
            user_input = input(">> ")
            if user_input.lower() in ["exit", "quit"]:
                break
            state["messages"].append(HumanMessage(content=user_input))
            state = await app.ainvoke(state)
            last_msg = state["messages"][-1]
            print("🤖", last_msg.content)

    asyncio.run(run_loop())


if __name__ == "__main__":
    main()
