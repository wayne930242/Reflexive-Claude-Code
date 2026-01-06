---
name: rcc:chrollo
description: Search external skills via claude-skills-mcp, analyze and rewrite as new project-specific skills
arguments:
  - name: query
    description: Search query for finding relevant skills (e.g., "code review", "testing", "documentation")
    required: true
---

# Chrollo - Skill Hunter

Search and adapt external skills from the Claude Skills library to create new project-specific skills.

## Prerequisites

This command requires the `claude-skills-mcp` MCP server to be installed.

### Installation Check

First, verify if the MCP tools are available:

```
Check if these MCP tools are accessible:
- find_helpful_skills
- read_skill_document
- list_skills
```

If not available, guide the user to install globally:

```bash
# Install to user scope (global)
claude mcp add --scope user --transport stdio claude-skills -- uvx claude-skills-mcp

# Verify installation
claude mcp list
```

## Process

### 1. Search External Skills

Use the MCP tool to find relevant skills:

```
find_helpful_skills(query: "{query}")
```

Review the results and select the most relevant skills (typically 1-3).

### 2. Read Skill Content

For each selected skill, first list all available files:

```
read_skill_document(skill_name: "...")
```

This returns a file listing like:
```
Available documents for skill 'code-review':
- SKILL.md (text, 3.2 KB)
- scripts/review.py (text, 5.4 KB)
- references/checklist.md (text, 1.8 KB)
```

Then retrieve specific files:

```
read_skill_document(skill_name: "...", document_path: "SKILL.md")
read_skill_document(skill_name: "...", document_path: "references/*")
read_skill_document(skill_name: "...", document_path: "scripts/*.py")
```

Supported patterns: `scripts/*.py`, `references/*`, `*.json`

### 3. Analyze Project Context

Before rewriting, understand:

```bash
# Current project skills
find . -name "SKILL.md" -type f

# Project rules
ls .claude/rules/ 2>/dev/null

# CLAUDE.md laws and conventions
cat CLAUDE.md
```

Identify:
- Overlaps with existing skills
- Project-specific conventions that should be applied
- Gaps the external skill would fill

### 4. Rewrite as New Skill

Use the `write-skill` skill to create a new skill that:

1. **Adapts** the external skill's capabilities to project context
2. **Follows** project conventions (from CLAUDE.md and rules)
3. **Integrates** with existing skills (no duplication)
4. **Localizes** any project-specific terminology or patterns

Key transformations:
- Replace generic examples with project-specific ones
- Add project conventions inline
- Reference existing skills instead of duplicating
- Keep < 200 lines (use references/ for details)

### 5. Validate New Skill

```bash
python3 skills/write-skill/scripts/validate_skill.py <new-skill-path>
```

### 6. Update Plugin Manifest

Add the new skill to the appropriate plugin JSON.

## Output Format

```markdown
## Chrollo Report

### External Skills Found
- [skill-name]: [relevance score] - [brief description]

### Selected for Adaptation
- [skill-name]: [reason for selection]

### New Skill Created
- Path: skills/[new-skill-name]/
- Based on: [external-skill-name]
- Adaptations made:
  - [list of changes]

### Integration Notes
- Related existing skills: [list]
- Rules applied: [list]
```

## Example Usage

```
/rcc:chrollo code review
/rcc:chrollo testing strategies
/rcc:chrollo documentation generation
```
