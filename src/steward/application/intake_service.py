"""Intake service - move or copy items from inbox to workshop."""

import shutil
from datetime import datetime
from pathlib import Path

from steward.domain.errors import ItemNotFoundError
from steward.domain.models import Item, Status
from steward.domain.stages import Stage, get_stage_path
from steward.infrastructure.env import get_workshop_path
from steward.infrastructure.filesystem import create_symlink, ensure_directory
from steward.infrastructure.slugify import slugify
from steward.infrastructure.status_yaml import write_status


def generate_item_id(slug: str, timestamp: datetime | None = None) -> str:
    """Generate an item ID in format YYYY-MM-DD-HHMM__slug."""
    if timestamp is None:
        timestamp = datetime.now()
    date_part = timestamp.strftime("%Y-%m-%d-%H%M")
    return f"{date_part}__{slug}"


def find_unique_id(items_path: Path, base_slug: str, timestamp: datetime) -> str:
    """Find a unique item ID, handling collisions."""
    base_id = generate_item_id(base_slug, timestamp)

    # Check if ID already exists
    if not (items_path / base_id).exists():
        return base_id

    # Handle collision by appending suffix
    suffix = 2
    while True:
        suffixed_slug = f"{base_slug}-{suffix}"
        item_id = generate_item_id(suffixed_slug, timestamp)
        if not (items_path / item_id).exists():
            return item_id
        suffix += 1


def intake_item(
    source_name: str,
    custom_slug: str | None = None,
    move: bool = False,
) -> Item:
    """Intake an item from inbox to workshop.

    Args:
        source_name: Name of file/folder in inbox.
        custom_slug: Optional custom slug (otherwise derived from source_name).
        move: If True, move the source. If False (default), copy it.

    Returns:
        The created Item.

    Raises:
        ItemNotFoundError: If source doesn't exist in inbox.
    """
    workshop_path = get_workshop_path()
    inbox_path = workshop_path / "1-inbox"
    items_path = workshop_path / "9-items"
    intake_stage_path = workshop_path / get_stage_path(Stage.INTAKE)

    # Find source in inbox
    source_path = inbox_path / source_name
    if not source_path.exists():
        raise ItemNotFoundError(f"not found in inbox: {source_name}")

    # Generate slug
    slug = custom_slug if custom_slug else slugify(source_name)

    # Generate unique item ID
    now = datetime.now()
    item_id = find_unique_id(items_path, slug, now)

    # Determine final slug from ID (in case of collision)
    final_slug = item_id.split("__", 1)[1]

    # Create item directory
    item_path = items_path / item_id
    ensure_directory(item_path)

    # Copy or move source into item directory
    dest_path = item_path / source_path.name
    if move:
        # Move: rename the source to destination
        source_path.rename(dest_path)
    else:
        # Copy: preserve source in inbox
        if source_path.is_dir():
            shutil.copytree(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)

    # Create status.yaml
    status = Status(stage=Stage.INTAKE, created=now, updated=now)
    write_status(item_path, status)

    # Create symlink in intake stage
    symlink_path = intake_stage_path / final_slug
    create_symlink(item_path, symlink_path)

    return Item(
        id=item_id,
        slug=final_slug,
        status=status,
        path=str(item_path),
    )
