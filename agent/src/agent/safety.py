from langchain_core.messages import HumanMessage, SystemMessage
from typing import Tuple
from dotenv import load_dotenv
from .prompts import REVIEWER_SYSTEM_PROMPT
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
safety_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

async def safety_check(command: str) -> Tuple[bool, str]:
    """Use a separate LLM to validate command safety"""
    response = await safety_llm.ainvoke([
        SystemMessage(content=REVIEWER_SYSTEM_PROMPT),
        HumanMessage(content=command)
    ])
    return ("APPROVED" in response.content), response.content
