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

**CRITICAL**: Complete each task one by one. Do not skip or batch tasks.

### 3. Validation

After all tasks complete, verify the architecture plan is fully implemented.
