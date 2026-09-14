from runbook.context.pipeline import ContextPipeline

def test_assemble_returns_full_file_on_first_use():
    pipeline = ContextPipeline(budget_limit=100000)
    result = pipeline.assemble({"a.py": "print(1)"}, current_task_files={"a.py"}, turn=1)
    assert len(result["entries"]) == 1
    assert "FULL FILE" in result["entries"][0]["content"]

def test_assemble_prunes_and_reports_dropped():
    pipeline = ContextPipeline(budget_limit=100000, max_entries=1)
    files = {"a.py": "print(1)", "b.py": "print(2)"}
    result = pipeline.assemble(files, current_task_files={"a.py"}, turn=1)
    assert len(result["entries"]) == 1
    assert len(result["dropped"]) == 1
    assert result["dropped"][0]["file_path"] == "b.py"
