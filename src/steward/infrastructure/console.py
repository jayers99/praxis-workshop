"""Console output utilities using Rich."""

import sys

from rich.console import Console

_console: Console | None = None
_error_console: Console | None = None


def get_console() -> Console:
    """Get the stdout console (for data output)."""
    global _console
    if _console is None:
        _console = Console()
    return _console


def get_error_console() -> Console:
    """Get the stderr console (for diagnostics)."""
    global _error_console
    if _error_console is None:
        _error_console = Console(stderr=True)
    return _error_console


def is_tty() -> bool:
    """Check if stdout is a TTY."""
    return sys.stdout.isatty()
