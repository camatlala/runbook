from runbook.checkpoint.manager import CheckpointManager
from runbook.sandbox.docker_manager import SandboxManager
from runbook.store.models import Session

def resume_session(db, session_id: int, sandbox: SandboxManager) -> dict:
    session = db.query(Session).get(session_id)
    if session is None:
        raise ValueError(f"No session with id {session_id}")

    checkpoint = CheckpointManager().latest(db, session_id)
    if checkpoint is None:
        raise ValueError(f"No checkpoint found for session {session_id}")

    new_container_id = sandbox.create_session(session.repo_url)
    if checkpoint["workspace_diff"]:
        sandbox.exec(new_container_id, ["sh", "-c", f"echo '{checkpoint['workspace_diff']}' | git apply -"])

    session.container_id = new_container_id
    session.status = "running"
    db.commit()

    return {
        "session_id": session.id,
        "container_id": new_container_id,
        "turn": checkpoint["turn"],
        "conversation": checkpoint["conversation"],
        "memory_pointer": checkpoint["memory_pointer"],
    }
