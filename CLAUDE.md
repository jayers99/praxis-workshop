# Praxis Workshop — Agent Notes

This is the **steward CLI** for workshop management in Praxis.

## Purpose

- **Code domain extension** providing a symlink-based workshop system
- Manages work items through stages without physical file movement
- Items are stored canonically in `_workshop/9-items/` (git-tracked)
- Stage views are symlinks (gitignored)

## CLI Commands

```bash
steward init              # Initialize _workshop/ at $PRAXIS_HOME
steward intake <file>     # Intake item from inbox to workshop
steward stage <slug> <stage>  # Transition item to new stage
```

## Stage Flow

```
Standard:   inbox → intake → backlog → forge → review
Fast-track: intake → forge (skip backlog)
Shelving:   forge ↔ shelf (bidirectional)
Exits:      ANY stage → handoff | archive | trash
```

## Key Files

| File | Purpose |
|------|---------|
| `src/steward/cli.py` | CLI entry point (Typer) |
| `src/steward/domain/stages.py` | Stage definitions and transitions |
| `src/steward/application/` | Service layer (init, intake, stage) |
| `tests/features/` | Gherkin scenarios |

## Architecture

Follows hexagonal architecture:
- `domain/` — Pure business logic (stages, models, errors)
- `application/` — Use cases (init_service, intake_service, stage_service)
- `infrastructure/` — External concerns (filesystem, YAML, env vars)

## When Working Here

- This is a workspace management tool, not a project template
- Changes affect how work items flow through the workshop
- Stage transitions are validated by the state machine in `stages.py`
- All items live permanently in `9-items/`, stages are just symlink views
