from anthropic import Anthropic
from runbook.llm.base import LLMAdapter, LLMResponse, ToolCall

class ClaudeAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "claude-sonnet-5"):
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def complete(self, messages: list[dict], tools: list[dict]) -> LLMResponse:
        response = self._client.messages.create(
            model=self._model, max_tokens=4096, messages=messages, tools=tools,
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        tool_calls = [
            ToolCall(id=block.id, name=block.name, arguments=block.input)
            for block in response.content if block.type == "tool_use"
        ]
        return LLMResponse(
            text=text, tool_calls=tool_calls,
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
        )
