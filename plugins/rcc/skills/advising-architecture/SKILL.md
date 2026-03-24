---
name: advising-architecture
description: Use when starting any skill/agent/rule workflow to validate approach. Use when classifying knowledge type (law vs rule vs skill vs agent). Use when checking for component conflicts.
context: fork
agent: Explore
argument-hint: "[component-description] [intended-type: law|rule|skill|agent]"
---

# Advising Architecture

## Overview

**Advising architecture IS classifying knowledge into the correct Claude Code component.**

One concept, one location. Misclassification wastes tokens (global rule that should be scoped) or loses enforcement (rule that should be a law).

**Core principle:** Laws = immutable display. Rules = scoped conventions. Skills = capabilities. Agents = isolated workers.

**Violating the letter of the rules is violating the spirit of the rules.**

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[advising-architecture] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Understand the request
2. Scan for conflicts
3. Classify component type
4. Provide recommendation

Announce: "Created 4 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Component Hierarchy (Priority Order)

```
1. CLAUDE.md (highest)       - Broad project instructions
   └─ Loaded every session (expensive — keep < 200 lines)
   └─ Only what Claude can't figure out from code
   └─ Specific, verifiable instructions with MUST/NEVER emphasis

2. Rules (.claude/rules/)    - Path-scoped conventions
   └─ Auto-injected when paths: glob matches
   └─ < 50 lines each (token cost)
   └─ Frontmatter: paths (YAML array of globs)
   └─ No paths = global (loaded at session start)

3. Skills (.claude/skills/)  - Capabilities (how to do)
   └─ Loaded on-demand by Claude OR invoked via /skill-name
   └─ Progressive disclosure: SKILL.md + references/
   └─ Gerund naming: writing-skills, not write-skill
   └─ Frontmatter: name, description, argument-hint,
      allowed-tools, model, effort, context, agent,
      hooks, user-invocable, disable-model-invocation

4. Agents (.claude/agents/)  - Isolated context workers
   └─ Invoked via Agent tool
   └─ Frontmatter: name, description, tools,
      disallowedTools, model, maxTurns, skills,
      permissionMode, effort, isolation, background,
      memory, mcpServers, hooks

5. Hooks (.claude/hooks/)    - Automated quality gates
   └─ Exit code 2 = block action
   └─ < 5 seconds execution
   └─ Static checks only
```

## Classification Decision Tree

```
Does it apply BROADLY to all project work?
├─ Yes → CLAUDE.md instruction
│   Examples: Communication style, build commands, architecture
│   Key: Keep < 200 lines, specific and verifiable
│
└─ No → What type of knowledge?
    │
    ├─ HOW TO DO something (capability)?
    │   → SKILL in skills/
    │   Naming: gerund form (writing-*, creating-*)
    │   Structure: Overview → Tasks → Red Flags → Flowchart
    │   Consider: context: fork for analysis-oriented skills
    │   Consider: model selection (haiku for fast, opus for complex)
    │
    ├─ WHAT TO DO (convention for specific files)?
    │   → RULE in .claude/rules/
    │   Use when: different paths need different conventions
    │     e.g., monorepo packages with different frameworks,
    │     src/ vs tests/ with different coding standards,
    │     frontend (React) vs backend (Express) rules
    │   paths: glob isolates rules to matching files only
    │   Format: paths as YAML array of globs
    │   Keep < 50 lines, imperative language
    │
    ├─ ISOLATED WORKER (needs separate context)?
    │   First consider: built-in subagent types (Explore, Plan, general-purpose)
    │   Then consider: skill with context: fork
    │   Last resort: custom AGENT in agents/
    │   CRITICAL: isolated context = no conversation history
    │   → Design argument-hint/prompt to pass sufficient context
    │
    └─ AUTOMATED CHECK (quality gate)?
        → HOOK in .claude/hooks/
        Python script, exit 2 to block
        Configure in settings.json
```

## Task 1: Understand the Request

**Goal:** Clarify what is being created or modified.

**Questions to answer:**
- What knowledge is being encoded?
- Is it immutable or contextual?
- Is it scoped to specific files?
- Does it teach a capability or enforce a convention?

**Verification:** Can state the knowledge type in one sentence.

## Task 2: Scan for Conflicts

**Goal:** Check existing components for overlaps.

**Process:**
1. Check CLAUDE.md for related laws
2. Check `.claude/rules/` for overlapping conventions
3. Check skills/ for duplicate capabilities
4. Check agents/ for overlapping responsibilities

**Verification:** Listed all related existing components (or confirmed none).

## Task 3: Classify Component Type

**Goal:** Apply decision tree to determine correct component type.

| If it... | Then it's a... |
|----------|----------------|
| Applies broadly to all project work | CLAUDE.md instruction |
| Different paths need different conventions (monorepo, frontend vs backend) | RULE with paths: |
| Teaches how to do something | SKILL |
| Needs isolated execution context | AGENT (or skill with `context: fork`) |
| Is an automated quality gate | HOOK |

**Verification:** Classification matches decision tree logic.

## Task 4: Provide Recommendation

**Goal:** Deliver structured recommendation.

**Output format:**
```markdown
## Architecture Assessment

**Request:** [What you're trying to create]

**Classification:** [law / skill / rule / hook / agent]

**Rationale:** [Why this classification]

**Location:** [Exact path where it should go]

**Conflicts Found:**
- [List any existing components that overlap, or "None"]

**Key Constraints:**
- [Important rules for this component type]

**Recommendation:** [Proceed / Reconsider / Merge with existing]
```

**Verification:** Recommendation includes all fields above.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "This is both a rule AND a skill"
- "Laws are overkill, a rule is fine"
- "Global rule is fine without paths:"
- "Skip conflict scan, it's obviously new"
- "Agent is needed" (before considering built-in types or context: fork)

**All of these mean: You're about to misclassify. Follow the decision tree.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's a bit of both" | Every knowledge has ONE correct location. Classify precisely. |
| "Laws are too heavy" | If it must be immutable, it's a law. Period. |
| "Global rule is simpler" | Global = always injected = token cost. Scope it. |
| "Need a custom agent" | Built-in types or context: fork often suffice. |
| "Conflict scan is overkill" | Duplicated knowledge = contradictions. Always scan. |

## Flowchart: Architecture Assessment

```dot
digraph architecture_assessment {
    rankdir=TB;

    start [label="Need to create\ncomponent", shape=doublecircle];
    understand [label="Task 1: Understand\nrequest", shape=box];
    scan [label="Task 2: Scan\nfor conflicts", shape=box];
    conflicts [label="Conflicts\nfound?", shape=diamond];
    resolve [label="Resolve conflicts\n(merge/replace)", shape=box, style=filled, fillcolor="#ffcccc"];
    classify [label="Task 3: Classify\ncomponent type", shape=box];
    is_immutable [label="Immutable?", shape=diamond];
    law [label="LAW\nin CLAUDE.md", shape=box, style=filled, fillcolor="#ffcccc"];
    is_capability [label="Capability?", shape=diamond];
    skill [label="SKILL\nin skills/", shape=box, style=filled, fillcolor="#ccffcc"];
    is_scoped [label="File-scoped\nconvention?", shape=diamond];
    rule [label="RULE\nin .claude/rules/", shape=box, style=filled, fillcolor="#ccccff"];
    is_isolated [label="Needs\nisolation?", shape=diamond];
    agent [label="AGENT\nor context: fork", shape=box, style=filled, fillcolor="#ffffcc"];
    hook [label="HOOK\nin .claude/hooks/", shape=box];
    recommend [label="Task 4: Provide\nrecommendation", shape=box];
    done [label="Assessment\ncomplete", shape=doublecircle];

    start -> understand;
    understand -> scan;
    scan -> conflicts;
    conflicts -> resolve [label="yes"];
    conflicts -> classify [label="no"];
    resolve -> classify;
    classify -> is_immutable;
    is_immutable -> law [label="yes"];
    is_immutable -> is_capability [label="no"];
    is_capability -> skill [label="yes"];
    is_capability -> is_scoped [label="no"];
    is_scoped -> rule [label="yes"];
    is_scoped -> is_isolated [label="no"];
    is_isolated -> agent [label="yes"];
    is_isolated -> hook [label="no"];
    law -> recommend;
    skill -> recommend;
    rule -> recommend;
    agent -> recommend;
    hook -> recommend;
    recommend -> done;
}
```
