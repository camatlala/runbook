<h1 align="center">📓 Runbook</h1>
<p align="center"><b>AI Agent CLI Harness</b></p>

<p align="center">
  <a href="https://github.com/DenverCoder1/readme-typing-svg">
    <img src="https://readme-typing-svg.demolab.com/?lines=Checkpoint+%2B+resume+long+sessions;Semantic+memory+over+pruned+context;Hard+token-budget+enforcement;Docker-isolated+coding+agent&font=Fira%20Code&center=true&width=520&height=45&color=b76cf0&vCenter=true&pause=1000&size=20" /></a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11+-14354C.svg?logo=python&logoColor=white">
  <img alt="Typer" src="https://custom-icon-badges.demolab.com/badge/-Typer-000000?style=flat&logoColor=white&logo=terminal">
  <img alt="Rich" src="https://custom-icon-badges.demolab.com/badge/-Rich-fae5d1?style=flat&logoColor=black&logo=terminal">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-07405e.svg?logo=sqlite&logoColor=white">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white">
  <img alt="pytest" src="https://img.shields.io/badge/Pytest-0A9EDC.svg?logo=pytest&logoColor=white">
  <img alt="Self-hosted" src="https://custom-icon-badges.demolab.com/badge/-Self--hosted-1F222E?style=flat&logoColor=white&logo=home">
</p>

<p align="center">
  A CLI for an autonomous coding agent that keeps going instead of hitting a wall — checkpoint/resume, diff-based context, semantic memory over what gets pruned, and hard token-budget gating.
</p>

<br/>

<details open>
<summary><h2>🧩 Architecture</h2></summary>

Single installable Python package. Typer + Rich drive an agent loop in the CLI process; each session's file edits and commands run inside a per-session Docker container via `docker exec`.

| Piece | Role |
|---|---|
| `runbook/sandbox/` | Docker session manager (same pattern as Patchwork) |
| `runbook/context/` | Cache → diff → pruner → **hard token-budget gate** |
| `runbook/memory/` | OpenAI-embedding semantic memory — pruned turns get summarized & embedded, never just discarded |
| `runbook/checkpoint/` | Full session-state snapshots (conversation + workspace diff + memory pointer) |
| `runbook/cli/` | Typer app (`start` / `resume` / `list` / `checkpoints`) + REPL |

</details>

<details open>
<summary><h2>🚀 Quickstart</h2></summary>

**Prerequisites:** Python 3.11+, Docker daemon running, `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY`.

> `OPENAI_API_KEY` is **always required**, even with Claude as the main agent LLM — semantic memory embeddings always go through OpenAI.

```bash
pip install -e ".[dev]"
docker build -t runbook-sandbox:latest docker/
```

```bash
runbook start <repo-url>          # clone into a sandboxed session, enter the REPL
runbook resume <session-id>       # restore from the latest checkpoint
runbook list                      # list all sessions
runbook checkpoints <session-id>  # show the latest checkpoint
```

</details>

<details>
<summary><h2>⚙️ Environment Variables</h2></summary>

| Variable | Default | Purpose |
|---|---|---|
| `RUNBOOK_DB_PATH` | `~/.runbook/runbook.db` | SQLite file path |
| `RUNBOOK_SANDBOX_IMAGE` | `runbook-sandbox:latest` | Docker image used per session |
| `RUNBOOK_MAX_TURNS` | `200` | Turn budget per session |
| `RUNBOOK_MAX_TOKENS` | `1000000` | Token budget per session |
| `RUNBOOK_BUDGET_WARN_RATIO` | `0.8` | Fraction of budget at which a warning shows |
| `RUNBOOK_CHECKPOINT_INTERVAL` | `10` | Turns between automatic checkpoints |

</details>

<details>
<summary><h2>🧪 Testing</h2></summary>

```bash
pytest tests/unit -v
pytest tests/integration -v -m integration   # requires Docker daemon
pytest tests/e2e -v -m e2e                   # requires Docker daemon + sandbox image built
```

</details>

<details>
<summary><h2>⚠️ Known Follow-up</h2></summary>

`runbook/cli/repl.py`'s `run_repl` is currently a shell — it doesn't yet call `AgentLoop.run_turn` per input. Wiring the REPL to actually drive the agent (call `run_turn` per message, checkpoint every `RUNBOOK_CHECKPOINT_INTERVAL` turns, exit cleanly on `/exit`) is the first follow-up, since it's glue code across every other component rather than a new isolated unit.

</details>

<details>
<summary><h2>📌 Status</h2></summary>

28/29 tests passing. Only the Docker-dependent sandbox test needs a live daemon to verify — run `pytest tests/integration -v -m integration` once Docker is confirmed working.

</details>
