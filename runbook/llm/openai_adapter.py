from openai import OpenAI
from runbook.llm.base import LLMAdapter, LLMResponse, ToolCall

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str = "gpt-4.1"):
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def complete(self, messages: list[dict], tools: list[dict]) -> LLMResponse:
        response = self._client.chat.completions.create(model=self._model, messages=messages, tools=tools)
        choice = response.choices[0]
        text = choice.message.content or ""
        tool_calls = [
            ToolCall(id=tc.id, name=tc.function.name, arguments=tc.function.arguments)
            for tc in (choice.message.tool_calls or [])
        ]
        return LLMResponse(
            text=text, tool_calls=tool_calls,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
        )
