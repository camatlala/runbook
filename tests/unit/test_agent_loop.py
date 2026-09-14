from unittest.mock import MagicMock
from runbook.agent.loop import AgentLoop
from runbook.llm.base import LLMResponse, ToolCall
from runbook.context.pipeline import ContextPipeline
from runbook.memory.store import MemoryStore

def test_run_turn_with_no_tool_calls_marks_done():
    llm = MagicMock()
    llm.complete.return_value = LLMResponse(text="All done.", tool_calls=[], prompt_tokens=10, completion_tokens=5)
    sandbox = MagicMock()
    embedder = MagicMock()
    embedder.embed.return_value = b"\x00\x01\x02\x03"
    memory_store = MemoryStore()
    compactor = MagicMock()

    loop = AgentLoop(
        llm=llm, sandbox=sandbox, container_id="c1",
        pipeline=ContextPipeline(budget_limit=100000),
        embedder=embedder, memory_store=memory_store, compactor=compactor,
    )
    result = loop.run_turn("fix the bug", {"a.py": "print(1)"}, turn=1)

    assert result.done is True
    assert result.assistant_text == "All done."
    assert result.budget_state == "ok"

def test_run_turn_dispatches_tool_call_and_continues():
    llm = MagicMock()
    llm.complete.return_value = LLMResponse(
        text="Running tests.",
        tool_calls=[ToolCall(id="1", name="run_command", arguments={"command": ["pytest"]})],
        prompt_tokens=10, completion_tokens=5,
    )
    sandbox = MagicMock()
    sandbox.exec.return_value = MagicMock(exit_code=0, stdout="1 passed", stderr="", timed_out=False)
    embedder = MagicMock()
    embedder.embed.return_value = b"\x00\x01\x02\x03"
    memory_store = MemoryStore()
    compactor = MagicMock()

    loop = AgentLoop(
        llm=llm, sandbox=sandbox, container_id="c1",
        pipeline=ContextPipeline(budget_limit=100000),
        embedder=embedder, memory_store=memory_store, compactor=compactor,
    )
    result = loop.run_turn("run the tests", {"a.py": "print(1)"}, turn=1)

    assert result.done is False
    assert "1 passed" in result.tool_results[0]
