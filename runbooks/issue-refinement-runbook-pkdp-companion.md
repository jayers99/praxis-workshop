# PKDP Companion: Refinement-Spawned Knowledge Distillation

**Purpose:** Detailed guidance for detecting knowledge gaps during refinement and spawning PKDP research when needed.

**Companion to:** `issue-refinement-runbook.md` (see "Knowledge Gap Detection" section)

---

## Overview

During ticket refinement, spikes may reveal that Praxis specifications or opinions lack the conceptual foundation needed to properly specify a feature. This companion doc provides the POC process for:

1. **Detecting** knowledge gaps (the "chain model")
2. **Sizing** gaps to determine research approach
3. **Spawning** research (background agent vs. dedicated PKDP session)
4. **Handing off** research results back to the feature

---

## The Chain Model: How Gaps Emerge

Knowledge gaps follow a predictable chain:

```
Clarifying Question → Spike → Knowledge Gap
```

### Chain explanation

1. **Clarifying Question:** During refinement, the agent asks a question to understand the feature better
2. **Spike:** The question triggers a spike to investigate the codebase/specs
3. **Knowledge Gap:** The spike discovers that Praxis lacks needed conceptual foundation

### Detection signals

Watch for these spike outcomes that indicate a knowledge gap:

| Signal | Example | Gap Type |
|--------|---------|----------|
| Missing definition | "The spec doesn't define what 'staged validation' means" | Terminology gap |
| Conflicting guidance | "lifecycle.md says X but opinions say Y" | Consistency gap |
| Missing pattern | "There's no established pattern for multi-stage approval" | Architectural gap |
| Undocumented prior art | "This resembles capability maturity models but we haven't researched that" | Foundation gap |

### What's NOT a knowledge gap

- Questions answerable by reading existing docs more carefully
- Implementation decisions specific to this feature
- User preference questions (ask the user instead)
- Scope decisions (handle in refinement, not research)

---

## Gap Sizing Heuristics

Size determines the research approach. Estimate conservatively.

### Small (S) - Background Agent

**Characteristics:**
- Single concept or definition to clarify
- Answer exists in external sources (not novel research)
- 1-2 hours of research time
- Non-blocking (refinement can continue with assumption)

**Examples:**
- "What's the standard term for this pattern?"
- "How do other frameworks define this concept?"
- "What's the precedent for this in prior art?"

**Route:** Background researcher agent
**Template:** Agent outputs to `bench/inbox-from-subagents/researcher/`

### Medium (M) - Dedicated PKDP Session

**Characteristics:**
- Pattern or cross-cutting concept
- Requires synthesis across multiple sources
- 4-8 hours of research time
- May need CCR (adversarial challenge) to validate

**Examples:**
- "What pattern should govern multi-stage workflows?"
- "How should privacy levels interact with external APIs?"
- "What's the right abstraction for domain-specific audit checks?"

**Route:** Dedicated PKDP session (Tier 1 or 2)
**Impact:** May pause refinement if blocking; may parallel if non-blocking

### Large (L) - Extended PKDP Session

**Characteristics:**
- Architectural foundation missing
- Requires prior art research, synthesis, and validation
- 12+ hours (may span multiple sessions)
- Definitely needs CCR + HVA

**Examples:**
- "What should Praxis's theory of roles be?"
- "How should PKDP relate to the lifecycle model?"
- "What's the governance model for opinions vs. specs?"

**Route:** Dedicated PKDP session (Tier 2 or 3)
**Impact:** Likely blocks refinement until foundation established

---

## Spawning Research

### Decision flow

```
Gap Detected
    ↓
Size Estimate (S/M/L)
    ↓
Route Recommendation (agent/session)
    ↓
Present to User
    ↓
User Decision:
  - SPAWN → Initiate research
  - DEFER → Continue with explicit assumption
  - PROCEED → User judges gap not significant
```

### User presentation format

When presenting a gap to the user:

```
══════════════════════════════════════════════════════════
 KNOWLEDGE GAP DETECTED
══════════════════════════════════════════════════════════

Gap: [Short description]
Discovered: Phase X, during [spike name]

Detection chain:
- Question: [What question led to the spike]
- Spike finding: [What the spike discovered]
- Gap: [The conceptual/architectural gap]

Size estimate: [S/M/L]
Route recommendation: [agent/session]
Rationale: [Why this size and route]

Impact on refinement:
- If spawned: [blocking/non-blocking]
- If deferred: [what assumption would be made]

Your options:
1. SPAWN - Initiate research now
2. DEFER - Continue with assumption (document rationale)
3. PROCEED - Judge gap not significant

══════════════════════════════════════════════════════════
```

### After spawn decision

**If SPAWN (agent):**
1. Create gap flags file (`X.XX-knowledge-gap-flags.md`)
2. Record gap with status `spawned`
3. Dispatch background researcher agent
4. Continue refinement
5. Integrate findings when agent completes

**If SPAWN (session):**
1. Create gap flags file
2. Record gap with status `spawned`
3. Create `blocked-by-research.md` stub if blocking
4. Initiate PKDP session (separate from refinement)
5. Resume refinement after PKDP HVA acceptance

**If DEFER:**
1. Create gap flags file (or update existing)
2. Record gap with status `deferred` and rationale
3. Document explicit assumption in feature ticket
4. Add "Assumption:" prefix to affected acceptance criteria
5. Continue refinement

---

## Handoff: Research Complete

When PKDP research completes:

### Integration steps

1. **Read research artifact** in `research-library/`
2. **Create handoff document** using `research-handoff-template.md`
3. **Update gap flags** - change status to `resolved`
4. **Update feature ticket** with:
   - Link to research artifact in "Links" section
   - Apply findings to affected acceptance criteria
   - Remove any "Assumption:" prefixes that are now resolved
5. **Resume refinement** if was paused

### Handoff document location

Place handoff doc in the feature's working folder:
- `_workshop/5-active/3-forge/<slug>/X.XX-research-handoff-<gap-id>.md`

---

## Scope Creep Prevention

### Guardrails

1. **One gap limit (POC):** For this POC, limit to one gap per refinement session. Queue additional gaps as backlog items.

2. **Timebox research:**
   - Small: 2 hours max
   - Medium: 8 hours max
   - Large: Explicit timebox agreed with user

3. **Research stays non-decisional:** PKDP output is knowledge, not commitments. The feature ticket makes decisions based on research.

4. **Deferred is valid:** Not every gap needs immediate research. Explicit assumptions are acceptable.

### When to escalate

Escalate to user if:
- Multiple L-size gaps detected in single refinement
- Gap appears to require fundamental Praxis changes
- Research timebox exceeded without clear resolution
- Gaps cascade (researching one reveals more)

---

## Artifact Reference

### Files used

| File | Purpose | Location |
|------|---------|----------|
| `X.XX-knowledge-gap-flags.md` | Track detected gaps | WIP folder |
| `X.XX-research-handoff-<gap-id>.md` | Document research handoff | WIP folder |
| `research-library/.../[artifact].md` | Cataloged research output | research-library |

### Templates

- `knowledge-gap-flags-template.md` - Gap tracking format
- `research-handoff-template.md` - Handoff documentation format

---

## POC Success Criteria

This POC is successful when:

- [ ] At least 1 gap identified during real feature refinement
- [ ] Gap flagged using the template artifact
- [ ] Research spawned (agent or session based on size)
- [ ] Research completed and cataloged in research-library
- [ ] Research artifact referenced in feature ticket
- [ ] Learnings captured for runbook improvement

---

## Future Considerations (Out of Scope for POC)

- Automated gap detection (AI pattern recognition)
- Multi-agent orchestration for parallel research
- Gap dependency tracking across features
- Research velocity metrics
