---
description: Start the aref refactoring pipeline on the current project. Triggers analyzing-codebases skill.
argument-hint: "[--dry-run]"
---

# /aref

Start agentic refactoring pipeline on the current project (CWD).

Flow:

1. Detect project languages and monorepo state
2. Run analysis toolchain; produce refactor map
3. User reviews map, approves plan
4. Scaffold characterization tests for hotspots
5. Apply refactors phase-by-phase on `refactor/` branch
6. Verify against hard rules; run mutation testing
7. Write `AGENTS.md` per subproject; suggest rcc handoff

Arguments:
- `--dry-run` — stop after planning; no scaffolding, no edits

## Action

Invoke the `analyzing-codebases` skill. If `$ARGUMENTS` contains `--dry-run`, pass the flag forward.
