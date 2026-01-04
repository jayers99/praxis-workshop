# Knowledge Gap Flags

**Purpose:** Track conceptual or architectural gaps in Praxis specifications/opinions discovered during refinement spikes.

**When to use:** During any refinement phase (1, 3-4, 6) when a spike reveals that Praxis lacks the conceptual foundation needed to properly specify a feature.

**File naming:** `X.XX-knowledge-gap-flags.md` where `X.XX` matches the phase where gaps are discovered (e.g., `1.35-`, `6.25-`).

---

## Gap Summary

| ID | Gap Description | Size | Route | Status |
|----|-----------------|------|-------|--------|
| G1 | [Short description] | S/M/L | agent/session | pending |

**Size heuristics:**
- **S (Small):** Missing definition, terminology clarification, single-concept gap (~1-2 hours research)
- **M (Medium):** Pattern not documented, cross-cutting concept, multiple related gaps (~4-8 hours research)
- **L (Large):** Architectural foundation missing, requires prior art research, affects multiple features (~12+ hours research)

**Routing:**
- **agent:** Background researcher agent (S gaps, non-blocking)
- **session:** Dedicated PKDP session (M/L gaps, may block refinement)

**Status:**
- **pending:** Gap identified, awaiting spawn decision
- **spawned:** Research initiated (link to PKDP run or agent output)
- **resolved:** Research complete, artifact in research-library
- **deferred:** Explicitly deferred (with rationale)

---

## Gap Details

### G1: [Gap Name]

**Discovered:** Phase X, during [spike name/activity]

**Detection chain:**
- Clarifying question: [What question led to the spike?]
- Spike finding: [What did the spike discover?]
- Gap identified: [What conceptual/architectural gap was revealed?]

**Why it matters:**
- [How does this gap affect the current feature's specification quality?]
- [Would shipping without this research lead to under-specified or inconsistent behavior?]

**Size rationale:** [Why S/M/L?]

**Route recommendation:** [agent/session] because [reason]

**Spawn decision:** [User approved / Deferred / N/A]
- If spawned: [Link to PKDP run folder or agent output file]
- If deferred: [Rationale for deferring]

**Resolution:**
- Research artifact: [Link to research-library/... when complete]
- Summary: [1-2 sentence summary of findings]
- Applied to feature: [How findings informed the feature spec]

---

## Instructions for AI Agent

### Detecting gaps

Watch for these signals during spikes:
1. Spike discovers that a concept referenced in the feature has no Praxis definition
2. Spike finds conflicting or ambiguous guidance in existing specs/opinions
3. Spike reveals an architectural pattern that should exist but doesn't
4. Spike uncovers prior art that contradicts current assumptions

### Flagging gaps

When a gap is detected:
1. Add entry to the summary table
2. Fill out the detail section
3. **STOP and present** to user with routing recommendation
4. Wait for user spawn decision before continuing refinement

### After spawn decision

- If spawned (agent): Continue refinement; agent works in background
- If spawned (session): Pause refinement; create `blocked-by-research.md` stub
- If deferred: Document rationale; continue refinement with explicit assumption

### Integration with feature ticket

When research completes:
1. Update gap status to `resolved`
2. Add research artifact link
3. Reference findings in the feature ticket's "Links" or "Context" section
