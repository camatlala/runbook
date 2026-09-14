from runbook.context.differ import build_diff

def test_first_read_returns_full_file():
    result = build_diff(None, "line1\nline2\n")
    assert result.startswith("FULL FILE:\n")

def test_unchanged_content_returns_no_diff_marker():
    assert build_diff("a\n", "a\n") == "NO CHANGE"

def test_changed_content_returns_unified_diff():
    result = build_diff("line1\nline2\n", "line1\nCHANGED\n")
    assert "-line2" in result
    assert "+CHANGED" in result
