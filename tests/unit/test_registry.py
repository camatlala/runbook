import pytest
from runbook.llm.registry import get_adapter
from runbook.llm.claude_adapter import ClaudeAdapter
from runbook.llm.openai_adapter import OpenAIAdapter

def test_get_adapter_returns_claude():
    assert isinstance(get_adapter("claude", api_key="fake-key"), ClaudeAdapter)

def test_get_adapter_returns_openai():
    assert isinstance(get_adapter("openai", api_key="fake-key"), OpenAIAdapter)

def test_get_adapter_rejects_unknown_provider():
    with pytest.raises(ValueError):
        get_adapter("unknown-provider", api_key="fake-key")
