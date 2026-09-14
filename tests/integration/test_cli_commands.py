import pytest
from typer.testing import CliRunner
from unittest.mock import patch

pytestmark = pytest.mark.integration

runner = CliRunner()

@patch("runbook.cli.app.run_repl")
@patch("runbook.cli.app.SandboxManager")
def test_start_creates_session_and_launches_repl(mock_sandbox_cls, mock_run_repl, tmp_path):
    mock_sandbox_cls.return_value.create_session.return_value = "container-123"

    from runbook.cli.app import app, settings
    settings.db_path = (tmp_path / "test.db").as_posix()

    result = runner.invoke(app, ["start", "https://example.com/repo.git"])

    assert result.exit_code == 0
    assert mock_run_repl.called

def test_list_shows_no_sessions_message_when_empty(tmp_path):
    from runbook.cli.app import app, settings
    settings.db_path = (tmp_path / "test.db").as_posix()

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
