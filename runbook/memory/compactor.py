from runbook.memory.embedder import Embedder
from runbook.memory.store import MemoryStore

class MemoryCompactor:
    def __init__(self, embedder: Embedder, store: MemoryStore):
        self._embedder = embedder
        self._store = store

    def compact(self, dropped_entries: list[dict]) -> int | None:
        if not dropped_entries:
            return None

        file_list = ", ".join(e["file_path"] for e in dropped_entries)
        summary = f"Context pruned at turn {dropped_entries[-1]['turn_last_used']}: files no longer in active context: {file_list}"

        embedding = self._embedder.embed(summary)
        return self._store.add(summary, embedding)
