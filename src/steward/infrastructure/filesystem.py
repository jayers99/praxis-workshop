"""Filesystem operations for workshop management."""

import os
from pathlib import Path


def ensure_directory(path: Path) -> None:
    """Create directory and parents if they don't exist."""
    path.mkdir(parents=True, exist_ok=True)


def create_symlink(target: Path, link: Path) -> None:
    """Create a symbolic link.

    Args:
        target: The path the symlink points to (canonical item).
        link: The symlink path to create (in stage folder).
    """
    # Ensure parent directory exists
    link.parent.mkdir(parents=True, exist_ok=True)

    # Calculate relative path from link location to target
    relative_target = Path(os.path.relpath(target, link.parent))

    # Remove existing symlink if present
    if link.is_symlink():
        link.unlink()

    link.symlink_to(relative_target)


def remove_symlink(link: Path) -> None:
    """Remove a symbolic link if it exists."""
    if link.is_symlink():
        link.unlink()


def move_to_items(source: Path, dest: Path) -> None:
    """Move a file or directory to the items folder.

    Args:
        source: Source path (in inbox).
        dest: Destination path (in 9-items/).
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    source.rename(dest)
