# Refactor Patterns

## Parallel Change (Expand-Migrate-Contract)

Fowler's canonical pattern. Three phases, each deployable:

- **Expand** — add new code path alongside old. Both work.
- **Migrate** — update call sites from old to new, one slice at a time.
- **Contract** — remove old code once no call sites remain.

Use for: renames, signature changes, data format migrations, type narrowing.

Verification per phase: full test suite green.

## Branch by Abstraction

Use for: replacing an implementation behind an interface.

- **Phase 1 — Extract seam**: introduce interface/abstract class; current impl becomes one implementation.
- **Phase 2 — Introduce new impl**: second implementation of the interface.
- **Phase 3 — Migrate callers**: callers use interface, not concrete class.
- **Phase 4 — Switch default**: new impl becomes default.
- **Phase 5 — Contract**: remove old impl once confirmed unused.

Use for: swapping ORM, HTTP client, test framework migration, state-store replacement.

## Strangler Fig

Use for: replacing a whole component or subsystem.

- Wrap the legacy component behind a router/facade.
- New implementation intercepts incrementally more calls.
- Legacy retires when zero traffic reaches it.

Rarely applicable at file scope. Surface when plan targets a module/package.

## Pattern Selection Matrix

| Situation | Pattern |
|-----------|---------|
| Rename function used in many places | Parallel Change |
| Change function signature | Parallel Change |
| Swap logger/HTTP client | Branch by Abstraction |
| Replace ORM entirely | Branch by Abstraction |
| Replace whole module/package | Strangler Fig |
| Break cyclic dep | Extract seam (precursor to Branch by Abstraction) |
| Extract shared util | Parallel Change with single-phase extract |

## Anti-patterns

- Starting with Contract (removing old first) → breaks at runtime.
- Combining Expand + Migrate → cannot rollback Migrate alone.
- Skipping Abstraction phase in BBA → callers tightly couple to new impl.
