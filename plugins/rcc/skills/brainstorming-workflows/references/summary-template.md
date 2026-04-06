# Workflow Summary Template

Write the summary to `docs/agent-system/{timestamp}-workflows.md` using this format:

```markdown
# Workflow Summary

**Date:** YYYY-MM-DD HH:MM
**Role:** [selected role]

## Core Workflows
1. [Workflow description]
2. [Workflow description]

## Tasks to Automate
- [Task] → suggested component type (hook/skill/rule)

## Weaknesses to Fix (from analysis)
- [Finding] → planned fix

## Conventions to Enforce
- [Convention] → suggested component type (rule/hook)

## Workflow Pattern Mapping
| Workflow | Anthropic Pattern | Skill Routing | Complexity Level | Rationale |
|----------|------------------|---------------|-----------------|-----------|
| [workflow] | Prompt Chaining / Routing / etc. | Tree/Chain/Node/Skill Steps | 1-6 | [why this level] |

## Past Failures & Constraints
- [What the user tried before and why it didn't work]
- [Constraints that limit design choices]

## Component Recommendations
| Component | Action | Rationale |
|-----------|--------|-----------|
| CLAUDE.md | create/modify | [reason] |
| Rule: [name] | create | [reason] |
| Hook: [name] | create | [reason] |
| Skill: [name] | create | [reason] |
```
