---
name: refactoring-skills
description: Analyzes and refactors all skills in the project - consolidate, optimize, and remove unnecessary ones. Use when skills need cleanup or reorganization.
---

# Refactoring Skills

Systematically analyze all skills and apply refactoring for quality and consistency.

## Process

### 1. Invoke Architecture Advisor

Use the `agent-architect` skill to get a holistic view of the current skill landscape.

### 2. Discover All Skills

```bash
find . -name "SKILL.md" -type f
```

### 3. Analyze Each Skill

For each skill, classify:

| Status | Action |
|--------|--------|
| **Keep** | Well-structured, unique purpose |
| **Refactor** | Has issues but valuable |
| **Merge** | Overlaps with another skill |
| **Extract** | Has conventions shared by other skills → move to Rules |
| **Delete** | Redundant or unused |

### 4. Apply Refactoring

**For skills to refactor:**
Use the `writing-skills` skill to guide improvements.

**For skills to merge:**
- Identify the primary skill
- Consolidate unique content
- Delete the redundant skill

**For shared conventions to extract:**
- Use `writing-rules` skill to create rule in `.claude/rules/`
- Remove duplicated convention from each skill

**For skills to delete:**
- Confirm no dependencies
- Remove entire skill directory

### 5. Validate Results

```bash
python3 skills/write-skill/scripts/validate_skill.py <skill-path>
```

### 6. Generate Report

```markdown
## Refactoring Summary

### Skills Analyzed: N

### Actions Taken:
- Kept: X skills
- Refactored: Y skills
- Merged: Z skills
- Extracted to Rules: A conventions
- Deleted: W skills

### Changes Made:
- [skill-name]: [action taken]
```
