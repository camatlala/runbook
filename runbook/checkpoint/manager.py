import json
from runbook.store.models import Checkpoint

class CheckpointManager:
    def save(self, db, session_id: int, turn: int, conversation: list[dict], workspace_diff: str, memory_pointer: int) -> int:
        checkpoint = Checkpoint(
            session_id=session_id,
            turn=turn,
            conversation_json=json.dumps(conversation),
            workspace_diff=workspace_diff,
            memory_pointer=memory_pointer,
        )
        db.add(checkpoint)
        db.commit()
        db.refresh(checkpoint)
        return checkpoint.id

    def latest(self, db, session_id: int) -> dict | None:
        checkpoint = (
            db.query(Checkpoint)
            .filter(Checkpoint.session_id == session_id)
            .order_by(Checkpoint.turn.desc())
            .first()
        )
        if checkpoint is None:
            return None

        return {
            "turn": checkpoint.turn,
            "conversation": json.loads(checkpoint.conversation_json),
            "workspace_diff": checkpoint.workspace_diff,
            "memory_pointer": checkpoint.memory_pointer,
        }
