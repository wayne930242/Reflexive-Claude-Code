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
- [ ] Body is < 500 lines

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

### What Makes a Good Skill

- **Focused**: One clear purpose
- **Unique**: Doesn't duplicate other skills
- **Lean**: < 500 lines, uses references for details
- **Discoverable**: Clear "Use when" trigger

### When to Merge Skills

- Two skills cover similar domains
- Significant content overlap
- One skill is a subset of another

### When to Delete Skills

- No clear use case
- Completely covered by another skill
- Too generic to be useful
- Empty or placeholder content
