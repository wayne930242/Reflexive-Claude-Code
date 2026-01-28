---
name: hunting-skills
description: Searches external skills via claude-skills-mcp, analyzes and rewrites as new project-specific skills. Use when looking for external skill implementations to adapt.
---

# Hunting Skills (Chrollo)

Search and adapt external skills from the Claude Skills library to create new project-specific skills.

## Prerequisites

Requires `claude-skills-mcp` MCP server.

### Installation Check

Verify MCP tools are accessible:
- `mcp__claude-skills__find_helpful_skills`
- `mcp__claude-skills__read_skill_document`
- `mcp__claude-skills__list_skills`

If not available:

```bash
claude mcp add --scope user --transport stdio claude-skills -- uvx claude-skills-mcp
claude mcp list
```

## Process

### 1. Search External Skills

```
mcp__claude-skills__find_helpful_skills(task_description: "<query>")
```

Select the most relevant skills (typically 1-3).

### 2. Read Skill Content

First list available files:

```
mcp__claude-skills__read_skill_document(skill_name: "...")
```

Then retrieve specific files:

```
mcp__claude-skills__read_skill_document(skill_name: "...", document_path: "SKILL.md")
mcp__claude-skills__read_skill_document(skill_name: "...", document_path: "references/*")
```

### 3. Analyze Project Context

```bash
find . -name "SKILL.md" -type f
ls .claude/rules/ 2>/dev/null
cat CLAUDE.md
```

Identify overlaps, project conventions, and gaps.

### 4. Rewrite as New Skill

Use the `writing-skills` skill to create a new skill that:
1. **Adapts** external skill's capabilities to project context
2. **Follows** project conventions (from CLAUDE.md and rules)
3. **Integrates** with existing skills (no duplication)

Key transformations:
- Replace generic examples with project-specific ones
- Add project conventions inline
- Reference existing skills instead of duplicating

### 5. Validate & Update Manifest

```bash
python3 skills/write-skill/scripts/validate_skill.py <new-skill-path>
```

Add the new skill to the appropriate plugin JSON.

## Output Format

```markdown
## Hunting Report

### External Skills Found
- [skill-name]: [relevance] - [description]

### New Skill Created
- Path: skills/[new-skill-name]/
- Based on: [external-skill-name]
- Adaptations: [list of changes]
```
