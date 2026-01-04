"""Step definitions for stage feature tests."""

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
from steward.domain.stages import Stage, get_stage_path
from steward.infrastructure.filesystem import create_symlink
from steward.infrastructure.status_yaml import read_status, write_status

scenarios("../features/stage.feature")


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


@given(parsers.parse('an item "{slug}" exists with stage "{stage}"'))
def item_exists_with_stage(
    temp_dir: dict, slug: str, stage: str, item_context: dict
) -> None:
    """Create an item at the specified stage."""
    items_path = temp_dir["path"] / "_workshop" / "9-items"
    now = datetime.now()
    item_id = now.strftime("%Y-%m-%d-%H%M") + f"__{slug}"
    item_path = items_path / item_id
    item_path.mkdir(parents=True, exist_ok=True)

    stage_enum = Stage(stage)
    status = Status(stage=stage_enum, created=now, updated=now)
    write_status(item_path, status)

    # Create symlink in stage folder
    stage_path = temp_dir["path"] / "_workshop" / get_stage_path(stage_enum)
    stage_path.mkdir(parents=True, exist_ok=True)
    symlink_path = stage_path / slug
    create_symlink(item_path, symlink_path)

    item_context["item_path"] = item_path
    item_context["item_id"] = item_id
    item_context["slug"] = slug


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


@then(parsers.parse('the item has stage "{stage}"'))
def check_item_stage(item_context: dict, stage: str) -> None:
    """Verify the item has the expected stage."""
    item_path = item_context["item_path"]
    status = read_status(item_path)
    assert status.stage == stage, f"Expected stage '{stage}', got '{status.stage}'"


@then("no symlink exists in _workshop/3-intake/")
def check_no_intake_symlink(temp_dir: dict, item_context: dict) -> None:
    """Verify no symlink exists in intake stage."""
    intake_path = temp_dir["path"] / "_workshop" / "3-intake"
    slug = item_context["slug"]
    symlink_path = intake_path / slug
    assert not symlink_path.exists(), f"Symlink should not exist: {symlink_path}"


@then(parsers.parse("a symlink exists in {stage_path} pointing to the item"))
def check_symlink_in_stage(
    temp_dir: dict, stage_path: str, item_context: dict
) -> None:
    """Verify symlink exists in the specified stage folder."""
    full_path = temp_dir["path"] / stage_path
    slug = item_context["slug"]
    symlink_path = full_path / slug
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
