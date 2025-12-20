# SKILL.md Specification

Version 1.0 (2025-10-16)

## YAML Frontmatter

### Required Fields

| Field | Format | Max Length |
|-------|--------|------------|
| `name` | lowercase, hyphens, numbers | 64 chars |
| `description` | Includes "Use when..." | 1024 chars |

### Optional Fields

| Field | Description |
|-------|-------------|
| `license` | License identifier |
| `allowed-tools` | List of pre-approved tools |
| `metadata` | Key-value pairs for client use |

## Name Requirements

- Must match containing directory name
- Lowercase Unicode alphanumerics and hyphens only
- Examples: `my-skill`, `pdf-editor`, `brand-guidelines`

## Description Formula

```
[What it does]. [Key capabilities]. Use when [specific triggers].
```

**Good**:
```yaml
description: Create semantic git commits. Analyzes staged changes and generates conventional commit messages. Use when committing code or managing git history.
```

**Bad**:
```yaml
description: Helps with git stuff.
```

## Body Guidelines

- Use imperative form ("Run the script" not "You should run")
- Keep under 200 lines
- No "When to use" sections (put in description)
- Link to references/ for detailed content

## Shared Conventions

If a convention appears in multiple skills, extract to `.claude/rules/`:

- Use `write-rules` skill to create shared convention
- Skills automatically inherit rules (auto-injected)
- Keep only skill-specific details in SKILL.md

**Rule of thumb**: Rules = conventions shared across skills.
