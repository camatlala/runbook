import os
import shutil
import subprocess
import tempfile
import pytest
from unittest.mock import MagicMock
from runbook.sandbox.docker_manager import SandboxManager
from runbook.agent.loop import AgentLoop
from runbook.llm.base import LLMResponse
from runbook.context.pipeline import ContextPipeline
from runbook.memory.store import MemoryStore
from runbook.checkpoint.manager import CheckpointManager
from runbook.store.db import get_engine, get_sessionmaker, init_db
from runbook.store.models import Session

pytestmark = pytest.mark.e2e

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "tiny_repo")

@pytest.fixture
def tiny_git_repo():
    tmp_dir = tempfile.mkdtemp(prefix="runbook_tiny_repo_")
    with open(os.path.join(tmp_dir, "calc.py"), "w") as f:
        f.write("def add(a, b):\n    return a - b\n")
    subprocess.run(["git", "init", "-q"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_dir, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=tmp_dir, check=True)
    yield tmp_dir
    shutil.rmtree(tmp_dir, ignore_errors=True)

def test_start_turn_checkpoint_resume_roundtrip(tiny_git_repo, tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    sandbox = SandboxManager(image="runbook-sandbox:latest")
    container_id = sandbox.create_session(f"file://{tiny_git_repo}")

    session = Session(repo_url=f"file://{tiny_git_repo}", status="running", container_id=container_id)
    db.add(session)
    db.commit()
    db.refresh(session)

    llm = MagicMock()
    llm.complete.return_value = LLMResponse(text="Fixed it.", tool_calls=[], prompt_tokens=10, completion_tokens=5)
    embedder = MagicMock()
    embedder.embed.return_value = b"\x00\x01\x02\x03"
    memory_store = MemoryStore()
    compactor = MagicMock()

    loop = AgentLoop(
        llm=llm, sandbox=sandbox, container_id=container_id,
        pipeline=ContextPipeline(budget_limit=100000),
        embedder=embedder, memory_store=memory_store, compactor=compactor,
    )
    result = loop.run_turn("fix the subtraction bug", {"calc.py": "def add(a, b):\n    return a - b\n"}, turn=1)
    assert result.done is True

    checkpoint_manager = CheckpointManager()
    checkpoint_manager.save(db, session.id, turn=1, conversation=[{"role": "assistant", "content": result.assistant_text}], workspace_diff="", memory_pointer=0)

    latest = checkpoint_manager.latest(db, session.id)
    assert latest["turn"] == 1
    assert latest["conversation"][0]["content"] == "Fixed it."

    sandbox.destroy(container_id)
