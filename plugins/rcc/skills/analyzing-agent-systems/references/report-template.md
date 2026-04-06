# Analysis Report Template

Write the report to `docs/agent-system/{timestamp}-analysis.md` using this format:

```markdown
# Agent System Analysis Report

**Date:** YYYY-MM-DD HH:MM
**Project:** [project name]

## Component Inventory

| # | Type | Path | Lines | Status |
|---|------|------|-------|--------|
| 1 | CLAUDE.md | ./CLAUDE.md | N | OK/NEEDS_FIX/MISSING |

## Weakness Findings

### CRITICAL (must fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

### WARNING (should fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

### INFO (nice to fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

## Summary

- Components scanned: N
- Critical issues: N
- Warnings: N
- Info: N
```
