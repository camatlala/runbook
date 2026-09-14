import numpy as np

class MemoryStore:
    def __init__(self):
        self._entries: list[tuple[int, str, bytes]] = []
        self._next_id = 1

    def add(self, summary: str, embedding: bytes) -> int:
        entry_id = self._next_id
        self._entries.append((entry_id, summary, embedding))
        self._next_id += 1
        return entry_id

    def search(self, query_embedding: bytes, top_k: int = 3) -> list[tuple[int, str, float]]:
        query_vec = np.frombuffer(query_embedding, dtype=np.float32)
        results = []
        for entry_id, summary, embedding in self._entries:
            vec = np.frombuffer(embedding, dtype=np.float32)
            denom = (np.linalg.norm(query_vec) * np.linalg.norm(vec))
            similarity = float(np.dot(query_vec, vec) / denom) if denom else 0.0
            results.append((entry_id, summary, similarity))

        results.sort(key=lambda r: r[2], reverse=True)
        return results[:top_k]
