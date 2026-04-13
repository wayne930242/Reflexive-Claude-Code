---
name: reflecting
description: Use when completing significant work to extract learnings. Use when user corrects your approach or when you discover important patterns during agent interactions. Use when agent learns something new that should be captured for future reference. Use when user says "reflect", "what did we learn", "capture learnings". Use after resolving complex problems or discovering patterns.
---

# Reflecting

## Overview

**Reflecting IS converting experience into a structured report for the planning pipeline.**

Analyze the conversation, extract learnings, and produce a reflection report. Route the report to planning-agent-systems — do not classify or create components directly.

**Core principle:** Capture before context is lost. Classify just enough for planning to act on.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Chain
**Handoff:** auto-invoke
**Next:** `planning-agent-systems`

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[reflecting] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Analyze conversation
2. Extract knowledge
3. Produce reflection report
4. Review report quality
5. Consolidation review
6. Route to planning

Announce: "Created 6 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 1: Analyze Conversation

**Goal:** Review the conversation to identify significant events.

**Look for:**
- **Corrections** — user corrected the agent's approach or output
- **Errors** — agent made a mistake, multiple attempts needed
- **Discoveries** — new insights about the project, domain, or tooling
- **Repetitions** — same action performed multiple times (automation candidate)

**Trace the skill router for each event:**
For corrections and errors, identify which component routed the agent to that behavior:
1. Which skill was active? (check skill invocations in conversation)
2. Which rule or CLAUDE.md law triggered the approach?
3. Was there no router (agent used general knowledge)?

**Locate the router's actual file path** — use Glob to find it:
- Skill → `Glob "**/skills/{name}/SKILL.md"` (covers `plugins/**/skills/` and `.claude/skills/`)
- Rule → `Glob "**/.claude/rules/{name}.md"`
- Agent/Subagent → `Glob "**/agents/{name}.md"` (covers `plugins/**/agents/` and `.claude/agents/`)
- CLAUDE.md → project root `CLAUDE.md`

If Glob returns multiple matches, record all paths — the conversation context usually disambiguates which one was active.

Record the resolved path. This path is used in Task 2 dedup gate.

This determines where fixes land:
- Router is a skill → fix goes in that skill
- Router is a rule → fix goes in that rule
- Router is CLAUDE.md → fix goes in CLAUDE.md
- No router → new rule or skill needed

**Document each event:**
```
Event: [What happened]
Context: [When/where it occurred]
Outcome: [Result]
Type: correction / error / discovery / repetition
Router: [skill/rule/law/none that caused this behavior]
Router path: [resolved file path, or "none"]
```

**Verification:** Listed at least 3 significant events. If fewer than 3 occurred, document why. Each event has a router identified (or explicitly "none").

## Task 2: Extract Knowledge

**Goal:** Derive actionable learnings from each event.

**For each event, ask:**
- What would have prevented this failure?
- What made this succeed that could be repeated?
- What did we learn that applies beyond this task?

**Simplicity principle:** Prefer the simplest component type that works.
- A one-line convention → `rule`, not a `skill`
- A repeated multi-step process → `skill`, not a `doc`
- An immutable project constraint → `law`, not a `rule`

**Learning format:**
```yaml
Learning:
  context: [When this applies]
  insight: [What was learned]
  evidence: [Specific event that taught this]
  router: [Which component routed the behavior, from event trace]
  fix_target: [Same component as router, or new component if router=none]
  suggested_component: rule / law / skill / hook / doc
  rationale: [Why this component type fits, informed by router analysis]
```

**Verification:** Each event has at least one learning with router, fix_target, suggested component, and rationale.

## Task 3: Produce Reflection Report

**Goal:** Write a structured report for the planning pipeline.

1. Read `references/report-template.md` for format and completeness checklist
2. Determine timestamp: `YYYY-MM-DD` format
3. Write report to `docs/agent-system/{timestamp}-reflection.md`

The report must follow the template exactly, including:
- Session context
- Events table (Event / Context / Outcome / Type)
- Learnings table (Learning / Evidence / Suggested Component / Rationale)
- Component recommendations with path hints and content summaries
- Weaknesses addressed (if applicable)

**Verification:** Report file exists at the expected path with no placeholder text.

## Task 4: Review Report Quality

**Goal:** Verify the report is complete before routing.

Use the completeness checklist from `references/report-template.md`:

- [ ] Every event has at least one learning
- [ ] Every learning has router, fix_target, suggested component, and rationale
- [ ] Every component recommendation has type, path hint, content summary, and traces-to
- [ ] No placeholder text (TBD, TODO, etc.)
- [ ] Session context accurately describes the work done
- [ ] At least 3 events documented (or explanation of why fewer)

**If missing learnings** → return to Task 2, extract more, then re-run Task 3.
**If format issues** → return to Task 3, fix the report.

**Verification:** All checklist items pass.

## Task 5: Consolidation Review

**Goal:** Ensure recommendations consolidate into existing components rather than bloating the system.

**Only review components with diff** — invoke reviewer agents on each recommendation's fix_target (using router path from Task 1).

**For each recommendation, invoke the corresponding reviewer agent:**

| fix_target type | Reviewer agent |
|-----------------|----------------|
| skill | `skill-reviewer` (has overlap check) |
| rule | `rule-reviewer` (has duplication check) |
| CLAUDE.md | `claudemd-reviewer` (has duplication check) |
| agent/subagent | `subagent-reviewer` (has overlap check) |
| hook | `hook-reviewer` |
| none (new component) | Invoke the reviewer matching `suggested_component` type |

**Pass the fix_target path to the reviewer.** The reviewer will check for overlap with existing components.

**Based on reviewer output, adjust recommendations:**
- Reviewer finds full overlap → remove recommendation, note why
- Reviewer finds partial overlap → change to "modify existing", describe only the gap
- Multiple recommendations to same fix_target → merge before invoking reviewer once
- Reviewer passes → keep recommendation as-is

**Edit the report:** Directly modify the report file from Task 3, adjusting the recommendations section.

**Verification:** Every recommendation has been reviewed by the appropriate agent. No redundant recommendations remain.

## Task 6: Route to Planning

**Goal:** Hand off the reflection report to planning-agent-systems.

1. Announce: "Reflection complete. Routing report to planning-agent-systems."
2. State the report path
3. Invoke `planning-agent-systems` with the report path as input

**Do not** classify components yourself. **Do not** create components directly. Planning handles classification and execution.

**Verification:** planning-agent-systems invoked with correct report path.

## Proactive Triggers

**When to self-trigger reflection:**
- User corrects your approach or methodology
- Agent discovers unexpected patterns or insights
- Failed assumptions are revealed during work
- New knowledge emerges that contradicts previous understanding
- User provides feedback that changes your mental model
- Workflow gaps or improvement opportunities are identified

**Integration with Memory System:**
Reflection reports automatically feed into Claude Code's built-in memory system at `/home/weihung/.claude/projects/-home-weihung-Reflexive-Claude-Code/memory/`. No additional memory management needed.

## When to Reflect

**Trigger reflection after:**
- Completing a significant feature
- Resolving a difficult bug
- Multiple failed attempts → eventual success
- Discovering something unexpected
- End of long working session

**Don't wait for "later" — context fades quickly.**

## Red Flags — STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "Nothing worth capturing"
- "I'll remember this"
- "Too small to document"
- "Reflection is overhead"
- "Skip the report, just create components directly"
- "I know where this learning belongs, skip planning"
- "Each learning needs its own recommendation"

**All of these mean: You're about to short-circuit the pipeline. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Nothing learned" | Every session has learnings. Look harder. |
| "I'll remember" | You won't. Context fades. Capture now. |
| "Too small" | Small learnings compound. Capture them. |
| "Overhead" | 10 minutes now saves hours later. |
| "Create directly" | Bypasses conflict checks, simplicity gates, and reviews. |
| "I know where it goes" | Planning has component-planning criteria you don't carry inline. |
| "Each learning = one recommendation" | Multiple learnings often belong in the same component. Consolidate. |

## Flowchart

```dot
digraph reflecting {
    rankdir=TB;

    start [label="Reflect on work", shape=doublecircle];
    analyze [label="Task 1: Analyze\nconversation", shape=box];
    extract [label="Task 2: Extract\nknowledge", shape=box];
    report [label="Task 3: Produce\nreflection report", shape=box];
    review [label="Task 4: Review\nreport quality", shape=box];
    quality_ok [label="Complete?", shape=diamond];
    consolidate [label="Task 5: Consolidation\nreview", shape=box];
    route [label="Task 6: Route\nto planning", shape=box];
    done [label="Handoff complete", shape=doublecircle];

    start -> analyze;
    analyze -> extract;
    extract -> report;
    report -> review;
    review -> quality_ok;
    quality_ok -> consolidate [label="yes"];
    quality_ok -> extract [label="missing\nlearnings"];
    quality_ok -> report [label="format\nissues"];
    consolidate -> route;
    route -> done;
}
```

## References

- `references/report-template.md` — report format and completeness checklist
- `planning-agent-systems` — classification and component creation
