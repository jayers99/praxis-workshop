"""Shared test fixtures."""

import os
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def temp_praxis_home() -> Generator[Path, None, None]:
    """Create a temporary PRAXIS_HOME directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir)
        old_env = os.environ.get("PRAXIS_HOME")
        os.environ["PRAXIS_HOME"] = str(path)
        try:
            yield path
        finally:
            if old_env is None:
                os.environ.pop("PRAXIS_HOME", None)
            else:
                os.environ["PRAXIS_HOME"] = old_env


@pytest.fixture
def workshop_path(temp_praxis_home: Path) -> Path:
    """Get the workshop path for tests."""
    return temp_praxis_home / "_workshop"


@pytest.fixture
def initialized_workshop(temp_praxis_home: Path) -> Path:
    """Create an initialized workshop for tests."""
    from steward.application import init_workshop

    return init_workshop()
