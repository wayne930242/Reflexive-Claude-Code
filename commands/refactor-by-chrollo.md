---
name: rcc:refactor-by-chrollo
description: Refactor existing skills by searching for better external implementations and adapting them
arguments:
  - name: skill-path
    description: Path to the skill to refactor (e.g., "skills/write-skill")
    required: false
---

# Refactor by Chrollo

Improve existing skills by hunting for better external implementations and synthesizing improvements.

## Prerequisites

Requires `claude-skills-mcp` MCP server. See `/rcc:chrollo` for installation.

## Process

### 1. Identify Skills to Refactor

If `{skill-path}` is provided, target that skill. Otherwise, analyze all:

```bash
find . -name "SKILL.md" -type f
```

For each skill, assess:
- Quality issues (too long, unclear, outdated)
- Missing capabilities that external skills might have
- Potential for improvement

### 2. Search External Alternatives

For each skill to refactor, use Chrollo's hunting approach:

```
find_helpful_skills(query: "[skill's core capability]")
```

For example:
- `write-skill` → search "skill authoring best practices"
- `write-rules` → search "code conventions rules"
- `agent-architect` → search "architecture decision"

### 3. Compare and Analyze

For promising external skills, first list available files:

```
read_skill_document(skill_name: "...")
```

Then read relevant content:

```
read_skill_document(skill_name: "...", document_path: "SKILL.md")
read_skill_document(skill_name: "...", document_path: "references/*")
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

Use `/rcc:improve-skill {skill-path}` with insights from external skills.

### 5. Apply Refactoring

For each skill improvement:

```markdown
## Changes from External Skill: [name]
- Added: [new capability/pattern]
- Improved: [enhanced section]
- Preserved: [project-specific content kept]
```

### 6. Validate Results

```bash
python3 skills/write-skill/scripts/validate_skill.py <skill-path>
```

Check:
- [ ] Still < 200 lines
- [ ] Project conventions maintained
- [ ] No broken references to other skills
- [ ] Integration with existing workflow preserved

## Output Format

```markdown
## Refactor by Chrollo Report

### Skills Analyzed: N

### External Skills Consulted
- [external-skill]: used for [which local skill]

### Improvements Made
| Local Skill | External Source | Changes |
|-------------|-----------------|---------|
| [name] | [source] | [brief] |

### Unchanged (No Better Alternative)
- [skill-name]: [reason]

### Summary
- Skills improved: X
- External skills referenced: Y
- Total patterns borrowed: Z
```

## Example Usage

```
# Refactor specific skill
/rcc:refactor-by-chrollo skills/write-skill

# Refactor all skills
/rcc:refactor-by-chrollo
```

## Difference from /rcc:refactor-skills

| Aspect | refactor-skills | refactor-by-chrollo |
|--------|-----------------|---------------------|
| Focus | Internal consolidation | External improvement |
| Action | Merge/delete redundant | Enhance with external patterns |
| Source | Project skills only | Claude Skills library |
| Goal | Reduce duplication | Increase quality |

Use together: `refactor-skills` to consolidate, then `refactor-by-chrollo` to enhance.
