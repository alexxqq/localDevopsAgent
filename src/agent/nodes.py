from langchain_core.messages import AIMessage
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from .tools import execute_bash_command
from .state import AgentState
from .prompts import SYSTEM_PROMPT
from typing import Literal
from dotenv import load_dotenv
from .safety import safety_check


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
# create tool-using agent
agent = create_openai_functions_agent(llm, tools, prompt)
# langchain agent wrapper, manages state
# internally decide if run tool and run tool!!!!!
agent_executor = AgentExecutor(agent=agent, tools=tools)

async def call_llm_agent(state: AgentState) -> AgentState:
    # if not state.get("validation_passed", True):
    #     return state
    
    latest_input = state["messages"][-1].content
    agent_result = await agent_executor.ainvoke({
        "input": latest_input,
        "messages": state["messages"],
    })

    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=agent_result["output"])],
        "agent_outcome": agent_result.get("intermediate_steps")[-1][0] if agent_result.get("intermediate_steps") else None,
    }

async def validate_input(state: AgentState) -> AgentState:
    """Pre-LLM validation node"""
    user_input = state["messages"][-1].content
    is_safe, reason = await safety_check(user_input)
    
    if not is_safe:
            return {
                **state,
                "messages": state["messages"] + [AIMessage(content=f"{reason}")],
                "validation_passed": False
            }
    
    return {**state, "validation_passed": True}

def router(state: AgentState) -> Literal["process", "end"]:
    """Conditional edge logic"""
    if state.get("validation_passed", True):
        return "process"
    return "end"
