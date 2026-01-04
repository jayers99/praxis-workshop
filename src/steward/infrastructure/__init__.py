"""Infrastructure layer - external adapters and implementations."""

from steward.infrastructure.console import get_console, get_error_console
from steward.infrastructure.env import get_praxis_home, get_workshop_path
from steward.infrastructure.filesystem import (
    create_symlink,
    ensure_directory,
    remove_symlink,
)
from steward.infrastructure.slugify import slugify
from steward.infrastructure.status_yaml import read_status, write_status

__all__ = [
    "create_symlink",
    "ensure_directory",
    "get_console",
    "get_error_console",
    "get_praxis_home",
    "get_workshop_path",
    "read_status",
    "remove_symlink",
    "slugify",
    "write_status",
]
