---
name: planning-agent-systems
description: Use when planning which agent system components to create or modify. Use when called by brainstorming-workflows after workflow exploration is complete.
---

# Planning Agent Systems

## Overview

**Planning agent systems IS mapping workflows to components with explicit rationale.**

Read the analysis report and workflow summary, decide what to create/modify/delete, identify which writing-* skills to invoke, and get user confirmation before execution.

**Core principle:** Every component must trace back to a workflow need or a weakness fix. No speculative components.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Chain
**Handoff:** user-confirmation
**Next:** `applying-agent-systems`
**Chain:** main

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[planning-agent-systems] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Read inputs
2. Design architecture flowchart
3. Plan components (includes reuse check)
4. Produce component plan
5. Get user confirmation

Announce: "Created 5 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Read Inputs

**Goal:** Load analysis report (if available) and workflow summary.

**Read:**
- `docs/agent-system/*-analysis.md` (most recent, if exists)
- `docs/agent-system/*-workflows.md` (most recent)

**Extract:**
- Weaknesses marked for fixing
- Workflows to support
- Conventions to enforce
- Component recommendations from workflow summary

**Verification:** Have a clear list of requirements from both sources.

## Task 2: Design Architecture Flowchart

**Goal:** Visualize the entire agent system topology before deciding individual components.

**Why this comes first:** Component lists hide dependency gaps and workflow disconnects. A flowchart forces you to see the whole picture — entry points, decision branches, data flow, and handoff points — before committing to any component.

**CRITICAL:** Read [references/anthropic-patterns.md](references/anthropic-patterns.md) for the six Anthropic workflow patterns, DOT flowchart conventions, and dependency graph template.

**Step 1 — Classify workflows into Anthropic patterns** using the reference table.

**Step 2 — Draw the architecture flowchart** in DOT format using the reference conventions.

**Step 3 — Build the dependency graph** from the flowchart, assigning phases by dependency depth.

**Step 4 — Identify the simplest viable subset:**

Ask: "What is the minimum set of components that delivers value?"
- Mark each component as **core** (must-have for any workflow to work) or **enhancement** (improves but not required)
- Phase 1 should contain ONLY core components
- Present the phased rollout to user for early feedback

**Verification:** Architecture flowchart produced showing all workflows, patterns identified, dependency graph built, phases assigned.

## Task 3: Plan Components

**Goal:** Decide action for each component type.

**CRITICAL:** Read [references/component-planning.md](references/component-planning.md) for the evaluation table, decision criteria, size constraints, and writing skill assignments.

**Use the dependency graph from Task 2** to determine execution order. Do NOT use a fixed order — let dependencies drive sequencing. Components in the same phase with no mutual dependencies can be built in parallel.

**Verification:** Each planned component has a traced rationale and assigned writing-* skill. No conflicts identified.

## Task 4: Produce Component Plan

**Goal:** Write structured plan to `docs/agent-system/{timestamp}-plan.md`.

**CRITICAL:** Read [references/plan-template.md](references/plan-template.md) for the full plan format including architecture flowchart, pattern mapping, dependency graph, and component sections.

**Verification:** Plan written with complete execution order and traceability.

## Task 5: Get User Confirmation

**Goal:** Present plan and get explicit approval.

**Present the FULL plan to user.** Show: architecture flowchart, pattern mapping, dependency graph with phases, each component's purpose and content, weakness fixes, core/enhancement classification, and estimated scope per phase.

**Anti-pattern:** Listing component names without explaining what they do is NOT presenting.

**Ask:** "這個計畫看起來可以嗎？要開始建立元件嗎？"

**Handoff:** After user confirms → invoke `applying-agent-systems` skill, pass plan path

**Verification:** User has reviewed the full plan and explicitly approved.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

| Thought | Reality |
|---------|---------|
| "Skip the flowchart" | Component lists hide dependency gaps. The flowchart reveals what's missing. |
| "Create everything" | YAGNI. Only create what traces to a need. |
| "Skip traceability" | Untraceable components become mystery debt. |
| "Skip confirmation" | User approval prevents wasted effort. |
| "Skip reuse check" | Duplicating existing skills creates conflicts. |
| "One big rule" | Multiple focused rules > one bloated rule. |
| "Fixed order is fine" | Dependencies vary per project. Let the graph decide. |

## Flowchart: Agent System Planning

```dot
digraph plan_agent {
    rankdir=TB;

    start [label="Plan agent\nsystem", shape=doublecircle];
    read [label="Task 1: Read\ninputs", shape=box];
    flowchart [label="Task 2: Design\narchitecture flowchart", shape=box, style=filled, fillcolor="#ffffcc"];
    plan [label="Task 3: Plan\ncomponents", shape=box];
    produce [label="Task 4: Produce\ncomponent plan", shape=box];
    confirm [label="Task 5: User\nconfirmation", shape=box];
    approved [label="Approved?", shape=diamond];
    handoff [label="Invoke\napplying-agent-systems", shape=box];
    done [label="Planning complete", shape=doublecircle];

    start -> read;
    read -> flowchart;
    flowchart -> plan;
    plan -> produce;
    produce -> confirm;
    confirm -> approved;
    approved -> handoff [label="yes"];
    approved -> flowchart [label="no\nrevise"];
    handoff -> done;
}
```

## References

- [references/anthropic-patterns.md](references/anthropic-patterns.md) — Six Anthropic workflow patterns, DOT conventions, dependency graph template
- [references/component-planning.md](references/component-planning.md) — Evaluation table, decision criteria, size constraints, writing skills
- [references/plan-template.md](references/plan-template.md) — Full component plan document format
