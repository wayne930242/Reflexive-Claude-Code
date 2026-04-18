# Analysis Report Template

Write the report to `.rcc/{timestamp}-analysis.md` using this format:

```markdown
# Agent System Analysis Report

**Date:** YYYY-MM-DD HH:MM
**Project:** [project name]

## Project Overview

| Aspect | Finding |
|--------|---------|
| Language(s) | |
| Framework(s) | |
| Project type | |
| CI/CD | |
| Testing | |
| Linting | |
| Team scale | |
| Notable | |

## Component Inventory

| # | Type | Path | Lines | Status |
|---|------|------|-------|--------|
| 1 | CLAUDE.md | ./CLAUDE.md | N | OK/NEEDS_FIX/MISSING |

## Weakness Findings

> Includes pipeline chain-break, state persistence, and mode mismatch checks

### CRITICAL (must fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

### WARNING (should fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

### INFO (nice to fix)

| # | Category | Component | Finding | Suggested Fix |
|---|----------|-----------|---------|---------------|

## Restructuring Recommendations

### Merge Recommendations

| # | ID | Components | Rationale | Priority |
|---|----|------------|-----------|----------|
| 1 | MERGE-1 | | | HIGH/MEDIUM/LOW |

### Extract Recommendations

| # | ID | Source | Extract To | Rationale | Priority |
|---|----|--------|------------|-----------|----------|
| 1 | EXTRACT-1 | | | | HIGH/MEDIUM/LOW |

**Migration table:**

| ID | Before | After | Migration Steps |
|----|--------|-------|-----------------|

### Pipeline Recommendations

| # | ID | Mode | Topology (DOT) | State Persistence | Priority |
|---|----|------|-----------------|-------------------|----------|
| 1 | PIPELINE-1 | | | | HIGH/MEDIUM/LOW |

**Components per pipeline:**

| Pipeline ID | Component | Role | Order |
|-------------|-----------|------|-------|

### Restructuring Summary

| Type | Count | HIGH | MEDIUM | LOW |
|------|-------|------|--------|-----|
| Merge | | | | |
| Extract | | | | |
| Pipeline | | | | |

## Rules Health Summary

| Metric                        | Value | Status |
|-------------------------------|-------|--------|
| CLAUDE.md lines               |       |        |
| Global rules count / lines    |       |        |
| Session-start total lines     |       |        |
| Path-scoped rules             |       |        |
| Rules with procedural content |       |        |
| Dead glob patterns            |       |        |

Status values: `ok`, `>200` (CLAUDE.md lines), `>300` (session total), count for others.

## Summary

- Components scanned: N
- Critical issues: N
- Warnings: N
- Info: N
- Merge recommendations: N
- Extract recommendations: N
- Pipeline recommendations: N
```
