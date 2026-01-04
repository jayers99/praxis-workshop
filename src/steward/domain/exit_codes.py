"""Exit codes for CLI commands.

Following Unix conventions:
- 0: Success
- 1: General error
- 2: Misuse of shell command (invalid arguments)
- 64-78: Reserved for application-specific errors (BSD sysexits.h)
"""

from enum import IntEnum


class ExitCode(IntEnum):
    """Standard exit codes for the CLI."""

    SUCCESS = 0
    GENERAL_ERROR = 1
    INVALID_ARGUMENT = 2
    ITEM_NOT_FOUND = 66  # EX_NOINPUT - cannot open input
    WORKSHOP_EXISTS = 73  # EX_CANTCREAT - can't create output
    INVALID_TRANSITION = 65  # EX_DATAERR - input data incorrect
    ENV_ERROR = 78  # EX_CONFIG - configuration error
