# `.rcc/config.yml` Schema Reference

Every RCC-enabled project maintains a single `.rcc/config.yml` recording migration state and significant decisions. This config is checked into git.

## Why a config file

- Decisions drift between sessions. The config makes them durable.
- Migration idempotency — re-running `migrating-agent-systems` should detect prior state, not re-do work.
- Cross-skill state — `reflecting`, `refactoring-plugins`, `planning-agent-systems` read this for consistent behavior.

## Schema

```yaml
config_version: 1

migration:
  completed: true | false
  initial_at: "YYYY-MM-DD"          # first migration
  last_at: "YYYY-MM-DD"             # most recent migration
  last_rcc_version: "X.Y.Z"         # rcc plugin version at last migration

release_automation:
  decision: enabled | declined | deferred
  tool: release-please | semantic-release | none
  configured_at: "YYYY-MM-DD"
  notes: "free-form rationale"

settings_scope:
  safety_bypass: path                # where safety rules live
  permissions: path                  # where permission grants live
  hooks: path                        # where hook configs live
  personal_overrides: path           # gitignored per-dev file
  user_global: path                  # ~/.claude/ wide settings

models:
  orchestrator:
    model: claude-opus-4-7 | ...
    effort: low | medium | high | xhigh | max
  implementer:
    model: sonnet | ...
    effort: ...
  reviewer:
    model: sonnet | ...
    effort: ...

artifacts:
  root: .rcc/
  memory: .rcc/memory/
  validation: .rcc/validation/
  archive: .rcc/archive/

decisions_log:
  - date: "YYYY-MM-DD"
    topic: short-topic-slug
    decision: what was decided
    rationale: why
```

## Field semantics

### `migration.completed`
- `false` on first RCC pass; `true` once migration routing succeeds.
- `migrating-agent-systems` Task 1 reads this. If `true` and `last_rcc_version` differs from installed version, offer re-migration.

### `release_automation.decision`
- `enabled` → release-please (or chosen tool) is wired; manual version bumps are anti-pattern.
- `declined` → user explicitly opted out; skip offers in future runs.
- `deferred` → not decided yet; re-ask on next plugin-lifecycle skill run.

### `settings_scope.*`
Canonical answer to "where does this kind of setting go?" Referenced by:
- `writing-rules` when deciding path for safety rules
- `writing-hooks` when registering in settings.json
- `update-config` skill if present

### `models.*`
Informs component generation in `planning-agent-systems` and `writing-subagents` — planners default to these models unless the component explicitly needs different.

### `decisions_log`
Append-only. `reflecting` adds entries when new decisions are made. Do not delete historical entries — outdated decisions still inform context.

## When to read

| Skill | Reads | Writes |
|-------|-------|--------|
| `migrating-agent-systems` | migration, release_automation, settings_scope | migration (creates/updates) |
| `planning-agent-systems` | models, settings_scope | — |
| `writing-rules` | settings_scope | — |
| `writing-hooks` | settings_scope | — |
| `refactoring-plugins` Task 7 | release_automation | release_automation |
| `creating-plugins` Task 6 | — | release_automation (on new plugin) |
| `reflecting` | decisions_log (historical context) | decisions_log (append new) |

## When to create

`migrating-agent-systems` Task 1 checks for `.rcc/config.yml`:
- Not exists → create with defaults during migration, populate based on maturity detection
- Exists → read and use to inform routing

## Gitignore

`.rcc/config.yml` is tracked. `.rcc/memory/` may contain runtime state — if per-machine state accumulates, add to `.gitignore` selectively. `.rcc/` itself is tracked.
