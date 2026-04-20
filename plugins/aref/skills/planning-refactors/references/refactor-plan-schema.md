# Refactor Plan Schema

`.rcc/{ts}-refactor-plan.md` format. Strict headings so `applying-refactors` can iterate phases.

## Required Structure

### Plan Metadata

```
- plan_ts: YYYYMMDD-HHMMSS
- source_map: .rcc/YYYYMMDD-HHMMSS-refactor-map.md
- targets: [list of paths]
- patterns: [parallel-change, branch-by-abstraction, ...]
- branch_name: refactor/YYYYMMDD-HHMMSS-<scope>
```

### High-Risk Acknowledgements

List of phases marked `high-risk`. Each needs `user_ack: true` before applying.

### Phases

For each phase, use a dedicated subsection `## Phase N`:

```markdown
## Phase 1: <title>

- type: expand | migrate | contract | break-cycle | extract-seam
- files:
  - path/to/file.ts:L10-L45
  - path/to/other.ts:L120-L160
- loc_estimate: 180
- verification:
  - command: "npx vitest run path/to/file.test.ts"
  - expected: "all tests pass"
- characterization_test:
  - status: must-scaffold | existing-sufficient | high-risk
  - target_module: path/to/module
  - strategy: golden-snapshot | assertion-based
- description: |
    <1-3 sentence prose describing the change>
- rollback: git reset --hard <phase-start-sha>
```

## Parse Rules

applying-refactors MUST:
- Read phases in ascending order (`Phase 1`, `Phase 2`, ...)
- Abort if any phase has loc_estimate > 400 and no `oversized: acknowledged` field
- Abort if any phase has `characterization_test.status: high-risk` without matching entry in High-Risk Acknowledgements
- Run verification command after each phase; non-zero exit → stop
