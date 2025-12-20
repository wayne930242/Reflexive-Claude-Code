---
name: improve-skill
description: Optimize a skill by analyzing project conventions and researching best practices
arguments:
  - name: skill-path
    description: Path to the skill directory to improve (e.g., skills/my-skill)
    required: true
---

# Improve Skill

Optimize the specified skill through systematic analysis and enhancement.

## Process

### 1. Analyze Current Skill

Read the skill's SKILL.md and all associated files:

```bash
ls -la $1
cat $1/SKILL.md
```

Document current state: purpose, triggers, references, line count.

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

Use the `write-skill` skill to check compliance with standards.

### 5. Check for Shared Conventions

Identify conventions that appear in multiple skills:

- Search other skills for similar guidelines
- If convention is duplicated → use `write-rules` skill to extract to `.claude/rules/`
- Remove duplicated convention from this skill (rules auto-inject)

**Rule of thumb**: Rules = conventions shared across skills.

### 6. Apply Improvements

Use the `write-skill` skill to guide targeted edits:

- Trim verbose explanations
- Add missing triggers to description
- Move large content to references/
- Update APIs to current best practices
- Remove conventions that now exist in rules

### 7. Validate Final Result

```bash
python3 skills/write-skill/scripts/validate_skill.py $1
```

## Example Usage

```
/improve-skill skills/pdf-processor
/improve-skill .claude/skills/api-client
```
