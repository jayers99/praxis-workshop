"""Step definitions for list feature tests."""

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
from steward.infrastructure.status_yaml import write_status

scenarios("../features/list.feature")


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

    # Store for later reference
    if "items" not in item_context:
        item_context["items"] = {}
    item_context["items"][slug] = {
        "path": item_path,
        "id": item_id,
        "stage": stage,
    }


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


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(result: dict, text: str) -> None:
    """Verify output contains text."""
    assert text in result["output"].output, (
        f"Expected '{text}' in output. Got: {result['output'].output}"
    )


@then(parsers.parse('the output does not contain "{text}"'))
def check_output_not_contains(result: dict, text: str) -> None:
    """Verify output does not contain text."""
    assert text not in result["output"].output, (
        f"Did not expect '{text}' in output. Got: {result['output'].output}"
    )


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
