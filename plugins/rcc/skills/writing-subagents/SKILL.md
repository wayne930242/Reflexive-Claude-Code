---
name: writing-subagents
description: Creates specialized Claude Code subagents in .claude/agents/ with minimal tools, clear triggers, and isolated context. Use when user says 'create agent', 'add reviewer', 'specialized agent', 'isolated context task'.
---

# Writing Subagents

## Overview

**Writing subagents IS creating specialized workers with isolated contexts.**

Subagents run via the Agent tool with their own context window, tools, and system prompt. Use for tasks that benefit from focused expertise.

**Core principle:** One agent, one responsibility. Bloated agents become unfocused.

## Task Initialization (MANDATORY)

Follow [task initialization protocol](../../references/task-initialization.md).

**Tasks:**
0. Fetch latest official subagent spec
1. Analyze requirements
2. Document problem context
3. Design agent configuration
4. Validate structure
5. Test invocation
6. Verify behavior
7. REFACTOR - quality review

Announce: "Created 8 tasks (0–7). Starting execution..."

## Agent Configuration Process

| Phase | Focus | What You Do |
|-------|-------|-------------|
| **Requirements** | Understanding | Identify what specialized task needs isolation |
| **Analysis** | Problem definition | Document why main agent isn't sufficient |
| **Design** | Configuration | Plan agent tools, model, and system prompt |
| **Implementation** | Creation | Write agent file with proper configuration |
| **Optimization** | Refinement | Fine-tune tools and prompts for efficiency |

## Task 0: Fetch Latest Official Spec

**Goal:** Pull the current Anthropic subagent spec before designing — never trust cached memory.

**Action:**
```
Skill tool: fetching-claude-docs
  component: subagent
  question: "frontmatter fields, tool inheritance, model selection,
             description trigger format (PROACTIVELY, examples), context isolation"
```

**Verification:** Received YAML with `source: https://code.claude.com/docs/en/sub-agents.md` and non-empty `spec_excerpt`. Use this as the **authoritative reference** for Tasks 1–7; if any rule in this SKILL conflicts with the fetched spec, the fetched spec wins (and flag the conflict for refactoring).

## Task 1: Analyze Requirements

**Goal:** Understand what specialized task needs isolation.

**Questions to answer:**
- What specific task needs a subagent?
- Why can't the main agent do this?
- What tools does this agent need?
- Should it be proactive or manual?

**When to use subagents:**
- Task needs isolated context (code review, deep analysis)
- Task would pollute main conversation
- Task is repetitive and well-defined
- Task benefits from specialized system prompt

See [references/examples.md](references/examples.md) for subagent templates and trigger examples.

**Built-in subagent types (consider BEFORE creating custom agents):**

| Type | Model | Tools | Use Case |
|------|-------|-------|----------|
| `Explore` | Haiku | Read-only (no Write/Edit) | Fast codebase search, analysis |
| `Plan` | Inherit | Read-only | Research and planning |
| `general-purpose` | Inherit | All | Complex multi-step tasks |

**Decision:** Can a built-in type handle this? If yes, use it directly via the Agent tool — no agent file needed.

**Verification:** Can describe the agent's single responsibility in one sentence.

## Task 2: Document Problem Context

**Goal:** Clearly understand why the main agent is insufficient for this task.

**Analysis points:**
1. What specific challenges arise when using the main agent?
2. How would task isolation improve the outcome?
3. What context pollution or focus issues occur?
4. What specialized expertise would help?

**Verification:** Documented specific problems that justify creating a specialized subagent.

## Task 3: Design Agent Configuration

**Goal:** Plan the agent configuration to address the documented problems.

**Before drafting the system prompt, walk through [prompt-design-principles.md](../../references/prompt-design-principles.md):**

- 5-skeleton framework — the system prompt needs Role (agent's job, not persona), Scope (what this agent does and doesn't handle), Workflow (procedure for its task), Standards (output rules), Completion (what "done" means for this agent's output).
- Failure-mode reverse engineering — anticipate what this agent could get wrong and write rules against those specific failures.
- Conditional dispatch — if the agent handles multiple task variants, write per-variant behavior, not absolute rules.
- Creative-constraint balance — decide what axes the agent can vary on (e.g., review phrasing) vs. must stay fixed (e.g., output YAML structure).

### Agent Location

```
.claude/agents/      # Project-level
~/.claude/agents/    # User-level (global)
```

### Agent Format

```yaml
---
name: agent-name
description: What this agent does. Use proactively when [triggers].
tools: Read, Grep, Glob, Bash
model: sonnet
---

System prompt for the agent.

## Role
[Clear description of the agent's responsibility]

## Process
[Steps the agent should follow]

## Output Format
[Expected output structure]
```

### Configuration & Tools

See [references/agent-spec.md](references/agent-spec.md) for full configuration fields, model selection, context:fork guidelines, and tool permissions.

**Key rules:**
- `name`: lowercase with hyphens, matches filename
- `description`: include 2-4 concrete examples in `<example>` blocks showing triggering conditions
- `model`: specified explicitly; `inherit` is an anti-pattern in plugin agents (only project/user-level agents in `.claude/agents/` may omit)
- `color`: unique color per agent (blue, green, red, purple, yellow)
- `tools`: minimal set (principle of least privilege). Subagents cannot request permissions at runtime.
- Plugin agents do not support `hooks`, `mcpServers`, or `permissionMode`
- System prompt should encourage parallel tool calls for independent operations (e.g. "When reading N files, fire N Read calls in a single response")

| Agent Type | Recommended Tools |
|------------|-------------------|
| Code reviewer | `Read, Grep, Glob` |
| Test runner | `Read, Bash, Grep` |
| Explorer | `Read, Glob, Grep, Bash` |
| Writer | `Read, Edit, Write` |

See [references/agent-spec.md](references/agent-spec.md) for the three-layer model selection guide, isolation guide, effort guide, and Opus/Haiku constraints.

**Verification:**
- [ ] Name is lowercase with hyphens
- [ ] Description has clear trigger
- [ ] `model` explicitly specified (`inherit` = anti-pattern in plugin agents)
- [ ] Tools are minimal (principle of least privilege)
- [ ] System prompt is focused

## Task 4: Validate Structure

**Goal:** Verify agent file structure is correct.

**Checklist:**
- [ ] File is in `.claude/agents/` directory
- [ ] Frontmatter has `name` and `description`
- [ ] Name matches filename (minus .md)
- [ ] Tools are appropriate for the task
- [ ] System prompt is actionable
- [ ] No overlapping responsibility with other agents

**Verification:** All checklist items pass.

## Task 5: Test Invocation

**Goal:** Verify agent can be invoked via Agent tool.

**Test:**
```
Agent tool:
- subagent_type: "[plugin:]agent-name"
- prompt: "Test invocation"
```

**Check:**
- Agent loads correctly
- System prompt is applied
- Tool restrictions work
- Model selection honored

**Verification:** Agent invocation succeeds without errors.

## Task 6: Verify Behavior

**Goal:** Run agent on real task and verify quality.

**Process:**
1. Invoke agent with real task input
2. Observe agent follows its system prompt
3. Verify output matches expected format
4. Check agent stays within its scope

**Verification:**
- Agent produces expected output
- Agent uses only granted tools
- Agent doesn't exceed its scope

## Task 7: REFACTOR - Quality Review

**Goal:** Have subagent reviewed by subagent-reviewer.

```
Agent tool:
- subagent_type: "rcc:subagent-reviewer"
- prompt: "Review subagent at [path/to/agent.md]"
```

**Interpret YAML output:**
- `pass: true` → Subagent complete
- `pass: false` → Fix all issues listed, re-run reviewer, repeat until `pass: true`

**This is the REFACTOR phase:** Close loopholes identified by reviewer.

**Verification:** subagent-reviewer returns YAML with `pass: true`.

## Trigger Patterns

- **Proactive:** Include "Use proactively when..." in description for auto-invoke
- **Manual:** Omit proactive triggers for explicit-only invocation

## Designing for Parallel Use (P-Thread / F-Thread)

A single agent file may be invoked once, fanned-out, or voted on.
Design choices change depending on which.

| Pattern | Invocation | Design implication |
|---------|------------|--------------------|
| **Single** | One Agent call | Default. No special design needed. |
| **P-Thread (fanout)** | N Agent calls in one message, different inputs | Output must be self-contained — no shared state, no "see other agent's result". |
| **F-Thread (Best-of-N)** | N Agent calls in one message, **same input** | Output must be deterministic-shape (YAML / structured) so caller can diff or vote. Reviewer agents are prime F-Thread candidates. |
| **B-Thread (orchestrator)** | This agent dispatches sub-agents itself | Grant the Agent tool. Document which sub-agents it may call. |

**Rules when designing for fanout:**

- Output schema must be **machine-mergeable** — fixed keys, not free prose.
- Avoid side effects (writes, commits) — fanned agents collide on the same files.
- Keep tool set narrow — `Read, Grep, Glob` is safe for N-parallel; `Write, Edit, Bash` is not.
- If an agent runs in F-Thread, its system prompt should say "you are one of several reviewers; do not coordinate, just give your independent judgment."

For dispatch mechanics (how the caller fans out and merges results), see the `dispatching-parallel-agents` skill.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "This agent needs all tools"
- "One agent can handle multiple responsibilities"
- "Main context is fine, don't need isolation"
- "Skip testing, the prompt is simple"
- "Use opus for everything / use haiku for everything"

**All of these mean: You're about to create a weak agent. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Needs all tools" | More tools = more ways to go wrong. Minimize. |
| "Multi-purpose agent" | Jack of all trades = master of none. One job. |
| "Main context works" | Context pollution is invisible until it's a problem. |
| "Simple prompt" | Simple ≠ correct. Test the behavior. |
| "Use opus for everything / use haiku for everything" | Each layer has a role. Start with Sonnet as implementer. Add Haiku orchestration only when dispatch complexity justifies it. Add Opus quality gate only with a revision loop. |

## References

- [references/examples.md](references/examples.md) - Subagent templates
- [references/tools.md](references/tools.md) - Available tools reference
- [../../references/prompt-design-principles.md](../../references/prompt-design-principles.md) - 5-skeleton framework, failure-mode reverse engineering, conditional dispatch, creative-constraint balance, completion semantics
- See also: `advising-architecture` skill for component classification guidance
