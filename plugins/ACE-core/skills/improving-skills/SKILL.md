---
name: improving-skills
description: Optimizes a skill by analyzing project conventions and researching best practices. Use when a skill needs quality improvement or updates to current standards.
---

# Improving Skills

Optimize the specified skill through systematic analysis and enhancement.

## Process

### 1. Analyze Current Skill

Read the skill's SKILL.md and all associated files:

```bash
ls -la <skill-path>
cat <skill-path>/SKILL.md
```

Document: purpose, triggers, references, structure.

### 2. Gather Project Conventions

Search the project for implementation patterns:
- Find related code using Grep for skill's domain keywords
- Identify naming conventions, file structures, coding styles

### 3. Research Best Practices

Use WebSearch to find current best practices:

```
Search: "[skill domain] best practices 2025"
Search: "[skill domain] API reference"
```

### 4. Validate Against Standards

Use the `writing-skills` skill to check compliance with standards.

### 5. Check for Shared Conventions

Identify conventions that appear in multiple skills:
- Search other skills for similar guidelines
- If convention is duplicated → use `writing-rules` skill to extract to `.claude/rules/`
- Remove duplicated convention from this skill (rules auto-inject)

### 6. Apply Improvements

Targeted edits:
- Trim verbose explanations
- Add missing triggers to description
- Move detailed content to references/
- Update APIs to current best practices
- Remove conventions that now exist in rules

### 7. Validate Final Result

```bash
python3 skills/write-skill/scripts/validate_skill.py <skill-path>
```
