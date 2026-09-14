from runbook.llm.base import LLMAdapter
from runbook.llm.claude_adapter import ClaudeAdapter
from runbook.llm.openai_adapter import OpenAIAdapter

_ADAPTERS = {"claude": ClaudeAdapter, "openai": OpenAIAdapter}

def get_adapter(provider: str, api_key: str) -> LLMAdapter:
    adapter_cls = _ADAPTERS.get(provider)
    if adapter_cls is None:
        raise ValueError(f"Unknown LLM provider: {provider}")
    return adapter_cls(api_key=api_key)
