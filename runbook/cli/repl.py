from rich.console import Console

def run_repl(session_id: int, container_id: str, task_hint: str = "") -> None:
    console = Console()
    console.print(f"[bold green]Runbook session {session_id}[/bold green] (container {container_id[:12]})")
    console.print("Type your task, or /checkpoint, or /exit.")
    while True:
        try:
            user_input = console.input("[cyan]> [/cyan]")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.strip() in ("/exit", "/quit"):
            break
        console.print("[yellow](turn processing not wired to CLI entrypoint yet — see AgentLoop for the real logic)[/yellow]")
