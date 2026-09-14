import typer
from rich.console import Console
from rich.table import Table
from runbook.store.db import get_engine, get_sessionmaker, init_db
from runbook.store.models import Session
from runbook.sandbox.docker_manager import SandboxManager
from runbook.checkpoint.manager import CheckpointManager
from runbook.checkpoint.resume import resume_session
from runbook.cli.repl import run_repl
from runbook.config import settings

app = typer.Typer()
console = Console()

def _get_db():
    engine = get_engine(f"sqlite:///{settings.db_path}")
    init_db(engine)
    SessionLocal = get_sessionmaker(engine)
    return SessionLocal()

@app.command()
def start(repo_url: str):
    db = _get_db()
    session = Session(repo_url=repo_url, status="pending")
    db.add(session)
    db.commit()
    db.refresh(session)

    sandbox = SandboxManager(image=settings.sandbox_image)
    container_id = sandbox.create_session(repo_url)
    session.container_id = container_id
    session.status = "running"
    db.commit()

    console.print(f"Started session {session.id}")
    run_repl(session.id, container_id)

@app.command()
def resume(session_id: int):
    db = _get_db()
    sandbox = SandboxManager(image=settings.sandbox_image)
    restored = resume_session(db, session_id, sandbox)
    console.print(f"Resumed session {restored['session_id']} at turn {restored['turn']}")
    run_repl(restored["session_id"], restored["container_id"])

@app.command(name="list")
def list_sessions():
    db = _get_db()
    sessions = db.query(Session).all()
    if not sessions:
        console.print("No sessions yet.")
        return
    table = Table("ID", "Repo", "Status")
    for s in sessions:
        table.add_row(str(s.id), s.repo_url, s.status)
    console.print(table)

@app.command()
def checkpoints(session_id: int):
    db = _get_db()
    latest = CheckpointManager().latest(db, session_id)
    if latest is None:
        console.print("No checkpoints for this session.")
        return
    console.print(f"Latest checkpoint at turn {latest['turn']}")
