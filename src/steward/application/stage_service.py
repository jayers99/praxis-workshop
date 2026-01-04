"""Stage service - transition items between stages."""

from datetime import datetime
from pathlib import Path

from steward.domain.errors import (
    AmbiguousItemError,
    InvalidStageTransitionError,
    ItemNotFoundError,
)
from steward.domain.models import Item, Status
from steward.domain.stages import Stage, get_stage_path, is_valid_transition
from steward.infrastructure.env import get_workshop_path
from steward.infrastructure.filesystem import create_symlink, remove_symlink
from steward.infrastructure.status_yaml import read_status, write_status


def find_item_by_slug(slug: str) -> tuple[Path, str]:
    """Find an item by its slug.

    Args:
        slug: The slug to search for (partial match allowed).

    Returns:
        Tuple of (item_path, item_id).

    Raises:
        ItemNotFoundError: If no item matches.
        AmbiguousItemError: If multiple items match.
    """
    workshop_path = get_workshop_path()
    items_path = workshop_path / "9-items"

    if not items_path.exists():
        raise ItemNotFoundError(f"No item found matching: {slug}")

    # Find all matching items
    matches: list[tuple[Path, str]] = []
    for item_dir in items_path.iterdir():
        if not item_dir.is_dir():
            continue
        # Check if slug is in the item ID (after the __ separator)
        item_id = item_dir.name
        if "__" in item_id:
            item_slug = item_id.split("__", 1)[1]
            if slug == item_slug or item_slug.startswith(slug):
                matches.append((item_dir, item_id))

    if not matches:
        raise ItemNotFoundError(f"No item found matching: {slug}")

    if len(matches) > 1:
        match_ids = [m[1] for m in matches]
        raise AmbiguousItemError(
            f"Multiple items match '{slug}'. Please be more specific.",
            matches=match_ids,
        )

    return matches[0]


def get_symlink_path_for_stage(stage: Stage, slug: str) -> Path:
    """Get the symlink path for an item at a given stage."""
    workshop_path = get_workshop_path()
    stage_path = workshop_path / get_stage_path(stage)
    return stage_path / slug


def stage_item(slug: str, to_stage: str) -> Item:
    """Transition an item to a new stage.

    Args:
        slug: Item slug (or partial match).
        to_stage: Target stage name.

    Returns:
        Updated Item.

    Raises:
        ItemNotFoundError: If item not found.
        AmbiguousItemError: If multiple items match slug.
        InvalidStageTransitionError: If transition is not allowed.
    """
    # Validate target stage
    try:
        target_stage = Stage(to_stage)
    except ValueError as e:
        valid_stages = ", ".join(s.value for s in Stage)
        raise InvalidStageTransitionError(
            f"Invalid stage: {to_stage}. Valid stages: {valid_stages}",
            from_stage="unknown",
            to_stage=to_stage,
        ) from e

    # Find the item
    item_path, item_id = find_item_by_slug(slug)
    item_slug = item_id.split("__", 1)[1]

    # Read current status
    status = read_status(item_path)
    current_stage = Stage(status.stage)

    # Validate transition
    if not is_valid_transition(current_stage, target_stage):
        raise InvalidStageTransitionError(
            f"Cannot transition from {current_stage.value} to {target_stage.value}",
            from_stage=current_stage.value,
            to_stage=target_stage.value,
        )

    # Remove old symlink
    old_symlink = get_symlink_path_for_stage(current_stage, item_slug)
    remove_symlink(old_symlink)

    # Update status
    now = datetime.now()
    new_status = Status(
        stage=target_stage,
        created=status.created,
        updated=now,
    )
    write_status(item_path, new_status)

    # Create new symlink
    new_symlink = get_symlink_path_for_stage(target_stage, item_slug)
    create_symlink(item_path, new_symlink)

    return Item(
        id=item_id,
        slug=item_slug,
        status=new_status,
        path=str(item_path),
    )
