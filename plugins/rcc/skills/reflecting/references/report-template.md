# Reflection Report Template

Write the report to `docs/agent-system/{timestamp}-reflection.md` using this format:

~~~markdown
# Reflection Report — {YYYY-MM-DD}

**Date:** YYYY-MM-DD HH:MM
**Session:** [Brief description of work done]

## Session Context

[1-3 sentences describing the work that was done in this session]

## Events

| # | Event | Context | Outcome | Type | Router |
|---|-------|---------|---------|------|--------|
| 1 | [What happened] | [When/where it occurred] | [Result] | correction / error / discovery / repetition | [skill/rule/law/none] |

**Type definitions:**
- **correction** — user corrected the agent's approach or output
- **error** — agent made a mistake, multiple attempts needed
- **discovery** — new insight about the project, domain, or tooling
- **repetition** — same action performed multiple times (automation candidate)

## Learnings

| # | Learning | Evidence | Router | Fix Target | Suggested Component | Rationale |
|---|----------|----------|--------|------------|---------------------|-----------|
| 1 | [Actionable insight] | Event #N | [component that routed behavior] | [where fix lands] | rule / law / skill / hook / doc | [Why, informed by router] |

**Suggested Component guidelines:**
- **law** — immutable, must enforce every response, project-specific
- **rule** — convention, path-scoped, enforceable by file matching
- **skill** — reusable capability, multi-step process
- **hook** — automated quality check, runs on events
- **doc** — reference material, not directly actionable

## Component Recommendations

For each suggested component, provide enough detail for planning-agent-systems to work with:

### Recommendation N: [Component Name]

- **Type:** rule / law / skill / hook / doc
- **Path hint:** [where it would live, e.g., `.claude/rules/api-response-format.md`]
- **Content summary:** [one-paragraph description of what it should contain]
- **Traces to:** Learning #N [, Learning #M]

## Weaknesses Addressed

Map learnings to the 10-category weakness checklist from analyzing-agent-systems where applicable. If a learning does not map to any weakness category, omit it from this section.

| Learning # | Weakness Category | How It Addresses |
|------------|-------------------|------------------|
| N | [category name] | [brief explanation] |
~~~

## Completeness Checklist (for Task 4 review)

Use this checklist to verify the report before routing to planning:

- [ ] Every event has at least one learning
- [ ] Every learning has a suggested component with rationale
- [ ] Every component recommendation has type, path hint, content summary, and traces-to
- [ ] No placeholder text (TBD, TODO, etc.)
- [ ] Session context accurately describes the work done
- [ ] At least 3 events documented (if fewer than 3 significant events occurred, document why)
