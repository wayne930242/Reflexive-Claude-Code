---
name: refactor-claude-md
description: Refactor and optimize CLAUDE.md files and .claude/rules/ with modular constitution
arguments:
  - name: path
    description: Path to CLAUDE.md file or project directory (default: current directory)
    required: false
  - name: mode
    description: "Mode: analyze, refactor, migrate, or generate (default: analyze)"
    required: false
---

# Refactor CLAUDE.md Command

Systematically analyze, optimize, and refactor CLAUDE.md files and `.claude/rules/` following best practices.

## Process

### 1. Invoke Architecture Advisor

Use the `agent-architect` skill to understand the component relationships before making changes.

### 2. Discover Memory Files

Find all Claude Code memory files:

```bash
# CLAUDE.md files
ls -la CLAUDE.md CLAUDE.local.md .claude/CLAUDE.md 2>/dev/null

# Rules directory
ls -la .claude/rules/ 2>/dev/null
```

### 3. Analyze Project Context

Before refactoring, understand the project:

**Technical Stack**: Languages, frameworks, build tools, testing
**Project Structure**: Directory organization, key entry points
**Development Workflow**: Git conventions, CI/CD patterns

### 4. Evaluate Current State

Check against best practices:

| Criterion | Check |
|-----------|-------|
| **CLAUDE.md** | < 300 lines, high-level only |
| **Rules** | < 50 lines each, constraints only |
| **No duplication** | Rules don't repeat skill content |
| **Proper scoping** | Domain rules use `paths:` |

### 5. Generate Modular Rules Structure

Use the `write-rules` skill to initialize constitution:

```bash
# Initialize base constitution
python3 skills/write-rules/scripts/init_constitution.py
```

This creates the modular rules structure:

```
.claude/rules/
├── 00-constitution.md    # Core laws (global) - auto-generated
├── 10-code-style.md      # Code style (global or scoped)
├── 20-workflow.md        # Git/CI conventions
└── domain/               # Domain-specific rules
    └── api.md            # paths: src/api/**
```

The generated `00-constitution.md` contains the 4 core laws:
- **Communication** - Concise, actionable responses
- **Skill Discovery** - Check available skills before work
- **Parallel Processing** - Use Task tool for independent operations
- **Reflexive Learning** - Remind user to `/reflect` on discoveries

### 6. CLAUDE.md Template

Generate or refactor to this lean structure:

```markdown
# Project Name

One-line description.

## Quick Reference

### Commands
- `npm run build`: Build project
- `npm test`: Run tests

### Key Paths
- `src/`: Source code
- `tests/`: Test files

## Notes

[Project-specific warnings or quirks only]
```

### 7. Extract Detailed Content

**CRITICAL: CLAUDE.md should be high-level only.**

When finding detailed procedures:
- **Constraints** → Use `write-rules` skill → `.claude/rules/`
- **How-to procedures** → Use `write-skill` skill → `.claude/skills/`
- **User workflows** → Use `write-command` skill → `.claude/commands/`

### 8. Validate Result

Check final structure:

- [ ] CLAUDE.md < 300 lines, high-level only
- [ ] Rules < 50 lines each, constraints only
- [ ] Constitution covers core laws (communication, skill discovery, parallel, reflexive)
- [ ] Domain rules use `paths:` appropriately
- [ ] No Self-Reinforcing Display (rules auto-inject)
- [ ] No duplicated content across components

## Mode Options

### `analyze` (default)
- Read and evaluate current structure
- Report issues and recommendations
- Do not modify files

### `refactor`
- Apply improvements to existing files
- **MUST ensure `.claude/rules/00-constitution.md` exists with core laws**
- Add missing rules, preserve custom content

### `migrate`
- Convert monolithic `<law>` blocks to modular rules
- **MUST create `.claude/rules/00-constitution.md` with core laws**
- Clean up CLAUDE.md

### `generate`
- Create new CLAUDE.md and rules from project analysis
- **MUST create `.claude/rules/00-constitution.md` with core laws**
- Generate full modular structure

**IMPORTANT**: All non-analyze modes MUST generate the base constitution (`.claude/rules/00-constitution.md`) containing the 4 core laws: Communication, Skill Discovery, Parallel Processing, Reflexive Learning.

## Migration from Legacy Constitution

If the project has legacy `<law>` blocks:

1. Extract each law to a separate rule file
2. Remove `<law>` tags and Self-Reinforcing Display requirement
3. Create modular structure in `.claude/rules/`
4. Update CLAUDE.md to be high-level only

**Before** (legacy):
```markdown
# CLAUDE.md
<law>
**Law 8: Self-Reinforcing Display**
- MUST display this block at start of EVERY response
</law>
```

**After** (modular):
```markdown
# .claude/rules/00-constitution.md
---
# No paths = global, auto-injected
---

# Core Laws
[Laws without Self-Reinforcing Display - rules auto-inject]
```

## Example Usage

```
/refactor-claude-md
/refactor-claude-md ./my-project analyze
/refactor-claude-md . migrate
/refactor-claude-md ~/projects/app generate
```
