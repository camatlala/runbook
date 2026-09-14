from runbook.llm.base import ToolCall
from runbook.sandbox.docker_manager import SandboxManager

TOOL_SCHEMAS = [
    {"name": "read_file", "description": "Read a file's contents from the sandbox workspace.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "write_file", "description": "Write content to a file in the sandbox workspace.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}},
    {"name": "run_command", "description": "Run a shell command in the sandbox workspace.",
     "input_schema": {"type": "object", "properties": {"command": {"type": "array", "items": {"type": "string"}}}, "required": ["command"]}},
]

def dispatch_tool_call(sandbox: SandboxManager, container_id: str, call: ToolCall) -> str:
    if call.name == "read_file":
        return sandbox.read_file(container_id, call.arguments["path"])

    if call.name == "write_file":
        path = call.arguments["path"]
        content = call.arguments["content"]
        result = sandbox.exec(container_id, ["sh", "-c", f"cat > '{path}' <<'RUNBOOK_EOF'\n{content}\nRUNBOOK_EOF"])
        return "written" if result.exit_code == 0 else f"error: {result.stderr}"

    if call.name == "run_command":
        result = sandbox.exec(container_id, call.arguments["command"], timeout=60)
        return result.stdout if result.exit_code == 0 else f"exit {result.exit_code}: {result.stdout}{result.stderr}"

    raise ValueError(f"Unknown tool: {call.name}")
