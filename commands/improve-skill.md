---
name: improve-skill
description: Optimize a skill by analyzing project conventions, researching best practices, and ensuring write-skill compliance
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
# Read skill structure
ls -la $1
cat $1/SKILL.md
```

Document:
- Current purpose and triggers
- Existing references and scripts
- Line count and complexity

### 2. Gather Project Conventions

Search the project for implementation patterns:

- Find related code using Grep for skill's domain keywords
- Identify naming conventions, file structures, coding styles
- Note common patterns in similar files

### 3. Research Best Practices

Use WebSearch to find current best practices:

```
Search: "[skill domain] best practices 2025"
Search: "[skill domain] API reference"
```

Focus on:
- Latest API patterns
- Common pitfalls to avoid
- Performance optimizations

### 4. Validate Against Write-Skill Standards

Check compliance with write-skill requirements:

| Criteria | Check |
|----------|-------|
| Line count | < 200 lines |
| Frontmatter | Has name + description with triggers |
| References | Large content moved to references/ |
| Scripts | Precision tasks use .py scripts |
| No bloat | No README/CHANGELOG/explanations Claude knows |

### 5. Create Improvement Plan

Document findings:

```markdown
## Current State
- [strengths]
- [issues]

## Research Findings
- [best practices discovered]
- [APIs to integrate]

## Proposed Changes
1. [specific change]
2. [specific change]
```

### 6. Apply Improvements

Make targeted edits:

- Trim verbose explanations
- Add missing triggers to description
- Move large content to references/
- Create scripts for precision operations
- Update APIs to current best practices

### 7. Validate Final Result

Use the `write-skill` skill to validate the improved skill meets all standards:

- SKILL.md < 200 lines
- Frontmatter has name + description with triggers
- References load correctly
- Scripts execute without errors

## Example Usage

```
/improve-skill skills/pdf-processor
/improve-skill .claude/skills/api-client
```
