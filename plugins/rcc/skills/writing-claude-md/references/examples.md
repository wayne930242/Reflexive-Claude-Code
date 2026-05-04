# CLAUDE.md Examples

## Complete Example

```markdown
# Project Name

One-line description.

## Tooling (non-default)

- Package manager: `bun` (NOT `npm` / `pnpm`) — lockfile is `bun.lock`
- Python deps: `uv sync` (NOT `pip install`); virtualenv lives in `.venv`
- TypeScript types from backend: `bun generate:api` after RSwag spec changes — never hand-edit `lib/api/schemas/backend.generated.ts`

## Workflow

- Single test: `bun run test --filter [name]` — NOT the full `bun test` suite
- MUST typecheck with `bun typecheck` before pushing to `main` (semantic-release tags from `main`; broken builds break releases)
- Branch naming: `feat/`, `fix/`, `refactor/`, `chore/` prefixes only

## Gotchas

- `auth` middleware caches tokens 5 min — restart dev server after editing auth logic
- `bun run build` must complete before `bun run e2e` (no watch mode for e2e)
- Admin subdomain URLs omit `/admin` in browser; `/admin/...` is the internal normalized form (see proxy.ts)
```

Note what's **not** there: no indentation rules (handled by Prettier/eslint), no big directory tree (`ls` shows it), no "follow best practices" platitudes, no restated tech stack from `package.json`. Every line is something Claude could not derive on its own.

## Good vs Bad Instructions

**Good** (specific, verifiable, non-obvious):
```markdown
- MUST validate all API input with zod schemas before processing — auth bypass incident 2025-Q4
- Run `pytest -x --tb=short` for quick test feedback (NOT `pytest` alone — full suite is 12 min)
- Use `bun` not `npm` (project standardized on Bun for install speed; npm leaves stale node_modules)
```

**Bad** (vague, obvious, unverifiable, or derivable):
```markdown
- Write clean, maintainable code
- Test your changes thoroughly
- Follow best practices
- Use 2-space indentation               # ← let Prettier/eslint handle this
- Project uses React + TypeScript        # ← Claude reads package.json
- API handlers live in src/api/handlers  # ← Claude can ls
```
Claude already tries to do the platitudes, and can derive the rest from the codebase. Document only the exceptions and the hidden context.
