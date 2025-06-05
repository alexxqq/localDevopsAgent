from langchain_core.messages import AIMessage
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

from typing import Literal

from utils.tokens import trim_messages_to_fit
from .prompts import SYSTEM_PROMPT
from .state import AgentState
from .tools import execute_bash_command

MAX_TOKENS_FOR_HISTORY = 13_000

load_dotenv()

tools = [execute_bash_command, ]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# prompt template for each prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="messages"), 
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
# create tool-using agent (openai fucnctions)
agent = create_openai_functions_agent(llm, tools, prompt)
# langchain agent wrapper, manages state
# internally decide if run tool and run tool!!!!!
agent_executor = AgentExecutor(agent=agent, tools=tools)

async def call_llm_agent(state: AgentState) -> AgentState:
    trimmed_messages = trim_messages_to_fit(state["messages"], MAX_TOKENS_FOR_HISTORY)
    latest_input = trimmed_messages[-1].content

    agent_result = await agent_executor.ainvoke({
        "input": latest_input,
        "messages": trimmed_messages,
    })

    return {
        **state,
        "messages": trimmed_messages + [AIMessage(content=agent_result["output"])],
        "agent_outcome": agent_result.get("intermediate_steps")[-1][0] if agent_result.get("intermediate_steps") else None,
    }
