# CLAUDE.md Examples

## Complete Example

```markdown
# Project Name

One-line description.

## Code Style

- Use 2-space indentation (not 4)
- MUST use ES modules (import/export), NOT CommonJS (require)
- Prefer named exports over default exports

## Workflow

- Run `npm test -- --filter [name]` for single test (NOT full suite)
- MUST typecheck with `npx tsc --noEmit` before committing
- Branch naming: `feature/TICKET-123-description`

## Architecture

- API handlers: `src/api/handlers/`
- Database models: `src/db/models/`
- Shared types: `src/types/` (single source of truth)

## Gotchas

- The `auth` middleware caches tokens for 5 min — restart dev server after changing auth logic
- `npm run build` must complete before `npm run e2e` (no watch mode for e2e)
```

## Good vs Bad Instructions

**Good** (specific, verifiable, non-obvious):
```markdown
- MUST validate all API input with zod schemas before processing
- Run `pytest -x --tb=short` for quick test feedback (NOT `pytest` alone)
```

**Bad** (vague, obvious, unverifiable):
```markdown
- Write clean, maintainable code
- Test your changes thoroughly
- Follow best practices
```
Claude already tries to do these. Document the exceptions.
