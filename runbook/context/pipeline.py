from runbook.context.cache import ContextCache
from runbook.context.differ import build_diff
from runbook.context.pruner import prune_context
from runbook.context.budget import TokenBudgetTracker

class ContextPipeline:
    def __init__(self, budget_limit: int, budget_warn_ratio: float = 0.8, max_entries: int = 20):
        self.cache = ContextCache()
        self.budget = TokenBudgetTracker(limit=budget_limit, warn_ratio=budget_warn_ratio)
        self._max_entries = max_entries

    def assemble(self, files: dict[str, str], current_task_files: set[str], turn: int) -> dict:
        entries = []
        for file_path, content in files.items():
            previous = self.cache.get(file_path)
            body = build_diff(previous, content) if self.cache.has_changed(file_path, content) or previous is None else "NO CHANGE"
            self.cache.put(file_path, content)
            entries.append({"file_path": file_path, "content": body, "score": 1.0 if file_path in current_task_files else 0.0, "turn_last_used": turn})

        kept, dropped = prune_context(entries, current_task_files, max_entries=self._max_entries)

        return {
            "entries": [{"file_path": e["file_path"], "content": e["content"]} for e in kept],
            "dropped": dropped,
        }
