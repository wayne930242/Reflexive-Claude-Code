---
name: initializing-projects
description: Initializes a new project with framework, best practices, and agent system from scratch. Use when bootstrapping a new project or setting up development environment.
---

# Initializing Projects

Bootstrap a new project with modern best practices and agent system.

## Process

### 1. Requirements Gathering

First ask **Project Type**, then ask relevant questions based on type.

#### Project Types → Questions

| Project Type | Questions to Ask |
|--------------|------------------|
| **Frontend SPA** | Language, Framework, UI Library, Styling, State Management, Package Manager, Testing, Linting |
| **Full-stack App** | Above + ORM/Database, Validation, API Style, Auth Strategy |
| **API Service** | Language, Framework, ORM, Validation, API Style, Auth, Testing |
| **CLI Tool / Library** | Language, Validation, Package Manager, Testing, Linting |
| **Static Blog / Docs** | Language, Framework, Styling, Static Site Generator |

Ask questions iteratively. Skip if already answered or not applicable.

### 2. Research Best Practices

Use web search to find:
- Latest stable version of chosen framework
- Official CLI tool and initialization commands
- Current best practices and recommended project structure

### 3. Write Blueprint

Create `/docs/blueprint.md` with:

```markdown
# Project Blueprint

## Stack
- Language: [version]
- Framework: [version]
- Package manager: [choice]

## Project Structure
[Recommended directory layout]

## Initialization Command
[Official CLI command, e.g., `npx create-next-app@latest`]

## Key Dependencies
[Core packages with versions]
```

**Ask user to confirm the blueprint before proceeding.**

### 4. Bootstrap Project

After user confirmation:
1. Run the official CLI tool to create project
2. Install additional dependencies if needed
3. Apply any post-init configurations

### 5. Setup Agent System

**CRITICAL: Invoke the `migrating-agent-systems` skill.**

This handles:
- Create CLAUDE.md with project-specific constitution
- Setup skills as needed
- Configure hooks for static checks
- Create rules based on discovered conventions

### 6. Final Confirmation

Ask user if they want to proceed with bootstrapping according to the blueprint.
