# SKILL.md Specification

Version 1.1 (2026-01)

## YAML Frontmatter

### Required Fields

| Field | Format | Max Length |
|-------|--------|------------|
| `name` | gerund form, lowercase, hyphens | 64 chars |
| `description` | Third person, includes "Use when..." | 1024 chars |

### Optional Fields

| Field | Description |
|-------|-------------|
| `license` | License identifier |
| `allowed-tools` | List of pre-approved tools |
| `metadata` | Key-value pairs for client use |

## Name Requirements

Use **gerund form** (verb + -ing):
- `processing-pdfs`, `writing-documentation`, `analyzing-code`
- Lowercase letters, numbers, hyphens only
- Must match containing directory name
- Avoid: `helper`, `utils`, reserved words (`anthropic`, `claude`)

## Description Formula

```
[What it does]. [Key capabilities]. Use when [specific triggers].
```

**Always write in third person** (description is injected into system prompt).

**Good**:
```yaml
description: Creates semantic git commits. Analyzes staged changes and generates conventional commit messages. Use when committing code or managing git history.
```

**Bad**:
```yaml
description: I can help you with git stuff.
description: You can use this for git commits.
```

## Body Guidelines

- Use imperative form ("Run the script" not "You should run")
- SKILL.md is overview; move detailed content to `references/` (loaded on-demand)
- No "When to use" sections (put in description)
- Include workflow checklists for complex tasks

## Shared Conventions

If a convention appears in multiple skills, extract to `.claude/rules/`:

- Use `write-rules` skill to create shared convention
- Skills automatically inherit rules (auto-injected)
- Keep only skill-specific details in SKILL.md

**Rule of thumb**: Rules = conventions shared across skills.
