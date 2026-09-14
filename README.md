# Runbook — AI Agent CLI Harness

Self-hosted CLI for an autonomous coding agent that works inside an isolated Docker sandbox, with checkpoint/resume, diff-based context updates, semantic memory, and hard token-budget enforcement so long sessions can keep going instead of hitting a wall.

## Prerequisites

- Python 3.11+
- Docker daemon running (required for the sandbox — session execution and the e2e test need it)
- `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY` for the main agent LLM
- `OPENAI_API_KEY` is **always required**, even when Claude is the main agent LLM, because semantic memory embeddings go through OpenAI regardless of which provider drives the agent loop

## Install

```bash
pip install -e ".[dev]"
docker build -t runbook-sandbox:latest docker/
```

## Usage

```bash
runbook start <repo-url>      # clone a repo into a fresh sandboxed session and enter the REPL
runbook resume <session-id>   # restore a session from its latest checkpoint
runbook list                  # list all sessions
runbook checkpoints <session-id>  # show the latest checkpoint for a session
```

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `RUNBOOK_DB_PATH` | `~/.runbook/runbook.db` | SQLite file path |
| `RUNBOOK_SANDBOX_IMAGE` | `runbook-sandbox:latest` | Docker image used per session |
| `RUNBOOK_MAX_TURNS` | `200` | Turn budget per session |
| `RUNBOOK_MAX_TOKENS` | `1000000` | Token budget per session |
| `RUNBOOK_BUDGET_WARN_RATIO` | `0.8` | Fraction of the token budget at which a warning is shown |
| `RUNBOOK_CHECKPOINT_INTERVAL` | `10` | Turns between automatic checkpoints |

## Known follow-up: REPL not yet wired to the agent loop

`runbook/cli/repl.py`'s `run_repl` is currently a shell — it reads input and echoes a placeholder rather than calling `AgentLoop.run_turn` per message. Wiring the REPL to actually drive the agent (call `run_turn` per input, save a checkpoint every `RUNBOOK_CHECKPOINT_INTERVAL` turns, exit cleanly on `/exit`) is the first follow-up task, since it's glue code across every other component rather than a new isolated unit.

## Run tests

```bash
pytest tests/unit -v
pytest tests/integration -v -m integration   # requires Docker daemon for docker_manager tests
pytest tests/e2e -v -m e2e                   # requires Docker daemon + sandbox image built
```
