from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict

@dataclass
class LLMResponse:
    text: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0

class LLMAdapter(ABC):
    @abstractmethod
    def complete(self, messages: list[dict], tools: list[dict]) -> LLMResponse:
        ...
