---
name: refactoring-with-external-skills
description: Refactors existing skills by searching for better external implementations and adapting them. Use when improving skills with external best practices.
---

# Refactoring with External Skills

Improve existing skills by hunting for better external implementations and synthesizing improvements.

## Prerequisites

Requires `claude-skills-mcp` MCP server. See `hunting-skills` skill for installation.

## Process

### 1. Identify Skills to Refactor

If a specific skill path is provided, target that skill. Otherwise, analyze all:

```bash
find . -name "SKILL.md" -type f
```

Assess each skill for:
- Quality issues (unclear, outdated)
- Missing capabilities external skills might have
- Potential for improvement

### 2. Search External Alternatives

For each skill to refactor:

```
mcp__claude-skills__find_helpful_skills(task_description: "[skill's core capability]")
```

### 3. Compare and Analyze

Read promising external skills:

```
mcp__claude-skills__read_skill_document(skill_name: "...", document_path: "SKILL.md")
```

Create comparison matrix:

| Aspect | Current Skill | External Skill | Winner |
|--------|---------------|----------------|--------|
| Clarity | | | |
| Completeness | | | |
| Best practices | | | |
| Integration | | | |

### 4. Synthesize Improvements

Don't replace wholesale. Instead:
1. **Extract** superior patterns from external skill
2. **Preserve** project-specific adaptations
3. **Merge** the best of both
4. **Validate** against project conventions

Use `improving-skills` skill with insights from external skills.

### 5. Validate Results

```bash
python3 skills/write-skill/scripts/validate_skill.py <skill-path>
```

## Difference from refactoring-skills

| Aspect | refactoring-skills | refactoring-with-external-skills |
|--------|-------------------|----------------------------------|
| Focus | Internal consolidation | External improvement |
| Action | Merge/delete redundant | Enhance with external patterns |
| Source | Project skills only | Claude Skills library |
| Goal | Reduce duplication | Increase quality |

Use together: `refactoring-skills` to consolidate, then this skill to enhance.
