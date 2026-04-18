# Component Plan Template

Write the plan to `.rcc/{timestamp}-plan.md` using this format:

```markdown
# Agent System Component Plan

**Date:** YYYY-MM-DD HH:MM
**Based on:** [analysis report path] + [workflow summary path]

## Architecture Flowchart

[DOT flowchart from Task 2 — shows entry points, routing, workflows, data flow]

## Workflow Pattern Mapping

| Workflow | Anthropic Pattern | Rationale |
|----------|------------------|-----------|
| [name] | Prompt Chaining / Routing / Parallelization / etc. | [why this pattern fits] |

## Dependency Graph & Phases

| Component | Depends On | Depended By | Phase | Core/Enhancement |
|-----------|-----------|-------------|-------|-----------------|
| [name] | [deps] | [dependents] | N | core/enhancement |

## Execution Order

Phase-driven (components within a phase can be built in parallel):
- **Phase 1 (foundation):** [core components with no dependencies]
- **Phase 2 (conventions):** [components depending on Phase 1]
- **Phase 3 (capabilities):** [components depending on Phase 2]

## Components

### 1. CLAUDE.md
- **Action:** create / modify
- **Key content:** [bullet list of what to include]
- **Writing skill:** `writing-claude-md`
- **Traces to:** [workflow/weakness references]

### 2. Rule: [name]
- **Action:** create
- **Paths:** `[glob pattern]`
- **Key constraints:** [bullet list]
- **Writing skill:** `writing-rules`
- **Traces to:** [workflow/weakness references]

[...repeat for each component...]

## Expected Fixes
| Weakness | Component | How It Fixes |
|----------|-----------|-------------|
```
