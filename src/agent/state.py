from typing import List, TypedDict, Union, Optional
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    Enhanced agent state with validation tracking.
    
    Attributes:
        messages: All messages in the conversation
        agent_outcome: Last LLM output (tool call or final answer)
        tool_output: Last tool execution result
        validation_passed: Whether input passed safety checks (new)
        pending_command: Raw command awaiting validation (new)
    """
    messages: List[BaseMessage]
    agent_outcome: Optional[Union[BaseMessage, dict]]
    tool_output: Optional[str]
    validation_passed: Optional[bool]
    pending_command: Optional[str]