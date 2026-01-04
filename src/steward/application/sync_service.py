"""Sync service - regenerate symlinks from status.yaml files."""

from pathlib import Path

from steward.domain.stages import Stage, get_stage_path
from steward.infrastructure.env import get_workshop_path
from steward.infrastructure.filesystem import create_symlink, remove_symlink
from steward.infrastructure.status_yaml import read_status


def get_all_stage_folders(workshop_path: Path) -> list[Path]:
    """Get all stage folders that may contain symlinks."""
    folders = []
    for stage in Stage:
        stage_path = workshop_path / get_stage_path(stage)
        if stage_path.exists():
            folders.append(stage_path)
    return folders


def clear_all_symlinks(workshop_path: Path) -> int:
    """Remove all symlinks from stage folders.

    Returns:
        Number of symlinks removed.
    """
    removed = 0
    for folder in get_all_stage_folders(workshop_path):
        for item in folder.iterdir():
            if item.is_symlink():
                remove_symlink(item)
                removed += 1
    return removed


def sync_workshop() -> tuple[int, int]:
    """Regenerate all symlinks from status.yaml files.

    Returns:
        Tuple of (symlinks_created, orphans_removed).
    """
    workshop_path = get_workshop_path()
    items_path = workshop_path / "9-items"

    if not items_path.exists():
        return (0, 0)

    # First, clear all existing symlinks
    orphans_removed = clear_all_symlinks(workshop_path)

    # Then, create symlinks based on status.yaml
    symlinks_created = 0
    for item_dir in items_path.iterdir():
        if not item_dir.is_dir():
            continue

        # Read status
        try:
            status = read_status(item_dir)
        except FileNotFoundError:
            continue

        # Extract slug from item ID
        item_id = item_dir.name
        if "__" not in item_id:
            continue
        slug = item_id.split("__", 1)[1]

        # Create symlink in appropriate stage folder
        stage = Stage(status.stage)
        stage_path = workshop_path / get_stage_path(stage)
        symlink_path = stage_path / slug
        create_symlink(item_dir, symlink_path)
        symlinks_created += 1

    return (symlinks_created, orphans_removed)
