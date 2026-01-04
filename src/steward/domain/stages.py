"""Stage definitions and transition rules.

Workshop stages follow this structure:
- 1-inbox: Raw capture (gitignored)
- 3-intake: First shaping (gitignored)
- 5-active/{1-backlog,3-forge,5-review,7-shelf}: Active stages (gitignored)
- 7-exits/{1-handoff,3-archive,5-trash}: Terminal stages (gitignored)
- 9-items: Canonical storage (tracked)

Stage transitions:
- Standard: inbox -> intake -> backlog -> forge -> review
- Fast-track: intake -> forge (skip backlog)
- Defer: forge -> backlog (return to backlog for later)
- Shelving: forge <-> shelf (bidirectional)
- Exits: ANY stage -> handoff | archive | trash
"""

from enum import Enum


class Stage(str, Enum):
    """Workshop stages."""

    INBOX = "inbox"
    INTAKE = "intake"
    BACKLOG = "backlog"
    FORGE = "forge"
    REVIEW = "review"
    SHELF = "shelf"
    HANDOFF = "handoff"
    ARCHIVE = "archive"
    TRASH = "trash"


# Terminal stages - items can transition here from any stage
TERMINAL_STAGES = {Stage.HANDOFF, Stage.ARCHIVE, Stage.TRASH}

# Valid forward transitions (non-terminal)
FORWARD_TRANSITIONS: dict[Stage, set[Stage]] = {
    Stage.INBOX: {Stage.INTAKE},
    Stage.INTAKE: {Stage.BACKLOG, Stage.FORGE},  # forge is fast-track
    Stage.BACKLOG: {Stage.FORGE},
    Stage.FORGE: {Stage.REVIEW, Stage.SHELF, Stage.BACKLOG},  # backlog = defer
    Stage.REVIEW: set(),  # Only terminal exits from review
    Stage.SHELF: {Stage.FORGE},  # Can return to forge
}

# Stage to filesystem path mapping
STAGE_PATHS: dict[Stage, str] = {
    Stage.INBOX: "1-inbox",
    Stage.INTAKE: "3-intake",
    Stage.BACKLOG: "5-active/1-backlog",
    Stage.FORGE: "5-active/3-forge",
    Stage.REVIEW: "5-active/5-review",
    Stage.SHELF: "5-active/7-shelf",
    Stage.HANDOFF: "7-exits/1-handoff",
    Stage.ARCHIVE: "7-exits/3-archive",
    Stage.TRASH: "7-exits/5-trash",
}


def get_stage_path(stage: Stage) -> str:
    """Get the filesystem path for a stage."""
    return STAGE_PATHS[stage]


def is_valid_transition(from_stage: Stage, to_stage: Stage) -> bool:
    """Check if a stage transition is valid.

    Valid transitions:
    - Forward transitions per FORWARD_TRANSITIONS
    - Any stage -> terminal stage (handoff, archive, trash)
    """
    # Terminal stages can be reached from anywhere
    if to_stage in TERMINAL_STAGES:
        return True

    # Check forward transitions
    allowed = FORWARD_TRANSITIONS.get(from_stage, set())
    return to_stage in allowed
