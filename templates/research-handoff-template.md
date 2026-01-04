# Research Handoff: [Gap ID] - [Gap Name]

**Purpose:** Document the handoff from completed PKDP research back to the originating feature refinement.

**When to use:** After PKDP research spawned from a knowledge gap is complete and accepted (HVA stage passed).

---

## Handoff Summary

| Field | Value |
|-------|-------|
| **Gap ID** | G[N] from [feature-slug]/X.XX-knowledge-gap-flags.md |
| **Research question** | [The question that was researched] |
| **Research artifact** | `research-library/[path]/[filename].md` |
| **PKDP run** | `[project]/pipeline-runs/[id]/` |
| **Risk tier** | [0-3] |
| **Originating feature** | [Feature ticket URL or WIP folder] |
| **Handoff date** | YYYY-MM-DD |

---

## Key Findings

### Executive Summary

[2-3 sentences summarizing what was learned and its implications for the feature]

### Findings Relevant to Feature

1. **[Finding 1]:** [Brief description]
   - Implication for feature: [How this affects the feature spec]

2. **[Finding 2]:** [Brief description]
   - Implication for feature: [How this affects the feature spec]

### Recommendations

- [ ] [Concrete recommendation 1 for the feature spec]
- [ ] [Concrete recommendation 2 for the feature spec]

### Open Questions (If Any)

- [Question that remains unanswered - may need follow-up research or explicit assumption]

---

## Integration Checklist

Use this checklist when integrating findings into the feature ticket:

- [ ] Read the full research artifact: `research-library/[path]/[filename].md`
- [ ] Update feature ticket with findings reference in "Links" section
- [ ] Apply recommendations to acceptance criteria or implementation notes
- [ ] Document any remaining assumptions explicitly
- [ ] Update knowledge gap status to `resolved` in flags file
- [ ] Close PKDP pipeline run if not already closed

---

## Research Artifact Reference

**Full path:** `research-library/[category]/[filename].md`

**Catalog entry:** (Add to `research-library/CATALOG.md`)

```markdown
| [Title] | [filename].md | [YYYY-MM-DD] | [status] | [Brief description] |
```

---

## Audit Trail

| Date | Action | Actor |
|------|--------|-------|
| [date] | Gap identified | [who/agent] |
| [date] | PKDP initiated (Tier [N]) | [who/agent] |
| [date] | Research completed | [who/agent] |
| [date] | HVA accepted | [who] |
| [date] | Handoff complete | [who/agent] |

---

## Notes

[Any additional context, caveats, or observations about the research process]
