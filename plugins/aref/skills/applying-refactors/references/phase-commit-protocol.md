# Phase Commit Protocol

## Commit Message Format

```
refactor(aref): phase N/M — <phase title>

<phase description from plan>

Phase: expand | migrate | contract | break-cycle | extract-seam
Pattern: parallel-change | branch-by-abstraction | strangler-fig
Files: <count>
LOC: +<added>/-<removed>
Verification: <command summary> — <result>
Reviewer: APPROVED after <N> retry

Plan: .rcc/<ts>-refactor-plan.md
```

## Size Enforcement

Before committing, compute actual diff LOC:

```
git diff --cached --numstat | awk '{a+=$1; d+=$2} END {print a+d}'
```

If > 400 and phase not marked `oversized` in plan → abort commit. Ask user to either:
- Split into two phases (go back to planning-refactors)
- Add `oversized: acknowledged` to the plan phase (one-time override)

## Forbidden Commit Flags

- `--amend`
- `--no-verify`
- `-c commit.gpgsign=false`
- `--no-gpg-sign`

## Rollback Command

```
git reset --hard <phase-start-sha>
```

Capture `<phase-start-sha>` as the `HEAD` commit BEFORE beginning phase edits. Record in `.rcc/{ts}-apply-state.yml` so a resumed session can find it.

## apply-state.yml format

```yaml
run_ts: YYYYMMDD-HHMMSS
plan: .rcc/YYYYMMDD-HHMMSS-refactor-plan.md
branch: refactor/...
phases:
  - n: 1
    start_sha: abcdef123
    end_sha: 234567890
    status: committed
  - n: 2
    start_sha: 234567890
    end_sha: null
    status: in-progress
```

Update this file after every phase commit.
