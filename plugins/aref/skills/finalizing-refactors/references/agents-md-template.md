# AGENTS.md Template

Per-subproject AGENTS.md skeleton. Fill placeholders via detection; preserve user content where present.

```markdown
# <Subproject Name>

<!-- aref:generated -->
<!-- Preserve sections outside aref-generated blocks. -->

## Overview

<Three paragraphs from README or manifest description.>

## Build / Test

```bash
<build commands extracted from package.json scripts / Makefile>
```

```bash
<test commands>
```

## Code Style

<Linter name + link to config file. Summarize rules that matter for agents.>

Example:
> Linted with eslint (see `eslint.config.js`). Enforces:
> - `no-unused-vars` (error)
> - `sonarjs/cognitive-complexity` (max 15)
> - Preferred import style: named exports

## Test Conventions

- Framework: <vitest / pytest / cargo test / go test>
- Test file location: <co-located / tests/ / __tests__/>
- Naming: <*.test.ts / test_*.py / *_test.go>
- Snapshots: <path>
- Golden fixtures: <path>

## Architecture

<Excerpt of dep graph from refactor-map. Top-level modules and their relationships.>

```
src/
├── auth/       — Authentication and authorization
├── api/        — HTTP handlers
├── repo/       — Data access
└── util/       — Shared helpers
```

Entry points:
- `src/index.ts` (public API)
- `src/cli.ts` (CLI binary)

## Security

<Placeholder — fill with project-specific guidance>

Examples:
- Never commit `.env*` files
- Secrets go through `<secret-manager>` not environment variables
- User input passes through `<validation-layer>` before persistence

## Refactor History

- Last aref run: `<ts>`, branch `<branch>`
- See `.rcc/archive/<ts>-aref-run/` for details

<!-- aref:end -->
```

## Section Preservation

When an AGENTS.md already exists:
- Preserve user content between `<!-- aref:generated -->` and `<!-- aref:end -->` markers
- Replace content within markers
- Append new sections at end if they didn't exist

First run on existing file: wrap existing content with `<!-- aref:preserved -->` markers, then add aref sections below.
