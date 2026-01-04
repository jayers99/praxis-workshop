"""Domain-level errors.

These errors represent business logic failures that should be
translated to user-friendly messages at the CLI layer.
"""


class WorkshopError(Exception):
    """Base class for workshop errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class WorkshopNotFoundError(WorkshopError):
    """Workshop directory does not exist."""

    pass


class WorkshopAlreadyExistsError(WorkshopError):
    """Workshop directory already exists."""

    pass


class ItemNotFoundError(WorkshopError):
    """Item not found in workshop."""

    pass


class AmbiguousItemError(WorkshopError):
    """Multiple items match the given slug."""

    def __init__(self, message: str, matches: list[str]) -> None:
        super().__init__(message)
        self.matches = matches


class InvalidStageTransitionError(WorkshopError):
    """Invalid stage transition attempted."""

    def __init__(self, message: str, from_stage: str, to_stage: str) -> None:
        super().__init__(message)
        self.from_stage = from_stage
        self.to_stage = to_stage
