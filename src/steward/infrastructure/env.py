"""Environment variable handling."""

import os
from pathlib import Path

from steward.domain.errors import WorkshopError

PRAXIS_HOME_VAR = "PRAXIS_HOME"
WORKSHOP_DIR = "_workshop"


def get_praxis_home() -> Path:
    """Get PRAXIS_HOME path from environment.

    Raises:
        WorkshopError: If PRAXIS_HOME is not set.
    """
    value = os.environ.get(PRAXIS_HOME_VAR)
    if not value:
        raise WorkshopError(f"{PRAXIS_HOME_VAR} environment variable must be set")

    path = Path(value)
    if not path.is_dir():
        raise WorkshopError(f"{PRAXIS_HOME_VAR} does not exist: {path}")

    return path


def get_workshop_path() -> Path:
    """Get the workshop directory path.

    Returns:
        Path to $PRAXIS_HOME/_workshop/
    """
    return get_praxis_home() / WORKSHOP_DIR
