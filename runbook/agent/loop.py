from dataclasses import dataclass, field
from runbook.llm.base import LLMAdapter
from runbook.sandbox.docker_manager import SandboxManager
from runbook.context.pipeline import ContextPipeline
from runbook.memory.embedder import Embedder
from runbook.memory.store import MemoryStore
from runbook.memory.compactor import MemoryCompactor
from runbook.agent.tools import TOOL_SCHEMAS, dispatch_tool_call

@dataclass
class AgentTurnResult:
    done: bool
    assistant_text: str
    tool_results: list[str] = field(default_factory=list)
    budget_state: str = "ok"
    prompt_tokens: int = 0
    completion_tokens: int = 0

class AgentLoop:
    def __init__(self, llm: LLMAdapter, sandbox: SandboxManager, container_id: str,
                 pipeline: ContextPipeline, embedder: Embedder, memory_store: MemoryStore, compactor: MemoryCompactor):
        self._llm = llm
        self._sandbox = sandbox
        self._container_id = container_id
        self._pipeline = pipeline
        self._embedder = embedder
        self._memory_store = memory_store
        self._compactor = compactor

    def run_turn(self, task: str, files: dict[str, str], turn: int) -> AgentTurnResult:
        task_embedding = self._embedder.embed(task)
        relevant_memory = self._memory_store.search(task_embedding, top_k=3)

        assembled = self._pipeline.assemble(files, current_task_files=set(files.keys()), turn=turn)
        self._compactor.compact(assembled["dropped"])

        memory_text = "\n".join(f"- {summary}" for _, summary, _ in relevant_memory)
        context_text = "\n\n".join(f"# {e['file_path']}\n{e['content']}" for e in assembled["entries"])

        messages = [
            {"role": "user", "content": f"Task: {task}\n\nRelevant memory:\n{memory_text}\n\nContext:\n{context_text}"},
        ]
        response = self._llm.complete(messages, TOOL_SCHEMAS)

        tool_results = [
            dispatch_tool_call(self._sandbox, self._container_id, call)
            for call in response.tool_calls
        ]

        budget_status = self._pipeline.budget.record(response.prompt_tokens, response.completion_tokens)

        return AgentTurnResult(
            done=len(response.tool_calls) == 0,
            assistant_text=response.text,
            tool_results=tool_results,
            budget_state=budget_status.state,
            prompt_tokens=response.prompt_tokens,
            completion_tokens=response.completion_tokens,
        )
