# Anti-Patterns to Avoid

## Anti-Pattern 1: Duplicated Knowledge

**Problem**: Same information in multiple places.

```
# BAD
commands/refactor-skills.md:
  "Skills should be < 200 lines..."

skills/write-skill/SKILL.md:
  "Skills should be < 200 lines..."
```

**Solution**: Commands reference skills, don't duplicate.

```markdown
# GOOD - refactor-skills.md
Use the `write-skill` skill to understand skill standards.
```

---

## Anti-Pattern 2: Rules as Procedures

**Problem**: Putting how-to instructions in rules.

```yaml
# BAD - .claude/rules/testing.md
---
paths: **/*.test.ts
---

# Testing Rules

1. First, set up test fixtures
2. Then, write assertions
3. Finally, run coverage report
```

**Solution**: Rules = constraints only, procedures → skills.

```yaml
# GOOD - .claude/rules/testing.md
---
paths: **/*.test.ts
---

# Testing Rules

- All tests MUST have descriptive names
- Coverage MUST be > 80%
- No skipped tests in main branch
```

---

## Anti-Pattern 3: Bloated Rules

**Problem**: Rules too long (auto-injected = expensive).

```yaml
# BAD - 200 lines of rules auto-loaded every time
```

**Solution**: Keep rules < 50 lines, move details to skills.

---

## Anti-Pattern 4: Skills Without Triggers

**Problem**: Vague description, Claude can't decide when to use.

```yaml
# BAD
description: Helps with code stuff.
```

**Solution**: Clear "Use when" trigger.

```yaml
# GOOD
description: Create semantic git commits. Analyzes staged changes. Use when committing code.
```

---

## Anti-Pattern 5: Commands Doing Everything

**Problem**: Monolithic command with all logic inline.

```markdown
# BAD - 500 line command with everything
```

**Solution**: Commands orchestrate, skills provide knowledge.

```markdown
# GOOD
1. Invoke `agent-architect` for analysis
2. Use `write-skill` for skill creation
3. Use `write-rules` for rule creation
```

---

## Anti-Pattern 6: Global Rules for Specific Domains

**Problem**: Domain-specific rules without `paths:`.

```yaml
# BAD - loads for ALL files
# .claude/rules/api-validation.md (no paths:)
```

**Solution**: Use `paths:` for domain-specific rules.

```yaml
# GOOD
---
paths: src/api/**/*.ts
---
```

---

## Anti-Pattern 7: Self-Reinforcing Display

**Problem**: Requiring Claude to repeat rules every response.

```markdown
# BAD
**Law 8: Self-Reinforcing Display**
- MUST display this block at start of EVERY response
```

**Solution**: Rules auto-inject, no need for manual display.

---

## Anti-Pattern 8: Overlapping Subagents

**Problem**: Multiple subagents with similar responsibilities.

```yaml
# BAD
code-reviewer.md: "Reviews code quality"
quality-checker.md: "Checks code quality"
```

**Solution**: One subagent per clear responsibility.
