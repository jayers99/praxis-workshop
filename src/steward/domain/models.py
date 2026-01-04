"""Domain models for workshop items."""

from datetime import datetime

from pydantic import BaseModel, Field

from steward.domain.stages import Stage


class Status(BaseModel):
    """Item status stored in status.yaml."""

    stage: Stage
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)

    model_config = {"use_enum_values": True}


class Item(BaseModel):
    """A workshop item."""

    id: str  # Format: YYYY-MM-DD-HHMM__slug
    slug: str
    status: Status
    path: str  # Canonical path in 9-items/

    @property
    def created(self) -> datetime:
        """Item creation timestamp."""
        return self.status.created

    @property
    def stage(self) -> Stage:
        """Current stage."""
        return Stage(self.status.stage)
