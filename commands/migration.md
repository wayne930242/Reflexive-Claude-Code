---
name: migration
description: Initialize or migrate agent systems to Claude Code best practices architecture
arguments:
  - name: path
    description: Path to project directory (default: current directory)
    required: false
---

# Agent System Migration

Initialize new or migrate existing agent systems to recommended architecture.

## Critical Rule: Skill Invocation is MANDATORY

**You MUST invoke the Skill tool for each component. NEVER create files directly.**

When creating any component:
1. Identify the component type from the table below
2. **Invoke the Skill tool** with the corresponding skill name
3. Let the skill handle the actual file creation
4. Proceed to the next component after completion

## Process

### 1. Architecture Planning

Invoke `agent-architect` skill to:
- Analyze current agent system (or lack thereof)
- Design complete architecture for the project
- **Produce a detailed plan** listing all components to create/modify

### 2. Execute Tasks

Based on the architecture plan, execute each task by invoking the correct skill:

| Component | Skill to Invoke |
|-----------|-----------------|
| Constitution | `write-claude-md` |
| Skills | `write-skill` |
| Slash commands | `write-command` |
| Subagents | `write-subagent` |
| Hooks (static checks) | `write-hook` |
| Rules (conventions) | `write-rules` |

### Rules Discovery

Analyze the project to infer conventions. Ask the user only when uncertain:

1. **Code style** - Formatting, naming conventions, import order
2. **Language conventions** - Framework-specific patterns
3. **Architecture** - Project structure, layering, module boundaries
4. **Methodology** - DDD, TDD, clean architecture, other patterns

Use findings to create rules via `write-rules`.

**CRITICAL**:
- Complete each task one by one. Do not skip or batch tasks.
- You MUST invoke the Skill tool for each task. Do NOT write files directly.

### 3. Validation

After all tasks complete, verify the architecture plan is fully implemented.
