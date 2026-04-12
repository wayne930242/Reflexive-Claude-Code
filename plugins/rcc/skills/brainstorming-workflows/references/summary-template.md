# Workflow Summary Template

Write the summary to `docs/agent-system/{timestamp}-workflows.md` using this format:

```markdown
# Workflow Summary

**Date:** YYYY-MM-DD HH:MM

## Analysis Report Reference

- Report path: [path to analysis report if available]
- Key findings addressed: [list of findings selected by user]

## Pipeline Mode Mapping

| Workflow | Mode | Steps | Entry Point | State Management | Script Needed | Rationale |
|----------|------|-------|-------------|------------------|---------------|-----------|

## Pain Points

| Pain Point | Root Cause | Suggested Fix | Component Type | Priority |
|------------|------------|---------------|----------------|----------|

## Routine Tasks

| Task | Frequency | Current Process | Automation Approach | Component Type |
|------|-----------|-----------------|---------------------|----------------|

## Component Recommendations

| Component | Type | Action | Traced To | Priority |
|-----------|------|--------|-----------|----------|
| [name] | rule/hook/skill/agent | create/modify | [pain point or routine task ref] | HIGH/MEDIUM/LOW |

## Workflow Pattern Mapping

| Workflow | Anthropic Pattern | Skill Routing | Complexity Level | Rationale |
|----------|------------------|---------------|-----------------|-----------|

## Human Intervention Points

| Workflow Step | Intervention Type | Trigger Condition | Component Impact |
|---------------|-------------------|-------------------|------------------|
| [step name] | review-checkpoint / confirmation-gate / guardrail-trigger | [when this fires] | [skill handoff / hook / rule affected] |

## Past Failures & Constraints

- [What the user tried before and why it didn't work]
- [Constraints that limit design choices]
```
