from runbook.context.pruner import prune_context

def test_current_task_files_always_kept():
    entries = [
        {"file_path": "a.py", "score": 0.1, "turn_last_used": 1},
        {"file_path": "b.py", "score": 0.9, "turn_last_used": 1},
    ]
    kept, dropped = prune_context(entries, current_task_files={"a.py"}, max_entries=1)
    assert "a.py" in {e["file_path"] for e in kept}

def test_dropped_entries_are_returned():
    entries = [
        {"file_path": "a.py", "score": 0.1, "turn_last_used": 1},
        {"file_path": "b.py", "score": 0.9, "turn_last_used": 1},
        {"file_path": "c.py", "score": 0.5, "turn_last_used": 1},
    ]
    kept, dropped = prune_context(entries, current_task_files=set(), max_entries=2)
    assert {e["file_path"] for e in kept} == {"b.py", "c.py"}
    assert {e["file_path"] for e in dropped} == {"a.py"}
