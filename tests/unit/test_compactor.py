from unittest.mock import MagicMock
from runbook.memory.compactor import MemoryCompactor

def test_compact_summarizes_and_stores_dropped_entries():
    embedder = MagicMock()
    embedder.embed.return_value = b"\x00\x01\x02\x03"
    store = MagicMock()
    store.add.return_value = 42

    compactor = MemoryCompactor(embedder=embedder, store=store)
    dropped = [{"file_path": "a.py", "score": 0.1, "turn_last_used": 3}]

    result = compactor.compact(dropped)

    assert result == 42
    embedder.embed.assert_called_once()
    summary_text = embedder.embed.call_args[0][0]
    assert "a.py" in summary_text
    store.add.assert_called_once_with(summary_text, b"\x00\x01\x02\x03")

def test_compact_returns_none_for_empty_input():
    embedder = MagicMock()
    store = MagicMock()
    compactor = MemoryCompactor(embedder=embedder, store=store)

    assert compactor.compact([]) is None
    embedder.embed.assert_not_called()
