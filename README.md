# Praxis Workshop

Symlink-based workshop system for managing work items through stages.

## Installation

```bash
poetry install
```

## Usage

```bash
# Initialize workshop at $PRAXIS_HOME/_workshop/
steward init

# Intake an item from inbox
steward intake my-idea.md

# Transition item to a new stage
steward stage my-idea backlog
steward stage my-idea forge
```

## Stage Flow

```
Standard:   inbox → intake → backlog → forge → review
Fast-track: intake → forge (skip backlog)
Shelving:   forge ↔ shelf (bidirectional)
Exits:      ANY stage → handoff | archive | trash
```

## Workshop Structure

```
_workshop/
├── 1-inbox/              # Raw capture (gitignored)
├── 3-intake/             # First shaping (gitignored)
├── 5-active/             # Active stages (gitignored)
│   ├── 1-backlog/
│   ├── 3-forge/
│   ├── 5-review/
│   └── 7-shelf/
├── 7-exits/              # Terminal stages (gitignored)
│   ├── 1-handoff/
│   ├── 3-archive/
│   └── 5-trash/
├── 8-epics/              # Ordered batching (gitignored)
└── 9-items/              # Canonical storage (tracked)
```

## Development

```bash
# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Run type checking
poetry run mypy .
```
