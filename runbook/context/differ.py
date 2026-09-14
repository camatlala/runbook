import difflib

def build_diff(old: str | None, new: str) -> str:
    if old is None:
        return f"FULL FILE:\n{new}"
    if old == new:
        return "NO CHANGE"
    diff = difflib.unified_diff(
        old.splitlines(keepends=True), new.splitlines(keepends=True),
        fromfile="before", tofile="after",
    )
    return "".join(diff)
