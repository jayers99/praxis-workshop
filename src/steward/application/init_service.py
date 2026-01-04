"""Init service - create workshop directory structure."""

from pathlib import Path

from steward.domain.errors import WorkshopAlreadyExistsError
from steward.infrastructure.env import get_praxis_home, get_workshop_path
from steward.infrastructure.filesystem import ensure_directory

# Directories to create
WORKSHOP_DIRS = [
    "1-inbox",
    "3-intake",
    "5-active/1-backlog",
    "5-active/3-forge",
    "5-active/5-review",
    "5-active/7-shelf",
    "7-exits/1-handoff",
    "7-exits/3-archive",
    "7-exits/5-trash",
    "8-epics",
    "9-items",
]

# .gitignore content for workshop
GITIGNORE_CONTENT = """# Workshop directories (except canonical items)
_workshop/*
!_workshop/9-items/
"""


def init_workshop() -> Path:
    """Initialize the workshop directory structure.

    Creates:
    - All stage directories under _workshop/
    - .gitignore patterns for workshop

    Returns:
        Path to the created workshop directory.

    Raises:
        WorkshopAlreadyExistsError: If _workshop/ already exists.
        WorkshopError: If PRAXIS_HOME is not set.
    """
    workshop_path = get_workshop_path()

    # Check if workshop already exists
    if workshop_path.exists():
        raise WorkshopAlreadyExistsError(
            f"Workshop already exists at {workshop_path}"
        )

    # Create all directories
    for dir_path in WORKSHOP_DIRS:
        ensure_directory(workshop_path / dir_path)

    # Update .gitignore at PRAXIS_HOME level
    praxis_home = get_praxis_home()
    gitignore_path = praxis_home / ".gitignore"

    # Read existing .gitignore if it exists
    existing_content = ""
    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()

    # Add workshop patterns if not present
    if "_workshop/*" not in existing_content:
        with open(gitignore_path, "a") as f:
            if existing_content and not existing_content.endswith("\n"):
                f.write("\n")
            f.write("\n" + GITIGNORE_CONTENT)

    return workshop_path
