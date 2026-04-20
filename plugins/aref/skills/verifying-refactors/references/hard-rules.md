# Hard Rules

Binary pass/fail. Refactor is not done until all pass.

## Rule 1: Zero Cyclic Dependencies

Tool: language-specific dep graph (dependency-cruiser, pydeps, cargo-modules, go-callvis).

Check: JSON output for `cycles: []` or equivalent. Non-empty → FAIL.

## Rule 2: File Line Cap 300

Tool: `wc -l` or language tool.

Check: `find <scope> -type f -name '<ext>' -exec wc -l {} + | awk '$1 > 300 {print}'`

Non-empty output → FAIL. Warn if any file 250-300.

Exclude: test files, generated code (mark via comment `// aref:generated` or `.aref-ignore` file).

## Rule 3: Function Line Cap 50

Tool: radon (Python), lizard (multi-lang), eslint (TS), gocyclo --over 0 with LOC reporter (Go).

Check: any function >50 body lines → FAIL.

## Rule 4: Cognitive Complexity ≤ 15

Tool: lizard, eslint-plugin-sonarjs, clippy::cognitive_complexity, gocognit.

Check: any function > 15 → FAIL.

## Rule 5: Cyclomatic Complexity ≤ 10

Tool: radon, gocyclo, clippy.

Check: any function > 10 → FAIL.

## Rule 6: Single-Entry Per Module

Definition: module root has exactly one entry file (`index.ts`, `__init__.py`, `lib.rs`, `mod.go`, etc.) OR a single public-export barrel.

Check: scan module directories for >1 top-level entry files that are not test / README / config.

Violation → FAIL with list of modules with multiple entries.

## Rule 7: Barrel Only at Module Boundaries

`index.ts` / `__init__.py` re-exports allowed only at module root, not nested folders.

Check: find re-export files at depth >1 within a module → FAIL.

## Exclusions

Files containing comment `// aref:exempt <rule-name> <reason>` on first 10 lines bypass that rule. Exemptions aggregate in verification report.

## Rule Evolution

New rules are added by editing this file plus verifying-refactors SKILL.md task list. Removing a rule requires changelog entry.
