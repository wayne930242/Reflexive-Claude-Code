# Mutation Testing

Scope: modules TOUCHED by the current refactor run only. Global mutation is out of scope (cost/benefit wrong for agent-driven runs).

## Deriving Touched Modules

```
git diff --name-only $(git merge-base <branch_name> main)..<branch_name> | \
  xargs -I{} dirname {} | sort -u
```

(`A..B` = commits/files in B not in A. The earlier `A...B` form was reversed and produced an empty set.)

Each directory = one touched module. Run mutation tool per module.

## Per-Language Invocation

### TypeScript / JavaScript — Stryker

```
npx stryker run --mutate <module-glob> --reporters json,progress
```

Config: `stryker.conf.json` at project root (generate if absent).

### Python — mutmut

```
mutmut run --paths-to-mutate <module-path>
mutmut results
```

### Rust — cargo-mutants

```
cargo mutants --file <module>/**/*.rs
```

### Go — go-mutesting

```
go-mutesting <module>/...
```

## Scoring

- Mutation score = killed / total
- Target: ≥80% per module
- Flag as `weak-tests` if <80%
- Record in `.rcc/{ts}-mutation-scores.json`:

```json
{
  "run_ts": "YYYYMMDD-HHMMSS",
  "modules": [
    {
      "path": "src/auth/token",
      "total": 48,
      "killed": 41,
      "score": 0.854,
      "flag": null
    }
  ]
}
```

## Time Budget

Per-module mutation can take minutes to hours. Set a ceiling:

- Per module timeout: 15 minutes
- Total run timeout: 60 minutes
- Exceed → abort mutation for remaining modules, mark skipped in report

## Non-blocking

Mutation score <80% is a WARNING, not FAIL. Hard rules block; mutation advises. User may accept weak-tests and proceed to finalizing.
