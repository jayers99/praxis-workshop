"""Status YAML file operations."""

from pathlib import Path

import yaml

from steward.domain.models import Status

STATUS_FILENAME = "status.yaml"


def read_status(item_path: Path) -> Status:
    """Read status.yaml from an item directory.

    Args:
        item_path: Path to the item directory in 9-items/.

    Returns:
        Parsed Status object.

    Raises:
        FileNotFoundError: If status.yaml doesn't exist.
    """
    status_file = item_path / STATUS_FILENAME
    with open(status_file) as f:
        data = yaml.safe_load(f)
    return Status(**data)


def write_status(item_path: Path, status: Status) -> None:
    """Write status.yaml to an item directory.

    Args:
        item_path: Path to the item directory in 9-items/.
        status: Status object to write.
    """
    status_file = item_path / STATUS_FILENAME

    # Ensure directory exists
    item_path.mkdir(parents=True, exist_ok=True)

    # Convert to dict with ISO format timestamps
    data = {
        "stage": status.stage if isinstance(status.stage, str) else status.stage.value,
        "created": status.created.isoformat(),
        "updated": status.updated.isoformat(),
    }

    with open(status_file, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)
