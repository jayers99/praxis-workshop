"""Step definitions for intake feature tests."""

import os
import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from steward.application import init_workshop
from steward.cli import app
from steward.domain.models import Status
from steward.domain.stages import Stage
from steward.infrastructure.status_yaml import read_status, write_status

scenarios("../features/intake.feature")


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


@pytest.fixture
def item_context() -> dict:
    """Store item context between steps."""
    return {}


@given("an initialized workshop")
def initialized_workshop(temp_dir: dict) -> None:
    """Set up an initialized workshop."""
    tmpdir = tempfile.mkdtemp()
    temp_dir["path"] = Path(tmpdir)
    temp_dir["old_env"] = os.environ.get("PRAXIS_HOME")
    os.environ["PRAXIS_HOME"] = tmpdir
    init_workshop()


@given(parsers.parse('a file "{filename}" exists in _workshop/1-inbox/'))
def file_in_inbox(temp_dir: dict, filename: str) -> None:
    """Create a file in inbox."""
    inbox_path = temp_dir["path"] / "_workshop" / "1-inbox"
    inbox_path.mkdir(parents=True, exist_ok=True)
    file_path = inbox_path / filename
    file_path.write_text("Test content")


@given(parsers.parse('a folder "{foldername}" exists in _workshop/1-inbox/'))
def folder_in_inbox(temp_dir: dict, foldername: str) -> None:
    """Create a folder in inbox."""
    inbox_path = temp_dir["path"] / "_workshop" / "1-inbox"
    folder_path = inbox_path / foldername.rstrip("/")
    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / "README.md").write_text("Test content")


@given(parsers.parse('an existing item with slug "{slug}"'))
def existing_item(temp_dir: dict, slug: str, item_context: dict) -> None:
    """Create an existing item."""
    items_path = temp_dir["path"] / "_workshop" / "9-items"
    now = datetime.now()
    item_id = now.strftime("%Y-%m-%d-%H%M") + f"__{slug}"
    item_path = items_path / item_id
    item_path.mkdir(parents=True, exist_ok=True)
    status = Status(stage=Stage.INTAKE, created=now, updated=now)
    write_status(item_path, status)
    item_context["existing_id"] = item_id


@when(parsers.parse('I run "{command}"'))
def run_command(cli_runner: CliRunner, result: dict, command: str) -> None:
    """Run a CLI command."""
    import shlex

    args = shlex.split(command)
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


@then(parsers.parse(
    'an item directory exists in _workshop/9-items/ with slug "{slug}"'
))
def check_item_exists(temp_dir: dict, slug: str, item_context: dict) -> None:
    """Verify an item directory exists with the given slug."""
    items_path = temp_dir["path"] / "_workshop" / "9-items"
    matches = [d for d in items_path.iterdir() if d.is_dir() and slug in d.name]
    assert len(matches) >= 1, f"No item found with slug '{slug}'"
    item_context["item_path"] = matches[0]
    item_context["slug"] = slug


@then(parsers.parse('the item contains status.yaml with stage "{stage}"'))
def check_status_stage(item_context: dict, stage: str) -> None:
    """Verify status.yaml contains the expected stage."""
    item_path = item_context["item_path"]
    status = read_status(item_path)
    assert status.stage == stage, f"Expected stage '{stage}', got '{status.stage}'"


@then("a symlink exists in _workshop/3-intake/ pointing to the item")
def check_intake_symlink(temp_dir: dict, item_context: dict) -> None:
    """Verify symlink exists in intake stage."""
    intake_path = temp_dir["path"] / "_workshop" / "3-intake"
    slug = item_context["slug"]
    symlink_path = intake_path / slug
    assert symlink_path.is_symlink(), f"Symlink not found: {symlink_path}"


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
