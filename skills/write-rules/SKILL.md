---
name: write-rules
description: Create Claude Code rule files for .claude/rules/. Writes constraints that auto-inject into context. Use when establishing project constraints, migrating constitution, or adding path-specific rules.
---

# Rule Creator

Create modular rule files that auto-inject into Claude's context.

## Core Principles

1. **Rules = Constraints** - What MUST be done, not how to do it
2. **< 50 lines** - Auto-injected = token expensive
3. **Use `paths:`** - Scope rules to relevant files only
4. **No procedures** - How-to belongs in skills

## Initialize Constitution

Run the init script to create base constitution:

```bash
python3 scripts/init_constitution.py
```

Options:
- `--path`, `-p`: Output directory (default: `.claude/rules`)
- `--force`, `-f`: Overwrite existing constitution

## Rule Structure

```
.claude/rules/
├── 00-constitution.md    # Core laws (global)
├── 10-code-style.md      # Style constraints (global)
├── api/
│   └── validation.md     # paths: src/api/**
└── testing/
    └── coverage.md       # paths: **/*.test.ts
```

## File Format

### Global Rule (no paths:)

```yaml
---
# No paths field = applies to ALL contexts
---

# Rule Title

- Constraint 1
- Constraint 2
```

### Path-Scoped Rule

```yaml
---
paths: src/api/**/*.ts
---

# API Rules

- All endpoints MUST validate input
- MUST use standard error format
```

## Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/api/**` | All under src/api/ |
| `*.md` | Markdown in root only |
| `{src,lib}/**/*.ts` | Multiple directories |
| `**/*.{ts,tsx}` | Multiple extensions |

## Constitution Template

Core rules for reflexive workflows:

```markdown
# .claude/rules/00-constitution.md
---
# Global - no paths
---

# Core Laws

## Communication
- Concise, actionable responses
- No unnecessary explanations
- Focus on decisions and next steps

## Skill Discovery
- MUST check available skills before starting work
- Invoke applicable skills to leverage specialized knowledge

## Parallel Processing
- MUST use Task tool to parallelize independent tasks
- Maximize efficiency with concurrent operations

## Reflexive Learning
- When discovering important patterns, remind user to run `/reflect`
- If user strongly requests a new constraint, use `write-rules` skill
```

## Validation Checklist

Before creating a rule:

- [ ] Is this a constraint, not a procedure?
- [ ] < 50 lines?
- [ ] Does it need `paths:` scoping?
- [ ] Not duplicating existing rules?
- [ ] Written in imperative form?

## References

- [paths-patterns.md](references/paths-patterns.md) - Advanced glob patterns
- [examples.md](references/examples.md) - Rule examples by domain
