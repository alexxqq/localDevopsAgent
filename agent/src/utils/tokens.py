import tiktoken
from langchain_core.messages import BaseMessage

from typing import List

def num_tokens_from_messages(messages: List[BaseMessage], model: str = "gpt-4o-mini") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0
    for msg in messages:
        tokens += 4
        tokens += len(encoding.encode(msg.content or ""))
    tokens += 2
    return tokens

def trim_messages_to_fit(messages: List[BaseMessage], max_tokens: int, model: str = "gpt-4o-mini") -> List[BaseMessage]:
    encoding = tiktoken.encoding_for_model(model)
    reversed_messages = list(reversed(messages))

    total_tokens = 2
    result = []

    for msg in reversed_messages:
        tokens = 4 + len(encoding.encode(msg.content or ""))
        if total_tokens + tokens > max_tokens:
            break
        result.append(msg)
        total_tokens += tokens

    return list(reversed(result))
