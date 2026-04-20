# aref Fixture Test Harness

Manual E2E checklist.
Each fixture is an intentionally broken project; running `/aref` against it should produce specific artifacts.
This is the self-test for aref development.

## Prerequisites

- Claude Code with aref plugin installed locally (`claude plugin add ./plugins/aref`)
- All required toolchains installed for the language under test (see language reference)

## Procedure per Fixture

### TypeScript

1. `cd plugins/aref/fixtures/typescript`
2. `npm install`
3. In a Claude Code session, run `/aref`
4. Verify analyzing-codebases produces `.rcc/<ts>-refactor-map.md` with:
   - languages: [typescript]
   - hotspots: at least `src/god-file.ts` in top 3
   - cyclic_dependencies: at least the `cyclic-a` ↔ `cyclic-b` pair
   - AGENTS.md status: absent
5. Verify planning-refactors produces plan with:
   - ≥2 phases: one break-cycle, one god-file split
   - Untested module `src/untested-module.ts` marked must-scaffold
6. Abort before scaffolding (dry-run). Confirm branch not created.

### Python

Same flow, CWD `plugins/aref/fixtures/python`:
- Expect hotspot: `src/god_module.py`
- Expect cycle: `cyclic_a` ↔ `cyclic_b`
- Expect must-scaffold: `src/untested_module.py`

### Rust

Same flow, CWD `plugins/aref/fixtures/rust`.
Note: Rust fixture uses intra-module mutual recursion; verify aref flags it as `high-complexity` rather than cycle (Rust compiler prevents module-level cycles).

### Go

Same flow, CWD `plugins/aref/fixtures/go`.
Similar to Rust, the Go fixture uses same-package mutual recursion.

## Expected Artifacts

Per fixture, `.rcc/` should contain after `/aref` (pre-apply):

```
.rcc/
├── aref-raw/
│   └── <ts>-<lang>-*.json
├── <ts>-refactor-map.md
└── <ts>-refactor-plan.md
```

## Pass Criteria

- All 4 fixtures produce refactor-map.md without errors
- Each map lists the intended hotspots in top 5
- Plan generates ≥2 phases per fixture
- No uncaught exceptions or tool-missing errors (assuming prerequisites installed)

## Failure Triage

Error referencing missing tool → verify prerequisites; update language reference with install command.
Error parsing manifest → fix fixture or parser.
Map missing expected hotspot → check hotspot scoring; might be weights, might be fixture too mild.
