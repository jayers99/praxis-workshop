"""Step definitions for wrapper feature tests."""

import os
import subprocess
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/wrapper.feature")


@pytest.fixture
def result() -> dict:
    """Store the result between steps."""
    return {}


@pytest.fixture
def temp_dir() -> dict:
    """Provide temporary directory context."""
    return {"path": None, "old_env": None}


@given("PRAXIS_HOME is set to a valid directory")
def praxis_home_set(temp_dir: dict) -> None:
    """Set up PRAXIS_HOME to the actual workspace."""
    # Use the real PRAXIS_HOME for wrapper test
    praxis_home = os.environ.get("PRAXIS_HOME")
    if not praxis_home:
        # Fall back to parent of extensions directory
        current = Path(__file__).resolve()
        # Navigate up to praxis-workspace
        praxis_home = str(current.parents[4])
    temp_dir["praxis_home"] = praxis_home


@when(parsers.parse('I run the steward wrapper with "{args}"'))
def run_wrapper(temp_dir: dict, result: dict, args: str) -> None:
    """Run the bin/steward wrapper."""
    praxis_home = temp_dir["praxis_home"]
    wrapper_path = Path(praxis_home) / "bin" / "steward"

    if not wrapper_path.exists():
        pytest.skip(f"Wrapper not found at {wrapper_path}")

    env = os.environ.copy()
    env["PRAXIS_HOME"] = praxis_home

    try:
        proc = subprocess.run(
            [str(wrapper_path)] + args.split(),
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )
        result["output"] = proc.stdout + proc.stderr
        result["exit_code"] = proc.returncode
    except subprocess.TimeoutExpired:
        result["output"] = "Timeout"
        result["exit_code"] = 1


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(result: dict, text: str) -> None:
    """Verify output contains text."""
    assert text in result["output"], (
        f"Expected '{text}' in output. Got: {result['output']}"
    )


@then(parsers.parse("the exit code should be {code:d}"))
def check_exit_code(result: dict, code: int) -> None:
    """Verify the exit code."""
    assert result["exit_code"] == code, (
        f"Expected exit code {code}, got {result['exit_code']}. "
        f"Output: {result['output']}"
    )
