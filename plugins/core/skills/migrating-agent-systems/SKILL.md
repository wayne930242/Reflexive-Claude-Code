---
name: migrating-agent-systems
description: Initializes or migrates agent systems to Claude Code best practices architecture. Use when setting up agent system for a project or migrating existing configurations.
---

# Migrating Agent Systems

Initialize new or migrate existing agent systems to recommended architecture.

## Critical Rule

**Invoke the appropriate skill for each component. Do not create files directly.**

## Process

### 1. Project Discovery

Invoke `project-discovery` skill to:
- Scan project structure and tech stack
- Identify existing workflows and automation
- Discover patterns and conventions
- **Produce a Discovery Report**

Present findings to user for validation.

### 2. Architecture Planning

Invoke `agent-architect` skill to:
- Receive validated Discovery Report
- Design complete architecture for the project
- **Produce a detailed plan** listing all components

### 3. Execute Tasks

Based on the architecture plan, invoke the correct skill for each component:

| Component | Skill to Invoke |
|-----------|-----------------|
| Constitution | `writing-claude-md` |
| Skills | `writing-skills` |
| Subagents | `writing-subagents` |
| Hooks (static checks) | `writing-hooks` |
| Rules (conventions) | `writing-rules` |

### Rules Discovery

Analyze the project to infer conventions. Ask user only when uncertain:

1. **Code style** - Formatting, naming conventions, import order
2. **Language conventions** - Framework-specific patterns
3. **Architecture** - Project structure, layering, module boundaries
4. **Methodology** - DDD, TDD, clean architecture, other patterns

**CRITICAL**:
- Complete each task one by one
- You MUST invoke the skill for each task
- Do NOT write files directly

### 4. Validation

After all tasks complete, verify the architecture plan is fully implemented.
