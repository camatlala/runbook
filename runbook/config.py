from dataclasses import dataclass
import os

@dataclass
class Settings:
    db_path: str = os.environ.get("RUNBOOK_DB_PATH", os.path.expanduser("~/.runbook/runbook.db"))
    sandbox_image: str = os.environ.get("RUNBOOK_SANDBOX_IMAGE", "runbook-sandbox:latest")
    max_turns: int = int(os.environ.get("RUNBOOK_MAX_TURNS", "200"))
    max_tokens_per_session: int = int(os.environ.get("RUNBOOK_MAX_TOKENS", "1000000"))
    token_budget_warn_ratio: float = float(os.environ.get("RUNBOOK_BUDGET_WARN_RATIO", "0.8"))
    checkpoint_every_n_turns: int = int(os.environ.get("RUNBOOK_CHECKPOINT_INTERVAL", "10"))

settings = Settings()
