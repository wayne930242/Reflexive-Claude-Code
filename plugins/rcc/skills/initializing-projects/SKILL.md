---
name: initializing-projects
description: Use when bootstrapping a new project from scratch. Use when user says "create project", "new project", "initialize project", "start new app".
---

# Initializing Projects

## Overview

**Initializing projects IS bootstrapping with modern best practices AND agent system.**

Don't just create files—set up the full development environment including Claude Code integration.

**Core principle:** Research current best practices. Don't assume—verify with official docs.

**Violating the letter of the rules is violating the spirit of the rules.**

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[initializing-projects] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Gather requirements
2. Research best practices
3. Write blueprint
4. Get user confirmation
5. Bootstrap project
6. Setup agent system
7. Final validation

Announce: "Created 7 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Gather Requirements

**Goal:** Understand what project to create.

**First, ask Project Type:**

| Project Type | Follow-up Questions |
|--------------|---------------------|
| **Frontend SPA** | Language, Framework, UI Library, Styling, State, Testing |
| **Full-stack App** | Above + ORM, Database, API Style, Auth |
| **API Service** | Language, Framework, ORM, Validation, Auth |
| **CLI Tool** | Language, Package Manager, Testing |
| **Library** | Language, Build Tool, Testing, Docs |

**Ask iteratively.** Skip already-answered or N/A questions.

**Verification:** Have answers to all relevant questions for project type.

## Task 2: Research Best Practices

**Goal:** Find current best practices for the chosen stack.

**Use WebSearch to find:**
- Latest stable version of framework
- Official CLI/init command
- Recommended project structure
- Current best practices (2025/2026)

**CRITICAL:** Don't assume. Official docs change frequently.

**Verification:** Have official init command and current version numbers.

## Task 3: Write Blueprint

**Goal:** Create a blueprint document for user review.

**Write to:** `/docs/blueprint.md`

### Blueprint Format

```markdown
# Project Blueprint

## Stack
- Language: [name] [version]
- Framework: [name] [version]
- Package manager: [choice]

## Initialization Command
\`\`\`bash
[official CLI command]
\`\`\`

## Project Structure
[Expected directory layout after init]

## Key Dependencies
[Core packages to add]

## Agent System Plan
- CLAUDE.md: [key laws]
- Rules: [planned rules]
- Hooks: [planned quality gates]
```

**Verification:** Blueprint is written and covers all sections.

## Task 4: Get User Confirmation

**Goal:** Have user approve the blueprint before execution.

**CRITICAL:** Do not proceed without explicit user confirmation.

**Present the FULL blueprint content to user.** Do NOT summarize — show every section with detail:
- Stack with exact versions and why each was chosen
- Complete init command with flags explained
- Project structure (directory tree)
- Key dependencies with purpose of each
- Agent system components planned and their rationale

**Anti-pattern:** Listing 3-5 bullet points of one-liners is NOT presenting. The user must see enough detail to catch wrong versions, missing dependencies, or incorrect structure.

**Ask:** "這個 blueprint 正確嗎？要開始執行嗎？"

**Verification:** User has reviewed the full blueprint and explicitly approved.

## Task 5: Bootstrap Project

**Goal:** Run the official CLI to create the project.

**Process:**
1. Run the official init command from blueprint
2. Install additional dependencies if needed
3. Apply any post-init configurations
4. Verify project builds/runs

**Example:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --eslint
cd my-app && npm run dev
```

**Verification:** Project builds and runs without errors.

## Task 6: Setup Agent System

**Goal:** Configure Claude Code for the new project.

**Since this is a new project, skip analysis and go directly to workflow exploration.**

**CRITICAL: Invoke the `brainstorming-workflows` skill.**

The skill chain will automatically continue:
1. `brainstorming-workflows` → explore user's workflows
2. `planning-agent-systems` → plan components
3. `applying-agent-systems` → create components via writing-* skills
4. `refactoring-agent-systems` → review and cleanup

**Verification:** Agent system is configured and verified by the skill chain.

## Task 7: Final Validation

**Goal:** Verify everything works together.

**Checklist:**
- [ ] Project builds without errors
- [ ] Project runs without errors
- [ ] CLAUDE.md exists, under 200 lines, uses standard markdown format
- [ ] Hooks run on file changes (if configured)
- [ ] README documents the setup

**Verification:** All checklist items pass.

## Project Type Quick Reference

### Frontend SPA
```bash
npx create-next-app@latest --typescript --tailwind
# or
npm create vite@latest -- --template react-ts
```

### Full-stack App
```bash
npx create-next-app@latest --typescript
# Add: prisma, next-auth, zod
```

### API Service
```bash
npm init -y && npm install express typescript
# or
cargo new --name api
```

### CLI Tool
```bash
npm init -y && npm install commander
# or
cargo new --name cli
```

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "I know the current version"
- "Skip research, I've done this before"
- "Don't need user confirmation"
- "A brief summary is enough for confirmation"
- "Agent system can wait"
- "Skip validation, it's a fresh project"

**All of these mean: You're about to create a weak foundation. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I know the version" | Versions change monthly. Verify. |
| "Skip research" | Best practices evolve. Check official docs. |
| "Skip confirmation" | Blueprint approval prevents wasted effort. |
| "Brief summary is enough" | Brief summaries hide wrong decisions. Show full detail. |
| "Agent system later" | Set it up now while context is fresh. |
| "Fresh = working" | Fresh projects can have config issues. Validate. |

## Flowchart: Project Initialization

```dot
digraph init_project {
    rankdir=TB;

    start [label="New project", shape=doublecircle];
    gather [label="Task 1: Gather\nrequirements", shape=box];
    research [label="Task 2: Research\nbest practices", shape=box];
    blueprint [label="Task 3: Write\nblueprint", shape=box];
    confirm [label="Task 4: User\nconfirmation", shape=box];
    confirmed [label="Approved?", shape=diamond];
    bootstrap [label="Task 5: Bootstrap\nproject", shape=box];
    agent [label="Task 6: Setup\nagent system", shape=box];
    validate [label="Task 7: Final\nvalidation", shape=box];
    valid [label="All\npasses?", shape=diamond];
    done [label="Project ready", shape=doublecircle];

    start -> gather;
    gather -> research;
    research -> blueprint;
    blueprint -> confirm;
    confirm -> confirmed;
    confirmed -> bootstrap [label="yes"];
    confirmed -> blueprint [label="no\nrevise"];
    bootstrap -> agent;
    agent -> validate;
    validate -> valid;
    valid -> done [label="yes"];
    valid -> bootstrap [label="no\nfix"];
}
```
