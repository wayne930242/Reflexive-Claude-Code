# Restructuring Guide

After weakness analysis and project scanning, use this guide to produce actionable restructuring recommendations.
Every recommendation must trace back to a specific weakness finding or project characteristic.

---

## 1. Merge Recommendations

### Trigger Conditions

- Two skills have semantically similar descriptions (synonyms, overlapping triggers)
- Two rules target the same glob pattern with overlapping content
- Multiple rules groupable under one theme (e.g., 3 scattered testing rules → 1 unified rule)
- Two skills share >50% task steps

### Output Format

Per merge recommendation:

```markdown
### MERGE-N: Merge A + B → C

**Priority:** HIGH / MEDIUM / LOW
**Type:** Merge
**Affected files:**
- `path/to/A`
- `path/to/B`

**Overlapping content:**
- [bullet list of shared triggers, steps, or rule content]

**Reason:** [traced to specific weakness finding, e.g., "Weakness #4.1: Two skills serve the same purpose — `writing-hooks` and `creating-hooks` both trigger on 'add hook'"]

**Action:** Create `path/to/C`, migrate unique content from both, delete originals.
```

### Priority Guidelines

| Priority | Criteria |
|----------|----------|
| HIGH | Active confusion — users trigger wrong skill, or contradictory rules fire simultaneously |
| MEDIUM | Maintenance burden — changes require updating 2+ files with same content |
| LOW | Cosmetic — minor overlap, no operational impact |

---

## 2. Extract Recommendations

### Trigger Conditions

- CLAUDE.md section > 10 lines → extract to rule file
- CLAUDE.md or rule with procedural content (multi-step instructions) → extract to skill
- Single rule file > 50 lines → split by sub-topic
- Skill SKILL.md > 300 lines → move details to `references/`

### Output Format

Per extract recommendation:

```markdown
### EXTRACT-N: Extract from A → B

**Priority:** HIGH / MEDIUM / LOW
**Type:** Extract
**Migration table:**

| Source File | Line Range | Target Path | Content Summary |
|-------------|------------|-------------|-----------------|
| `CLAUDE.md` | 45-72 | `.claude/rules/deploy-safety.md` | Deploy safety checklist |
| `CLAUDE.md` | 80-95 | `.claude/rules/testing.md` | Test conventions |

**Reason:** [traced to weakness, e.g., "Weakness #8.5: CLAUDE.md contains conventions that belong in rules — deploy section is 28 lines of path-specific conventions"]

**Action:** Create target files, remove extracted lines from source, add reference link if needed.
```

### Extraction Decision Tree

1. Content is path-specific? → Rule with `paths:` frontmatter
2. Content is procedural (do step 1, then step 2)? → Skill
3. Content is declarative but long? → Rule (no paths = global rule)
4. Content is reference data? → Skill `references/` directory

---

## 3. Pipeline Recommendations

Based on project type and detected tooling, recommend missing agent system components.

### Component Triggers

| Project Characteristic | Recommended Component | Type |
|------------------------|-----------------------|------|
| CI/CD config detected | Deployment safety hook | Hook |
| Multiple languages | Language-specific rules per language | Rule |
| Monorepo structure | Path-scoped rules per package | Rule |
| Test framework detected | Test runner PostToolUse hook | Hook |
| Linter config detected | Lint check PostToolUse hook | Hook |
| Team size > 1 | Code review skill or rule | Skill/Rule |

### Pipeline Mode Classification

**owner-pipe:**
- 2-3 steps total
- Single entry point
- One skill dispatches and orchestrates all steps
- Example: `write-skill` → internal steps (scaffold, fill, review)

**chain-pipe:**
- Multiple steps with distinct skills
- Entry varies depending on context
- Independent handoffs between skills
- Example: `analyze` → `brainstorm` → `plan` → `apply` → `review`

### State Persistence Recommendation

| Condition | Recommendation |
|-----------|----------------|
| chain-pipe >= 3 steps | State directory + recommend script management |
| Any pipe with large scope (20+ files, cross-module) | State directory + script |
| Short chain + small scope | File-based state (single markdown report) |
| Scope unclear | Flag: "建議在 brainstorming 階段確認工作範圍" |

### Output Format

Per pipeline recommendation:

```markdown
### PIPELINE-N: [Pipeline Name]

**Priority:** HIGH / MEDIUM / LOW
**Type:** Pipeline
**Mode:** owner-pipe / chain-pipe

**Rationale:** [why this pipeline is needed, traced to project characteristic or weakness]

**Topology:**

​```dot
digraph pipeline {
    rankdir=LR;
    A [label="Step 1", shape=box];
    B [label="Step 2", shape=box];
    A -> B;
}
​```

**State persistence:**
- Path: `.rcc/` or project-specific
- Format: markdown / JSON
- Script management: yes / no / TBD

**Components:**

| # | Component | Type | Exists? | Action |
|---|-----------|------|---------|--------|
| 1 | deploy-safety | Hook | No | Create |
| 2 | test-runner | Hook | No | Create |
| 3 | lint-check | Hook | Yes | OK |
```

---

## 4. Recommendation Summary

After all recommendations are produced, append a count table:

```markdown
## Restructuring Summary

| Type | Count | HIGH | MEDIUM | LOW |
|------|-------|------|--------|-----|
| Merge | N | N | N | N |
| Extract | N | N | N | N |
| Pipeline | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** |
```

### Summary Rules

- Every recommendation must have: type, affected files, reason (traced to weakness or project characteristic), priority.
- HIGH items block normal workflow or cause active errors.
- MEDIUM items cause maintenance burden or degraded experience.
- LOW items are cosmetic or preventive improvements.
- If zero recommendations in a category, still show the row with count 0.

---

## Traceability Requirement

Every recommendation's **Reason** field must reference one of:
- A specific weakness finding ID (e.g., "Weakness #4.1")
- A project characteristic detected during scanning (e.g., "Project uses Go + TypeScript but has no language-specific rules")
- A metric threshold breach (e.g., "CLAUDE.md is 250 lines, exceeds 200-line threshold")

Recommendations without traced reasons are invalid.
Do not generate recommendations from intuition alone.
