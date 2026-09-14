from runbook.context.budget import TokenBudgetTracker

def test_starts_ok():
    tracker = TokenBudgetTracker(limit=1000, warn_ratio=0.8)
    status = tracker.record(prompt_tokens=100, completion_tokens=50)
    assert status.state == "ok"
    assert status.used_tokens == 150

def test_warns_near_limit():
    tracker = TokenBudgetTracker(limit=1000, warn_ratio=0.8)
    status = tracker.record(prompt_tokens=800, completion_tokens=50)
    assert status.state == "warn"

def test_hard_limit_once_exceeded():
    tracker = TokenBudgetTracker(limit=1000, warn_ratio=0.8)
    status = tracker.record(prompt_tokens=900, completion_tokens=200)
    assert status.state == "hard_limit"

def test_accumulates_across_calls():
    tracker = TokenBudgetTracker(limit=1000, warn_ratio=0.8)
    tracker.record(prompt_tokens=400, completion_tokens=100)
    status = tracker.record(prompt_tokens=400, completion_tokens=100)
    assert status.used_tokens == 1000
    assert status.state == "hard_limit"
