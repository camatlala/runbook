import numpy as np
from runbook.memory.store import MemoryStore

def _vec(*values):
    return np.array(values, dtype=np.float32).tobytes()

def test_search_ranks_by_cosine_similarity():
    store = MemoryStore()
    store.add("about auth", _vec(1.0, 0.0))
    store.add("about billing", _vec(0.0, 1.0))

    results = store.search(_vec(0.9, 0.1), top_k=2)

    assert results[0][1] == "about auth"
    assert results[0][2] > results[1][2]

def test_search_respects_top_k():
    store = MemoryStore()
    for i in range(5):
        store.add(f"entry {i}", _vec(1.0, float(i)))

    results = store.search(_vec(1.0, 0.0), top_k=2)
    assert len(results) == 2
