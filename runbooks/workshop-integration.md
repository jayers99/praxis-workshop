# Workshop Integration Guide

This guide explains how to use the `steward` CLI with the ticket refinement workflow.

## Workshop Directory Structure

```
_workshop/
├── 1-inbox/              # Raw capture (drop files here)
├── 3-intake/             # First shaping (symlinks)
├── 5-active/             # Active workflow stages (symlinks)
│   ├── 1-backlog/        # Awaiting attention
│   ├── 3-forge/          # Being shaped/refined
│   ├── 5-review/         # At validation gate
│   └── 7-shelf/          # Intentionally paused
├── 7-exits/              # Terminal states (symlinks)
│   ├── 1-handoff/        # Transitioning out
│   ├── 3-archive/        # Completed/closed
│   └── 5-trash/          # Abandoned
└── 9-items/              # Canonical storage (git-tracked)
```

## Workflow Mapping

| Old (bench/) | New (_workshop/) | Steward Command |
|--------------|------------------|-----------------|
| `bench/backlog/<slug>/` | `_workshop/5-active/1-backlog/<slug>` | `steward stage <slug> backlog` |
| `bench/wip/<slug>/` | `_workshop/5-active/3-forge/<slug>` | `steward stage <slug> forge` |
| `bench/shelf/<slug>/` | `_workshop/5-active/7-shelf/<slug>` | `steward stage <slug> shelf` |
| `bench/trash/<slug>/` | `_workshop/7-exits/5-trash/<slug>` | `steward stage <slug> trash` |

## Ticket Refinement with Steward

### Phase 0: Intake

1. Drop raw idea into inbox:
   ```bash
   echo "My feature idea" > $PRAXIS_HOME/_workshop/1-inbox/my-feature.md
   ```

2. Intake into workshop:
   ```bash
   steward intake my-feature.md
   # Creates: _workshop/9-items/YYYY-MM-DD-HHMM__my-feature/
   # Symlink: _workshop/3-intake/my-feature → 9-items/...
   ```

### Phase 1: Draft Nucleus

1. Move to backlog (awaiting refinement):
   ```bash
   steward stage my-feature backlog
   ```

2. Copy nucleus template into item:
   ```bash
   cp $PRAXIS_HOME/extensions/praxis-workshop/templates/issue-nucleus.md \
      $PRAXIS_HOME/_workshop/5-active/1-backlog/my-feature/1.10-issue-nucleus.md
   ```

3. When ready to actively refine, move to forge:
   ```bash
   steward stage my-feature forge
   ```

### Phase 3-6: Expert Review & Refinement

Work happens in `_workshop/5-active/3-forge/my-feature/`:
- `1.10-issue-nucleus.md` → `1.20-issue-draft.md`
- CCR notes: `3.10-ccr-notes.md`
- ASR summary: `4.10-asr-summary.md`
- Reviewed draft: `4.20-issue-draft-reviewed.md`
- Final draft: `7.10-issue-draft.md`

### Phase 9: Create GitHub Issue

After checkpoint 3 acceptance:

1. Create GitHub issue
2. Archive the item:
   ```bash
   steward stage my-feature archive
   ```

### Shelving

To pause work:
```bash
steward stage my-feature shelf
```

To resume:
```bash
steward stage my-feature forge
```

### Abandoning

To abandon:
```bash
steward stage my-feature trash
```

## Path Stability

Workshop items stay at their canonical path:
```
_workshop/9-items/2026-01-04-1530__my-feature/
```

Stage folders contain symlinks, so "Copy Relative Path" in VS Code works:
```
_workshop/5-active/3-forge/my-feature/1.10-issue-nucleus.md
```

This resolves correctly regardless of stage changes.

## Listing Items

```bash
steward list                  # All items
steward list --stage forge    # Items being refined
steward list --stage backlog  # Items awaiting attention
```

## Syncing Symlinks

If symlinks get out of sync with status.yaml:
```bash
steward sync
```
