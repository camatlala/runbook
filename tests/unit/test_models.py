from runbook.store.db import get_engine, get_sessionmaker, init_db
from runbook.store.models import Session, Message, Checkpoint, MemoryEntry, TokenUsage

def test_create_and_query_session(tmp_path):
    engine = get_engine(f"sqlite:///{tmp_path}/test.db")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    db = SessionLocal()

    session = Session(repo_url="https://example.com/repo.git", status="running", container_id="c1")
    db.add(session)
    db.commit()
    db.refresh(session)

    assert session.id is not None

    db.add(Message(session_id=session.id, role="user", content="fix the bug"))
    db.add(Checkpoint(session_id=session.id, turn=1, conversation_json="[]", workspace_diff="", memory_pointer=0))
    db.add(MemoryEntry(session_id=session.id, summary="earlier turns about auth", embedding_blob=b"\x00\x01"))
    db.add(TokenUsage(session_id=session.id, turn=1, prompt_tokens=100, completion_tokens=20))
    db.commit()

    assert db.query(Message).count() == 1
    assert db.query(Checkpoint).count() == 1
    assert db.query(MemoryEntry).count() == 1
    assert db.query(TokenUsage).count() == 1
