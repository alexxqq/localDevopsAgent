from langchain_core.messages import BaseMessage

from typing import List, TypedDict, Union, Optional


class AgentState(TypedDict):
    """
    Enhanced agent state with validation tracking.
    
    Attributes:
        messages: All messages in the conversation
        agent_outcome: Last LLM output (tool call or final answer)
        tool_output: Last tool execution result
    """
    messages: List[BaseMessage]
    agent_outcome: Optional[Union[BaseMessage, dict]]
    tool_output: Optional[str]
