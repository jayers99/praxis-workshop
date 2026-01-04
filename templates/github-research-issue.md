# <TITLE>

## Issue metadata (required)

- **Type:** research
- **Priority:** <priority> (P0/P1/P2/P3)
- **Size:** <size> (XS/S/M/L/XL)
- **Maturity:** ready

## Labels to apply (required)

Apply the repo's standard labels for:

- `type:research`
- `priority:<...>`
- `size:<...>`
- `maturity:ready`

<!--
Maturity levels (aligned with refinement phases):
- raw: Phases 0-1 (intake, initial drafting)
- shaped: Phases 3-4 (expert reviewed via CCR + ASR)
- reviewed: Phases 5-6 (post-CCR loops, implementation-reviewed)
- ready: Phase 9 (execution-ready, GitHub issue created)

Issues created via the Ticket Refinement Runbook should be maturity:ready.
-->

## Research question

(What question are we trying to answer?)

## Why now

(What decision or capability does this research unlock?)

## Scope

### In scope

-

### Out of scope

-

## Method / approach

(How will we answer it? What sources/repos/docs? What validations/reviews?)

## Deliverables

- Primary artifact(s):
- Supporting notes/logs:
- Where it will live (repo path / research-library path):

## Acceptance criteria

- [ ] Research question is answered with evidence and clear caveats
- [ ] Key tradeoffs and uncertainties are explicit
- [ ] Output is linkable and durable (GitHub issue is source of record)
- [ ] Work follows the target repo’s `CONTRIBUTING.md`
- [ ] <add project-specific acceptance criteria here>

## Risks / open questions

-

## Links

- Bench WIP folder: `bench/wip/<folder>`
- Related docs/specs:
- Related issues/PRs:

---

## gh command (copy/edit)

1. Copy this file to a temp location (recommended):

- `cp bench/backlog/_templates/github-research-issue.md .gh-temp/issue.md`

2. Edit `.gh-temp/issue.md`, then create:

- `GH_PAGER=cat gh issue create --repo <owner>/<repo> --title "<TITLE>" --body-file .gh-temp/issue.md`
