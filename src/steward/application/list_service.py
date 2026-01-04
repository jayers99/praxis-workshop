"""List service - enumerate items in workshop."""

from steward.domain.models import Item
from steward.domain.stages import Stage
from steward.infrastructure.env import get_workshop_path
from steward.infrastructure.status_yaml import read_status


def list_items(stage_filter: str | None = None) -> list[Item]:
    """List all items in the workshop.

    Args:
        stage_filter: Optional stage name to filter by.

    Returns:
        List of Item objects.
    """
    workshop_path = get_workshop_path()
    items_path = workshop_path / "9-items"

    if not items_path.exists():
        return []

    # Validate stage filter if provided
    filter_stage: Stage | None = None
    if stage_filter:
        filter_stage = Stage(stage_filter)

    items: list[Item] = []
    for item_dir in sorted(items_path.iterdir()):
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

        # Apply filter
        if filter_stage and status.stage != filter_stage.value:
            continue

        items.append(
            Item(
                id=item_id,
                slug=slug,
                status=status,
                path=str(item_dir),
            )
        )

    return items
