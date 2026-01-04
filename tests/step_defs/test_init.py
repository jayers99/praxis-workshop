"""Step definitions for init feature tests."""

import os
import tempfile
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from steward.cli import app

scenarios("../features/init.feature")


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a CLI test runner."""
    return CliRunner(mix_stderr=False)


@pytest.fixture
def result() -> dict:
    """Store the CLI result between steps."""
    return {}


@pytest.fixture
def temp_dir() -> dict:
    """Provide temporary directory context."""
    return {"path": None, "old_env": None}


@given("PRAXIS_HOME is set to a valid directory")
def praxis_home_set(temp_dir: dict) -> None:
    """Set up a temporary PRAXIS_HOME."""
    tmpdir = tempfile.mkdtemp()
    temp_dir["path"] = Path(tmpdir)
    temp_dir["old_env"] = os.environ.get("PRAXIS_HOME")
    os.environ["PRAXIS_HOME"] = tmpdir


@given("_workshop/ does not exist")
def workshop_not_exists(temp_dir: dict) -> None:
    """Ensure workshop directory doesn't exist."""
    workshop_path = temp_dir["path"] / "_workshop"
    if workshop_path.exists():
        import shutil

        shutil.rmtree(workshop_path)


@given("_workshop/ already exists")
def workshop_exists(temp_dir: dict) -> None:
    """Create workshop directory."""
    workshop_path = temp_dir["path"] / "_workshop"
    workshop_path.mkdir(parents=True, exist_ok=True)


@given("PRAXIS_HOME environment variable is not set")
def praxis_home_not_set(temp_dir: dict) -> None:
    """Unset PRAXIS_HOME."""
    temp_dir["old_env"] = os.environ.get("PRAXIS_HOME")
    if "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner: CliRunner, result: dict, command: str) -> None:
    """Run a CLI command."""
    import shlex

    args = shlex.split(command)
    # Remove 'steward' from args if present
    if args and args[0] == "steward":
        args = args[1:]
    result["output"] = cli_runner.invoke(app, args)


@then(parsers.parse("the exit code should be {code:d}"))
def check_exit_code(result: dict, code: int) -> None:
    """Verify the exit code."""
    assert result["output"].exit_code == code, (
        f"Expected exit code {code}, got {result['output'].exit_code}. "
        f"Output: {result['output'].output}"
    )


@then(parsers.parse("{path} directory exists"))
def check_directory_exists(temp_dir: dict, path: str) -> None:
    """Verify a directory exists."""
    full_path = temp_dir["path"] / path
    assert full_path.is_dir(), f"Directory not found: {full_path}"


@then(parsers.parse('.gitignore contains "{pattern}" pattern'))
def check_gitignore_pattern(temp_dir: dict, pattern: str) -> None:
    """Verify .gitignore contains a pattern."""
    gitignore_path = temp_dir["path"] / ".gitignore"
    assert gitignore_path.exists(), ".gitignore not found"
    content = gitignore_path.read_text()
    assert pattern in content, f"Pattern '{pattern}' not in .gitignore"


@then(parsers.parse('stderr contains "{text}"'))
def check_stderr_contains(result: dict, text: str) -> None:
    """Verify stderr contains text."""
    stderr = result["output"].stderr or ""
    combined = stderr or result["output"].output
    assert text in combined, f"Expected '{text}' in stderr. Got: {combined}"


@pytest.fixture(autouse=True)
def cleanup_env(temp_dir: dict):
    """Clean up environment after test."""
    yield
    if temp_dir.get("old_env") is not None:
        os.environ["PRAXIS_HOME"] = temp_dir["old_env"]
    elif "PRAXIS_HOME" in os.environ and temp_dir.get("path"):
        del os.environ["PRAXIS_HOME"]
    if temp_dir.get("path") and temp_dir["path"].exists():
        import shutil

        shutil.rmtree(temp_dir["path"])
