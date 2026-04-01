---
name: refactoring-plugins
description: Use when refactoring, migrating, or auditing a Claude Code plugin package. Use when user says "refactor plugin", "audit plugin", "plugin health check", "migrate plugin structure". Use when plugin structure drifts from official best practices.
---

# Refactoring Plugins

## Overview

**Refactoring plugins IS aligning plugin structure with official Claude Code best practices.**

Run health checks, detect structural drift, fix anti-patterns, and verify the result. Plugins differ from agent systems — they have an official schema (`plugin.json`), auto-discovery conventions, and distribution requirements.

**Core principle:** A plugin that fails health check will fail in production. Measure first, then fix.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Skill Steps
**Handoff:** none
**Next:** none

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[refactoring-plugins] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Identify plugin target
2. Run health check
3. Analyze findings against checklist
4. Present refactoring plan
5. Execute refactoring
6. Verify fixes

Announce: "Created 6 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Identify Plugin Target

**Goal:** Locate the plugin to refactor.

**Discovery order:**
1. User provided a path → use it
2. Current directory has `.claude-plugin/plugin.json` → use it
3. Search for `*/.claude-plugin/plugin.json` in working directory
4. Ask user to specify

**Record:**
- Plugin root path
- Plugin name (from plugin.json or directory name)
- Whether a marketplace.json exists upstream

**Verification:** Have a valid plugin directory with `.claude-plugin/plugin.json`.

## Task 2: Run Health Check

**Goal:** Execute the automated health check script.

**Step 1 — Official CLI validation** (if available):
```bash
claude plugin validate <plugin-path>
```

**Step 2 — Extended health check script:**
```bash
uv run scripts/validate_plugin.py <plugin-path>
# or: python3 scripts/validate_plugin.py <plugin-path>
```

The script integrates `claude plugin validate` automatically and adds extended checks:
- Manifest integrity (JSON syntax, required fields, naming, semver)
- Directory structure (components at root, not inside `.claude-plugin/`)
- Skills quality (frontmatter, gerund naming, line count, mandatory sections, trigger overlap)
- Commands and agents validation
- Path safety (no absolute paths)
- Version sync with marketplace.json

**Capture output:** Save results for analysis in Task 3.

**Verification:** Health check completed with error/warning counts.

## Task 3: Analyze Findings Against Checklist

**Goal:** Deep analysis beyond the automated script.

**CRITICAL:** Read [references/plugin-health-checklist.md](references/plugin-health-checklist.md) for the full checklist.

**The script catches structural issues. Manual analysis catches:**
- Skill trigger overlaps
- Cross-component duplication
- Distribution readiness problems
- README documentation gaps
- Hook safety concerns

**For each finding, record:**
- Category (from checklist)
- Severity: CRITICAL / WARNING / INFO
- Component affected
- Specific issue
- Suggested fix

**Verification:** All 8 checklist categories evaluated.

## Task 4: Present Refactoring Plan

**Goal:** Show user the full findings and planned fixes.

**Present ALL findings with detail.** Do NOT summarize:
1. Health check script output (errors and warnings)
2. Manual analysis findings by severity
3. Planned fix for each issue

**Format:**

| # | Severity | Category | Component | Issue | Planned Fix |
|---|----------|----------|-----------|-------|-------------|

**Ask:** "以上是插件健康檢查結果，要開始修正嗎？"

**Verification:** User has confirmed the refactoring plan.

## Task 5: Execute Refactoring

**Goal:** Fix all confirmed issues.

**CRITICAL:** Read [references/plugin-structure-rules.md](references/plugin-structure-rules.md) for official rules and execution order.

**CRITICAL:** All edits in main conversation. Never delegate writes to subagents.

**Verification:** Each fix applied and individually verified.

## Task 6: Verify Fixes

**Goal:** Re-run health check to confirm all issues resolved.

**Process:**
1. Re-run `validate_plugin.py` on the refactored plugin
2. Verify zero CRITICAL errors
3. Verify all WARNING items from Task 3 are resolved
4. Check no new issues introduced

**If issues remain:** Return to Task 5 and fix.

**Produce final report:**

```markdown
# Plugin Refactoring Report

**Date:** YYYY-MM-DD HH:MM
**Plugin:** [name]

## Changes Made

| # | Component | Change | Rationale |
|---|-----------|--------|-----------|

## Health Check Results

| Metric | Before | After |
|--------|--------|-------|
| Errors | N | 0 |
| Warnings | N | N |
| Skills | N | N |
| Commands | N | N |
| Agents | N | N |
```

**Verification:** Health check passes with zero errors.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "Skip the health check script, I can see the issues"
- "The structure looks fine, skip the checklist"
- "Fix it directly without showing the user"
- "Skip re-verification, I just fixed it"
- "This plugin is simple, skip manual analysis"
- "Move components without checking references"

**All of these mean: You're about to leave a broken plugin. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip health check" | Scripts catch what eyes miss. Always run it. |
| "Structure looks fine" | Anti-patterns hide in config files. Check all 8 categories. |
| "Fix without showing" | User must confirm before structural changes. |
| "Skip re-verification" | Fixes can break other things. Re-run the script. |
| "Simple plugin" | Simple plugins still need valid manifests and naming. |
| "I know the official structure" | Official structure evolves. Verify against the checklist. |

## Flowchart: Plugin Refactoring

```dot
digraph refactor_plugin {
    rankdir=TB;

    start [label="Refactor\nplugin", shape=doublecircle];
    identify [label="Task 1: Identify\nplugin target", shape=box];
    health [label="Task 2: Run\nhealth check", shape=box];
    analyze [label="Task 3: Analyze\nfindings", shape=box];
    present [label="Task 4: Present\nrefactoring plan", shape=box];
    confirm [label="User\nconfirms?", shape=diamond];
    execute [label="Task 5: Execute\nrefactoring", shape=box];
    verify [label="Task 6: Verify\nfixes", shape=box];
    pass [label="Zero\nerrors?", shape=diamond];
    done [label="Refactoring\ncomplete", shape=doublecircle];

    start -> identify;
    identify -> health;
    health -> analyze;
    analyze -> present;
    present -> confirm;
    confirm -> execute [label="yes"];
    confirm -> done [label="no"];
    execute -> verify;
    verify -> pass;
    pass -> done [label="yes"];
    pass -> execute [label="no\nfix more"];
}
```

## References

- [references/plugin-health-checklist.md](references/plugin-health-checklist.md) — Full 8-category plugin health checklist
- Health check script: `scripts/validate_plugin.py` (cross-platform, supports `uv run`)
