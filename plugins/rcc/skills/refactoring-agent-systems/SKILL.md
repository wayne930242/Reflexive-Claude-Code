---
name: refactoring-agent-systems
description: Use when reviewing and cleaning up an agent system after creation or modification. Use when user says "review agent system", "cleanup agent system", "refactor agent setup". Use when called by applying-agent-systems.
---

# Refactoring Agent Systems

## Overview

**Refactoring agent systems IS applying clean code principles to agent configurations.**

Re-analyze after changes, compare before/after, fix remaining issues, simplify over-engineering.

**Core principle:** Refactoring without measurement is guessing. Analyze, then change, then verify.

**Violating the letter of the rules is violating the spirit of the rules.**

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[refactoring-agent-systems] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Re-analyze current state
2. Compare with prior analysis
3. Execute refactoring
4. Final verification
5. Produce refactoring report

Announce: "Created 5 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Re-analyze Current State

**Goal:** Run a fresh analysis of the agent system.

**Invoke `analyzing-agent-systems` skill** to produce a new analysis report.

This gives us the "after" snapshot to compare with the "before" analysis (if one exists).

**Verification:** New analysis report exists at `docs/agent-system/{timestamp}-analysis.md`.

## Task 2: Compare With Prior Analysis

**Goal:** Identify what improved, what remains, and what's new.

**If prior analysis exists:**

| Category | Before | After | Status |
|----------|--------|-------|--------|
| [weakness] | CRITICAL | resolved | FIXED |
| [weakness] | WARNING | WARNING | REMAINING |
| [new issue] | — | WARNING | NEW |

**If no prior analysis:** Use the new analysis as baseline. All findings are actionable.

**Verification:** Comparison table complete with clear status for each finding.

## Task 3: Execute Refactoring

**Goal:** Fix remaining and new issues.

**Refactoring actions (in priority order):**

| Issue Type | Action | Method |
|------------|--------|--------|
| Duplicate logic across components | Merge or extract to rule | Main conversation edits |
| Conflicting instructions | Unify or remove one | Main conversation edits |
| Over-engineered component | Simplify (YAGNI) | Main conversation edits |
| Weak skill trigger | Improve description | Main conversation edits |
| Missing isolation | Add `context: fork` to agent | Main conversation edits |
| CLAUDE.md too long | Move content to rules/skills | Main conversation edits |

**CRITICAL:** All edits happen in main conversation. Never delegate refactoring writes to subagents.

**For each refactoring action:**
1. Identify the specific change
2. Make the edit
3. Verify the fix resolves the issue
4. Move to next action

**Verification:** All REMAINING and NEW issues addressed.

## Task 4: Final Verification

**Goal:** Confirm no critical issues remain.

**Run `analyzing-agent-systems` one more time** (lightweight — focus on critical/warning only).

**Pass criteria:**
- Zero CRITICAL issues
- WARNING count decreased or stable
- No new issues introduced by refactoring

**If critical issues remain:** Return to Task 3 and fix.

**Verification:** Analysis shows zero critical issues.

## Task 5: Produce Refactoring Report

**Goal:** Document what was changed and why.

**Write to:** `docs/agent-system/{timestamp}-refactoring-report.md`

**Report format:**

```markdown
# Agent System Refactoring Report

**Date:** YYYY-MM-DD HH:MM

## Changes Made

| # | Component | Change | Rationale |
|---|-----------|--------|-----------|

## Before/After Comparison

| Metric | Before | After |
|--------|--------|-------|
| Components | N | N |
| Critical issues | N | 0 |
| Warnings | N | N |
| Total lines (CLAUDE.md) | N | N |

## Remaining Items (INFO)

- [Low priority items for future consideration]
```

**Verification:** Report accurately reflects all changes.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "Skip re-analysis, I just built this"
- "No need to compare, everything is new"
- "Use a subagent to make the edits"
- "Skip final verification, I just fixed it"
- "The report is busywork"

**All of these mean: You're about to leave mess behind. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip re-analysis" | Building introduces new issues. Always re-analyze. |
| "Skip comparison" | Without before/after, you can't prove improvement. |
| "Subagent edits" | Subagents can't write to `.claude/`. Use main conversation. |
| "Skip verification" | Refactoring can break things. Verify. |
| "Skip report" | Report documents decisions for future maintainers. |

## Flowchart: Agent System Refactoring

```dot
digraph refactor_agent {
    rankdir=TB;

    start [label="Refactor agent\nsystem", shape=doublecircle];
    analyze [label="Task 1: Re-analyze\ncurrent state", shape=box];
    compare [label="Task 2: Compare\nwith prior", shape=box];
    refactor [label="Task 3: Execute\nrefactoring", shape=box];
    verify [label="Task 4: Final\nverification", shape=box];
    clean [label="Zero\ncritical?", shape=diamond];
    report [label="Task 5: Produce\nreport", shape=box];
    done [label="Refactoring complete", shape=doublecircle];

    start -> analyze;
    analyze -> compare;
    compare -> refactor;
    refactor -> verify;
    verify -> clean;
    clean -> report [label="yes"];
    clean -> refactor [label="no\nfix more"];
    report -> done;
}
```
