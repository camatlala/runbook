from dataclasses import dataclass

@dataclass
class BudgetStatus:
    used_tokens: int
    limit: int
    ratio: float
    state: str  # ok|warn|hard_limit

class TokenBudgetTracker:
    def __init__(self, limit: int, warn_ratio: float = 0.8):
        self._limit = limit
        self._warn_ratio = warn_ratio
        self._used = 0

    def record(self, prompt_tokens: int, completion_tokens: int) -> BudgetStatus:
        self._used += prompt_tokens + completion_tokens
        ratio = self._used / self._limit if self._limit else 1.0

        if self._used >= self._limit:
            state = "hard_limit"
        elif ratio >= self._warn_ratio:
            state = "warn"
        else:
            state = "ok"

        return BudgetStatus(used_tokens=self._used, limit=self._limit, ratio=ratio, state=state)
