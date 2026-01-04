# <TITLE>

## Issue metadata (required)

- **Type:** <type> (e.g., feature, tweak, bug, chore, docs)
- **Priority:** <priority> (P0/P1/P2/P3)
- **Size:** <size> (XS/S/M/L/XL)
- **Maturity:** ready

## Labels to apply (required)

Apply the repo's standard labels for:

- `type:<...>`
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

## Problem

(What’s broken / missing? Why does it matter?)

## Outcome

(What does “done” look like for users?)

## MVP scope

-

## Non-goals

-

## Acceptance criteria

- [ ] Documentation is updated for the future state (README/docs/guides as appropriate)
- [ ] Issue and follow-on changes follow the target repo’s `CONTRIBUTING.md`
- [ ] PR includes clear UAT instructions for reviewers
- [ ] <add feature-specific acceptance criteria here>

## Proposed approach (optional)

-

## Risks / open questions

-

## Links

- Bench WIP folder: `bench/wip/<folder>`
- Related docs/specs:
- Related PRs:

---

## gh command (copy/edit)

1. Copy this file to a temp location (recommended):

- `cp bench/backlog/_templates/github-issue-feature.md .gh-temp/issue.md`

2. Edit `.gh-temp/issue.md`, then create:

- `GH_PAGER=cat gh issue create --repo <owner>/<repo> --title "<TITLE>" --body-file .gh-temp/issue.md`
