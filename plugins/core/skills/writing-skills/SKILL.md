---
name: writing-skills
description: Creates effective Claude Code SKILL.md files following Anthropic's official patterns. Use when writing new skills, improving existing skills, or learning skill best practices.
---

# Writing Skills

Create skills that extend Claude's capabilities with specialized knowledge and workflows.

## Core Principles

1. **Concise is key** - Context window is shared; only add what Claude doesn't know
2. **Progressive disclosure** - SKILL.md is overview; Claude loads `references/` only when needed
3. **Description triggers** - Include "Use when..." in description (third person)
4. **Scripts for precision** - Use scripts for deterministic operations

## Naming Convention

Use **gerund form** (verb + -ing) for skill names:
- `processing-pdfs`, `analyzing-code`, `writing-documentation`
- Must be lowercase, hyphens, numbers only (max 64 chars)
- Avoid: `helper`, `utils`, reserved words (`anthropic`, `claude`)

## Skill Structure

```
skill-name/
├── SKILL.md           # Required (<200 lines)
├── scripts/           # Optional: executable code
└── references/        # Optional: docs loaded on-demand
```

## Creation Workflow

Copy this checklist and track progress:

```
Skill Creation Progress:
- [ ] Step 1: Initialize structure
- [ ] Step 2: Write SKILL.md
- [ ] Step 3: Validate
- [ ] Step 4: Test with real usage
```

### Step 1: Initialize

```bash
python3 scripts/init_skill.py <skill-name>
```

### Step 2: Write SKILL.md

**Frontmatter** (required):
```yaml
---
name: processing-pdfs
description: Extracts text and tables from PDFs. Use when working with PDF files or document extraction.
---
```

**Description formula**: `[What it does]. [Key capabilities]. Use when [triggers].`

Always write in third person. The description is injected into system prompt.

**Body**: Instructions only. Keep lean—move details to `references/`.

### Step 3: Validate

```bash
python3 scripts/validate_skill.py <path/to/skill>
```

### Step 4: Test

Restart Claude Code, trigger naturally (don't mention skill name).

## Degrees of Freedom

| Level | When | Format |
|-------|------|--------|
| High | Multiple valid approaches | Text guidance |
| Medium | Preferred pattern exists | Pseudocode |
| Low | Fragile operations | Specific scripts |

## Feedback Loop Pattern

For quality-critical operations, use validate → fix → repeat:

```markdown
1. Create output
2. Run: `python scripts/validate.py output`
3. If errors, fix and repeat step 2
4. Only proceed when validation passes
```

## MCP Tool References

Always use fully qualified names: `ServerName:tool_name`
- `BigQuery:bigquery_schema`
- `GitHub:create_issue`

## What NOT to Include

- README.md, CHANGELOG.md
- Explanations Claude already knows
- "When to use" in body (put in description)
- Shared conventions → extract to `.claude/rules/`

## References

- [spec.md](references/spec.md) - Frontmatter specification
- [patterns.md](references/patterns.md) - Common patterns
- [examples.md](references/examples.md) - Before/after examples
