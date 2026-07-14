---
name: dispatching-parallel-agents
description: Fans out work across multiple agents — same prompt to many for Best-of-N, different prompts for parallel exploration, or a scout before committing. Use when user says "parallel agents", "fan out", "best of N", "scout", "race", "vote", "spawn workers".
---

# Dispatching Parallel Agents

## Overview

**Dispatching parallel agents IS trading compute for confidence or throughput.**

A single Agent call is one bet.
N Agent calls in one message is N bets — they execute concurrently and you pick or merge.
The runtime fans out automatically when multiple Agent tool uses appear in a single response; serializing by mistake (one Agent call per response) wastes the entire benefit.

**Core principle:** Parallelism is a property of the dispatch (one message, N tool uses), not of the agents themselves.

## Task Initialization (MANDATORY)

Follow [task initialization protocol](../../references/task-initialization.md).

**Tasks:**
0. Classify the dispatch pattern
1. Choose agents and inputs
2. Fan out in a single message
3. Merge results
4. Report to user

Announce: "Created 5 tasks (0–4). Starting execution..."

## Task 0: Classify the Dispatch Pattern

**Goal:** Pick exactly one pattern. Mixing patterns = confused merge step.

| Pattern | When | Inputs | Merge strategy |
|---------|------|--------|----------------|
| **P-Thread** (parallel, divergent) | Independent subtasks, each agent owns a slice | N **different** prompts | Concatenate — each result stands alone |
| **F-Thread** (Best-of-N, fusion) | One hard question, want confidence or cherry-pick | N **identical** prompts | Vote / diff / cherry-pick |
| **Scout** (throw-away recon) | Unfamiliar territory, want to learn before committing | One scout prompt, **discard the code** | Read scout's findings → write better main prompt |
| **B-Thread** (nested orchestrator) | One sub-agent dispatches further sub-agents | Single Agent call to an orchestrator agent | Orchestrator handles its own merge |

**Anti-patterns:**

- "I'll fan out 5 agents to write the same file" — they collide. Fanout is for **read-only or sliced-write** tasks.
- "I'll fan out then iterate on each" — that's serial, not parallel. Decide the dispatch shape upfront.
- "Best-of-N for a deterministic question" — if the answer is `git log`, one agent suffices. F-Thread costs N× tokens; pay only when judgment varies.

**Verification:** Can name the pattern in one word and justify it in one sentence.

## Task 1: Choose Agents and Inputs

**Goal:** Pick the agent type per call and the prompts.

**Agent selection:**

| Need | Use |
|------|-----|
| Read-only research | `Explore` (Haiku, fast, no Write/Edit) |
| Planning | `Plan` |
| Code review (F-Thread voting) | Project reviewer agents (e.g. `rcc:skill-reviewer`) |
| General multi-step | `general-purpose` |

**Prompt design for fanout:**

- Each prompt is **self-contained** — agents do not see this conversation, do not see each other's output.
- For F-Thread: identical prompts, identical context. The only variable is the agent's stochastic output.
- For P-Thread: explicit slice in each prompt — "you handle X, ignore Y."
- For Scout: tell the scout it's a scout — "your output will be discarded; report what you learned, what files you touched, where you got stuck."

**Tool set:** Pass minimal tools. Fanout amplifies any tool the agent has — five Edits in parallel = five chances to corrupt the same file.

**Verification:** Each prompt readable cold, no implicit context, tool set scoped.

## Task 2: Fan Out in a Single Message

**Goal:** Issue all N Agent calls in **one assistant turn**.

**Why this matters:** the runtime parallelizes tool uses within a single message. Splitting across turns serializes them and you pay round-trip latency × N.

**Correct shape:**

```
[one assistant message]
  Agent(prompt=A, ...)
  Agent(prompt=B, ...)
  Agent(prompt=C, ...)
```

**Wrong shape (serial):**

```
[message 1] Agent(A) → wait → [message 2] Agent(B) → wait → ...
```

**Background flag:** for long-running fans (>2 min each), set `run_in_background: true` so the main turn doesn't block. The runtime notifies on completion.

**Verification:** All Agent calls visible in a single assistant message.

## Task 3: Merge Results

**Goal:** Collapse N outputs into one decision or report.

**Merge strategies by pattern:**

| Pattern | Strategy |
|---------|----------|
| **P-Thread** | Concatenate sections. Each agent owned a slice; the slices compose. |
| **F-Thread (vote)** | Count agreement. ≥ ⌈N/2⌉+1 agree → that answer wins. Disagreement → escalate to user. |
| **F-Thread (diff)** | Show user the N outputs side-by-side. User picks or cherry-picks. |
| **F-Thread (cherry-pick)** | Take the strongest part of each — only when outputs are structured (e.g. YAML lists you can union). |
| **Scout** | Discard scout's code. Extract the **lessons** (files touched, blockers found) into the next prompt. |

**Reviewer F-Thread special case:**

When voting reviewer agents (e.g. 3× `rcc:skill-reviewer`), if YAML outputs disagree on `pass`, the safe default is **fail** — any reviewer flagging an issue counts.

**Verification:** A single artifact (decision, file, report) emerges from N inputs.

## Task 4: Report to User

**Goal:** Make the parallel dispatch legible.

**Report shape:**

- State the pattern: "Ran F-Thread, 3 reviewers."
- Show the merge: "All 3 passed" or "2 pass / 1 fail — flagging the failing concern."
- Surface dissent — never silently drop the minority output.

**Verification:** User can audit which agent said what without re-running.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "I'll just run them one at a time, it's the same thing"
- "Fanout is overkill for this"
- "Best-of-N for everything makes results better"
- "I'll fan out 5 agents to edit the same file"
- "Scout is wasteful, just write the real prompt"
- "Hide the dissenting reviewer, the others passed"

**All of these mean: You're about to lose the value of parallel dispatch. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Serial is simpler" | Serial costs N× wall-clock. The whole point is the wall-clock saving. |
| "More agents = better answer" | F-Thread costs N× tokens. Use it for judgment-heavy questions, not lookups. |
| "Scout is throwaway, skip it" | The scout's blockers are intel. Skipping = re-discovering them yourself. |
| "Fanout writes are fine" | Two agents writing the same file race. Fanout writes only on disjoint slices. |
| "Pick the best output silently" | The user can't audit a hidden decision. Surface dissent. |

## References

- [writing-subagents](../writing-subagents/SKILL.md) — design agents that survive fanout
- User-level `investigating` skill — scout pattern detail (lives outside this plugin)
