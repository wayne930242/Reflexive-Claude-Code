# Prompt Design Principles

Shared reference for `writing-claude-md`, `writing-skills`, `writing-subagents`.

Distilled from post-hoc analysis of agent-facing prompts that reliably produce high-quality output.
Use as an evaluation checklist during the **Design** phase of each writing skill — before writing the body, walk through this file and confirm each principle is addressed.

This file deliberately does not repeat guidance that's already strong in the individual writing skills (naming, frontmatter format, line limits, reviewer loops).
It captures what was previously implicit.

## 1. The 5-Skeleton Framework

Every successful agent-facing prompt has these load-bearing layers. If a layer is missing or vague, the prompt is weaker than it looks.

| Layer | Question it answers | What concrete content looks like |
|-------|---------------------|----------------------------------|
| **Role** | What's the agent's relationship to the user and the task? | Not "you are an expert." State the job, the relationship (reviewer / implementer / designer-to-manager), and what the agent is expected to produce. |
| **Scope** | What does this prompt cover and not cover? | Explicit in-scope / out-of-scope bullets, or a dispatch table of task variants. |
| **Workflow** | How does the agent get from input to output? | Numbered procedure with a verification step attached to every stage. |
| **Standards** | What counts as good output vs. bad output? | Concrete do / don't rules with examples. No adjectives-only sentences. |
| **Completion** | What does "done" mean operationally? | A verifiable criterion (file opens cleanly, reviewer returns `pass: true`, tests green, no console errors). |

**Evaluation prompt:** "For each of the 5 layers, what specific content in this prompt satisfies it?" If the answer to any layer is abstract or missing, rewrite that layer.

## 2. Failure-Mode Reverse Engineering

Strong Red Flags sections are reverse-engineered from observed failures, not forward-engineered from aspirational wish-lists.

**Weak (aspirational):**
> Write clean, maintainable code.

**Strong (failure-driven):**
> Files over 1000 lines are a red flag — split them. Every abstraction must have at least two callers; delete single-use abstractions.

**Methodology during Design:**

1. List 5+ concrete ways an agent has gotten (or would get) this type of task wrong.
2. Write one rule against each.
3. Place these in **Red Flags** and **Common Rationalizations** sections.

The Red Flags section should read like a transcript of past mistakes, not a list of virtues.

**Signals the Red Flags section is too abstract:**

- Uses adjectives instead of behaviors ("be careful," "be thorough").
- Doesn't name the shortcut the agent is tempted to take.
- Could be copy-pasted into an unrelated skill unchanged.

## 3. Conditional Dispatch Over Absolute Rules

Absolute rules ("always X") fail because tasks differ. Conditional rules ("when X, do Y; when Z, do W") scale.

**Weak pattern:**

> Always explain your reasoning. Always provide three options. Always ask clarifying questions.

**Strong pattern:**

> For a new project or ambiguous requirement, ask before starting.
> For a follow-up tweak on an existing artifact, act directly.
> For a design exploration, produce 3+ variants.
> For a bug fix, produce one fix plus the test that reproduces it.

**How to apply during Design:**

1. List the 3–5 concrete task variants this skill / prompt will handle.
2. Write the correct behavior for each.
3. Only promote to an absolute rule if it genuinely holds for every variant.

## 4. Creative-Constraint Balance

Creative prompts that only diverge produce chaos. Disciplined prompts that only converge produce boring, generic output. Strong prompts do both — on different axes.

| Axis | Diverge (encourage variation) | Converge (enforce discipline) |
|------|-------------------------------|-------------------------------|
| Form / presentation | Yes — multiple variants, novel layouts, different framings. | — |
| Content / facts | — | Yes — no hallucinated APIs, no invented brand elements, no fabricated citations. |
| Process / workflow | — | Yes — required steps, verification gates, completion protocol. |
| Tooling / side effects | — | Yes — explicit tool-use order, preconditions, destructive-action guards. |

**Application:** When designing a skill, explicitly decide what can vary and what must be fixed. Write rules for each.

## 5. Completion Protocol Semantics

"Done" ≠ "I produced output." Completion must be defined operationally so the agent can self-verify.

Examples by task type:

- **Artifact task:** file exists + opens cleanly + no console errors + reviewer returns `pass: true`.
- **Analysis task:** output answers the N specific questions listed in the task brief.
- **Refactor task:** tests pass before AND after; no new lint warnings; behavior unchanged.
- **Documentation task:** link target exists + example commands run successfully + < line limit.

**Weak completion criteria** ("the work is done") cause open-ended loops and silent incompletion.
**Strong completion criteria** let the agent terminate confidently and let a reviewer verify independently.

The final task in every skill should be a verification step with a binary outcome, not a narrative summary.

## How to Use This File

When invoking `writing-claude-md`, `writing-skills`, or `writing-subagents`, during the **Design** phase:

1. Walk through the 5-skeleton framework — confirm each layer has concrete content.
2. When drafting Red Flags, apply failure-mode reverse engineering.
3. When drafting task-level guidance, prefer conditional dispatch over absolute rules.
4. Decide explicitly which axes diverge vs. converge.
5. Define completion operationally, not narratively.

If any step above cannot be answered concretely, the prompt is not ready to ship.
