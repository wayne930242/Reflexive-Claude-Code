---
name: refactor-skills
description: Analyze and refactor all skills in the project - consolidate, optimize, and remove unnecessary ones
---

# Refactor Skills Command

Systematically analyze all skills in this project and apply refactoring to improve quality, reduce redundancy, and remove unnecessary skills.

## Process

### 1. Discover All Skills

Find all SKILL.md files:

```bash
find . -name "SKILL.md" -type f
```

### 2. Analyze Each Skill

For each skill, evaluate:

**Structure Check**:
- [ ] YAML frontmatter has `name` and `description`
- [ ] Description includes "Use when..." trigger
- [ ] Name matches directory name
- [ ] Body is < 200 lines

**Content Check**:
- [ ] Uses imperative form
- [ ] No "When to use" in body
- [ ] Code examples are concrete
- [ ] No redundant documentation (README, CHANGELOG)

**Redundancy Check**:
- [ ] Not duplicating another skill's functionality
- [ ] References shared content instead of duplicating
- [ ] No unnecessary files in skill directory

### 3. Identify Issues

Classify each skill:

| Status | Action |
|--------|--------|
| **Keep** | Well-structured, unique purpose |
| **Refactor** | Has issues but valuable |
| **Merge** | Overlaps with another skill |
| **Delete** | Redundant or unused |

### 4. Apply Refactoring

**For skills to refactor**:
- Fix description formula: `[What]. [Capabilities]. Use when [triggers].`
- Convert to imperative form
- Move large content to `references/`
- Remove empty directories

**For skills to merge**:
- Identify the primary skill
- Consolidate unique content
- Delete the redundant skill

**For skills to delete**:
- Confirm no dependencies
- Remove entire skill directory

### 5. Validate Results

Run validation on each remaining skill:

```bash
python3 skills/write-skill/scripts/validate_skill.py <skill-path>
```

### 6. Generate Report

Output summary:

```
## Refactoring Summary

### Skills Analyzed: N

### Actions Taken:
- Kept: X skills
- Refactored: Y skills
- Merged: Z skills
- Deleted: W skills

### Changes Made:
- [skill-name]: [action taken]
- ...

### Validation Results:
- All skills pass validation: Yes/No
```

## Guidelines

### Core Principles

1. **Concise is key** - Context window is shared; only add what Claude doesn't know
2. **< 200 lines** - Split to `references/` if approaching limit
3. **Description triggers** - Include "Use when..." in YAML description, not body
4. **Scripts for precision** - Create `.py` scripts for tasks requiring exact format or validation

### Skill Structure

```
.claude/
└── skills/
    └── skill-name/
        ├── SKILL.md           # Required: instructions (<200 lines)
        ├── scripts/           # Optional: executable code
        ├── references/        # Optional: docs loaded on-demand
        └── assets/            # Optional: templates, images
```

### What Makes a Good Skill

- **Focused**: One clear purpose
- **Unique**: Doesn't duplicate other skills
- **Lean**: < 200 lines, uses references for details
- **Discoverable**: Clear "Use when" trigger

### Description Formula

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

### Degrees of Freedom

Choose format based on how critical/fragile the operation is:

| Level | When | Format |
|-------|------|--------|
| High | Multiple valid approaches | Text guidance |
| Medium | Preferred pattern exists | Pseudocode |
| Low | Fragile/critical operations | Specific scripts |

### Progressive Disclosure

Split content when SKILL.md grows:

```markdown
## Quick start
[Essential usage]

## Advanced
- **Forms**: See [forms.md](references/forms.md)
- **API**: See [api.md](references/api.md)
```

Claude loads references only when needed.

### Common Skill Patterns

| Pattern | Use Case | Structure |
|---------|----------|-----------|
| High-Level Guide | Lean SKILL.md with linked docs | SKILL.md → references/*.md |
| Domain-Specific | Multi-domain skills | SKILL.md → references/{domain}.md |
| Framework Variants | Multiple frameworks supported | SKILL.md → references/{framework}.md |
| Script-Heavy | Deterministic reliability needed | SKILL.md → scripts/*.py |

### Anti-Patterns to Fix

- **❌ Deeply nested references** - Keep references one level deep from SKILL.md
- **❌ Duplicate information** - Don't repeat content in SKILL.md and references
- **❌ Verbose explanations** - Claude already knows basics; add only non-obvious knowledge
- **❌ Auxiliary files** - No README.md, CHANGELOG.md in skills

### When to Merge Skills

- Two skills cover similar domains
- Significant content overlap
- One skill is a subset of another

### When to Delete Skills

- No clear use case
- Completely covered by another skill
- Too generic to be useful
- Empty or placeholder content
