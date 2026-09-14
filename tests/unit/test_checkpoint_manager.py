from runbook.store.db import get_engine, get_sessionmaker, init_db
from runbook.store.models import Session
from runbook.checkpoint.manager import CheckpointManager

def test_save_and_load_latest_checkpoint(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    session = Session(repo_url="https://example.com/repo.git", status="running")
    db.add(session)
    db.commit()
    db.refresh(session)

    manager = CheckpointManager()
    conversation = [{"role": "user", "content": "fix the bug"}]
    manager.save(db, session.id, turn=1, conversation=conversation, workspace_diff="diff --git a b", memory_pointer=2)
    manager.save(db, session.id, turn=5, conversation=conversation + [{"role": "assistant", "content": "done"}], workspace_diff="diff2", memory_pointer=4)

    latest = manager.latest(db, session.id)
    assert latest["turn"] == 5
    assert latest["memory_pointer"] == 4
    assert len(latest["conversation"]) == 2

def test_latest_returns_none_when_no_checkpoints(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    manager = CheckpointManager()
    assert manager.latest(db, session_id=999) is None
