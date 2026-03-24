---
name: brainstorming-workflows
description: Use when exploring user workflows to design an agent system. Use when user says "explore workflows", "setup agent" for a new project. Use when called by analyzing-agent-systems or migrating-agent-systems.
---

# Brainstorming Workflows

## Overview

**Brainstorming workflows IS understanding the human before designing the system.**

Use role templates to quickly identify the user's context, then explore their specific workflows one question at a time. Don't assume the user is a developer — they may use the agent system for project management, content creation, data analysis, or other work.

**Core principle:** The agent system must serve the user's actual workflows, not an imagined ideal.

**Violating the letter of the rules is violating the spirit of the rules.**

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[brainstorming-workflows] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Import analysis findings (if available)
2. Role selection
3. Workflow exploration
4. Produce workflow summary

Announce: "Created 4 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Import Analysis Findings (if available)

**Goal:** If an analysis report exists, bring its findings into the conversation.

**If analysis report path was provided:**
1. Read the analysis report
2. Summarize critical and warning findings
3. Ask user: "分析發現以下弱點，是否要在這次一併修補？"
4. Present findings as a checklist for user to select
5. Record selected items → these become requirements in the workflow summary

**If no analysis report:** Skip to Task 2.

**This allows skipping questions already answered by analysis.** For example:
- Analysis found "no linting hook" → skip asking about code quality tools
- Analysis found "CLAUDE.md > 200 lines" → skip asking about constitution preferences

**Verification:** User has confirmed which findings to address (or no analysis exists).

## Task 2: Role Selection

**Goal:** Identify the user's primary role to guide exploration.

**Present the role table:**

| Role | Typical Workflows |
|------|-------------------|
| **A) Software Developer** | coding, testing, code review, CI/CD, deployment |
| **B) Project Manager** | task tracking, reporting, scheduling, communication |
| **C) Content Creator** | writing, translation, publishing, social media |
| **D) Data Analyst** | data processing, visualization, reporting, automation |
| **E) Operations / DevOps** | monitoring, deployment, incident response, IaC |
| **F) Custom** | describe your role |

**Ask:** "你的角色最接近哪一個？選擇字母即可。"

**Verification:** User has selected a role.

## Task 3: Workflow Exploration

**Goal:** Explore the user's specific workflows one question at a time.

**CRITICAL:** Read [references/role-templates.md](references/role-templates.md) for role-specific deep-dive questions.

**Rules:**
- **One question at a time** — never ask multiple questions in one message
- **Skip questions answered by analysis** — don't re-ask what we already know
- **Multiple choice when possible** — easier for user to answer
- **Adapt to answers** — if user reveals something unexpected, explore it
- **5-8 questions maximum** — don't exhaust the user

**Verification:** Have enough information to map workflows to agent system components.

## Task 4: Produce Workflow Summary

**Goal:** Write structured summary to `docs/agent-system/{timestamp}-workflows.md`.

**Summary format:**

```markdown
# Workflow Summary

**Date:** YYYY-MM-DD HH:MM
**Role:** [selected role]

## Core Workflows
1. [Workflow description]
2. [Workflow description]

## Tasks to Automate
- [Task] → suggested component type (hook/skill/rule)

## Weaknesses to Fix (from analysis)
- [Finding] → planned fix

## Conventions to Enforce
- [Convention] → suggested component type (rule/hook)

## Component Recommendations
| Component | Action | Rationale |
|-----------|--------|-----------|
| CLAUDE.md | create/modify | [reason] |
| Rule: [name] | create | [reason] |
| Hook: [name] | create | [reason] |
| Skill: [name] | create | [reason] |
```

**Handoff:** "工作流摘要完成。要繼續規劃 agent system 元件嗎？"
- If yes → invoke `planning-agent-systems` skill, pass workflow summary path

**Verification:** Summary written with all workflows mapped to components.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "The user is obviously a developer, skip role selection"
- "I know what workflows they need"
- "Ask all questions at once to save time"
- "Skip analysis import, start fresh"
- "Don't need a summary, just proceed to planning"

**All of these mean: You're about to design for assumptions, not reality. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Obviously a developer" | PMs, analysts, creators all use agent systems. Ask. |
| "I know the workflows" | You know common workflows. Theirs may differ. |
| "Multiple questions saves time" | Multiple questions overwhelm. One at a time. |
| "Skip analysis" | Analysis findings prevent redundant questions. Use them. |
| "Summary is overhead" | Summary is the contract for planning. Essential. |

## Flowchart: Workflow Brainstorming

```dot
digraph brainstorm_workflows {
    rankdir=TB;

    start [label="Brainstorm\nworkflows", shape=doublecircle];
    analysis [label="Task 1: Import\nanalysis findings", shape=box];
    has_analysis [label="Analysis\nexists?", shape=diamond];
    confirm_fixes [label="User selects\nfindings to fix", shape=box];
    role [label="Task 2: Role\nselection", shape=box];
    explore [label="Task 3: Workflow\nexploration", shape=box];
    summary [label="Task 4: Produce\nworkflow summary", shape=box];
    handoff [label="Invoke\nplanning-agent-systems", shape=box];
    done [label="Brainstorm complete", shape=doublecircle];

    start -> analysis;
    analysis -> has_analysis;
    has_analysis -> confirm_fixes [label="yes"];
    has_analysis -> role [label="no"];
    confirm_fixes -> role;
    role -> explore;
    explore -> summary;
    summary -> handoff [label="continue"];
    summary -> done [label="stop here"];
    handoff -> done;
}
```

## References

- [references/role-templates.md](references/role-templates.md) — Role-specific deep-dive questions and component mappings
