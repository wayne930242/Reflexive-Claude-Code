---
name: writing-claude-md
description: Use when creating CLAUDE.md, improving existing CLAUDE.md, or setting up project configuration. Use when user says "create CLAUDE.md", "setup project", "configure agent".
---

# Writing CLAUDE.md

## Overview

**Writing CLAUDE.md IS establishing project memory that persists across sessions.**

CLAUDE.md is context, not enforced configuration. Claude treats it as high-priority guidance loaded every session. For deterministic enforcement, use hooks.

**Core principle:** Only include what Claude can't figure out from reading the code. Specific and verifiable > vague and aspirational.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Skill Steps
**Handoff:** none
**Next:** none

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[writing-claude-md] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
0. Fetch latest official memory/CLAUDE.md spec
1. Analyze current state
2. Identify documentation gaps
3. Design instruction structure
4. Write CLAUDE.md
5. Add project content
6. Validate structure
7. Review and optimize
8. Test with new session

Announce: "Created 9 tasks (0–8). Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## Task 0: Fetch Latest Official Spec

**Goal:** Pull the current Anthropic CLAUDE.md / memory spec before designing — never trust cached memory.

**Action:**
```
Skill tool: fetching-claude-docs
  component: memory
  question: "CLAUDE.md location precedence (project/user/local), import syntax,
             auto-loading behavior, token cost, recommended structure"
```

**Verification:** Received YAML with `source: https://code.claude.com/docs/en/memory.md` and non-empty `spec_excerpt`. Use as authoritative reference; if any rule in this SKILL conflicts with the fetched spec, the fetched spec wins.

## Task 1: Analyze Current State

**Goal:** Understand what exists and what's needed.

**If CLAUDE.md exists:**
1. Read current content
2. Check length (target: < 200 lines)
3. Identify vague or unverifiable instructions
4. Check if content belongs elsewhere (rules, skills, hooks)

**If no CLAUDE.md:** Document what Claude would need to know that it can't learn from reading the code.

**Verification:** Can list specific instructions needed and why each can't be derived from code.

## Task 2: RED - Test Without Proper CLAUDE.md

**Goal:** Observe what Claude gets wrong without guidance.

**Process:**
1. Start session with weak/no CLAUDE.md
2. Ask Claude to perform common project tasks
3. Note where it uses wrong commands, wrong conventions, wrong paths
4. Document specific gaps (not vague "drift")

**What to look for:**
- Wrong build/test commands
- Incorrect assumptions about project structure
- Missing project-specific conventions
- Wrong language or communication style

**Verification:** Documented at least 2 specific things Claude got wrong.

## Task 3: GREEN - Write CLAUDE.md

**Goal:** Create specific, verifiable instructions addressing the gaps you documented.

**Before writing, walk through [prompt-design-principles.md](../../references/prompt-design-principles.md):**

- 5-skeleton framework — CLAUDE.md typically needs **Role** (what Claude does in this project), **Scope** (what's in/out), and **Standards** (concrete rules). Workflow and Completion usually live in skills / rules, not CLAUDE.md.
- Failure-mode reverse engineering — every `MUST` / `NEVER` line should trace to an observed or predicted failure (documented in Task 2 RED), not an aspirational wish.
- Conditional dispatch — avoid absolute rules that don't hold across all task variants.

### What to Include vs Exclude

**Filter every line through this question first:** "Can Claude derive this from reading the code, package.json, or running `ls`?" If yes, exclude — it's noise that pushes real signal out of attention budget.

The 2026 ETH Zürich study found that LLM-auto-generated CLAUDE.md files **reduced** task success by ~3% and increased cost ~20% precisely because they re-stated derivable content. The same study found that named tools/commands in CLAUDE.md are used ~160× more — confirming Claude reads it carefully, so every wasted line displaces a useful one.

**Three-axis frame (WHAT / WHY / HOW):**

- **WHAT** — non-obvious project identity Claude can't infer: monorepo layout, unusual subdirectory roles
- **WHY** — rationale for surprising choices: historical constraints, legal/compliance drivers, prior incidents
- **HOW** — non-default tooling and commands: `bun` not `npm`, `uv` not `pip`, custom build scripts, project-specific test filters

| Include (Claude can't guess) | Exclude (Claude already knows or can derive) |
|------------------------------|---------------------------------------------|
| Non-default tooling (`bun` not `npm`, `uv` not `pip`) | Standard language conventions |
| Build/test/deploy commands with project-specific flags | Things a linter or formatter enforces |
| Repo conventions (branch naming, PR format) | General programming practices |
| Why a surprising architecture exists (incident, constraint) | Big architecture overviews / directory listings (Claude can `ls`) |
| Environment quirks, gotchas, prior incidents | Detailed API docs (link instead) |
| Hidden invariants not visible in code | Restating what package.json / pyproject.toml already says |
| Anti-patterns previously caught in review | Aspirational "write clean code" / "follow best practices" |

### CLAUDE.md Structure

Sections: Code Style, Workflow, Architecture, Gotchas. See [references/examples.md](references/examples.md) for complete example.

### Writing Rules

Instructions MUST be **SPECIFIC**, **VERIFIABLE**, **NON-OBVIOUS**, and **ACTIONABLE**.

Use `MUST`/`NEVER`/`IMPORTANT` sparingly — if everything is critical, nothing is.

### When to Use Other Mechanisms Instead

| If the instruction is... | Use... |
|--------------------------|--------|
| A focused convention scoped to a directory or file glob | `.claude/rules/<name>.md` with `paths:` scope tag (still loads every session — split for budget, not for filtering) |
| A reusable multi-step workflow | A skill in `.claude/skills/` (loaded on-demand) |
| **Must NEVER be bypassed** (force-push protection, secret-commit block, destructive ops) | **A hook** with `exit 2` — text in CLAUDE.md is ~70% compliance, not 100%. Hard rules live in hooks. |
| Only relevant for certain tasks | A skill (loaded on-demand, saves tokens) |
| Specific to a subdirectory of a monorepo | A nested `CLAUDE.md` inside that subdirectory — Claude Code merges parent + child when working in that path |

### Conditional Dispatch (for instructions only relevant to specific tasks)

When a section only applies to certain task types (testing, deploying, migrating), wrap it in a conditional block instead of always-on prose. Claude reads the condition and skips the body when it doesn't apply, freeing attention budget for the rest of the file.

```markdown
<important if="writing or modifying tests">
- Use `createTestApp()` helper for integration tests
- Mock the database with `dbMock` (NEVER hit real DB in unit tests)
</important>

<important if="deploying to production">
- Run `bun build` locally first; CI does not auto-build
- Tag the release before pushing to main
</important>
```

Use this for: test setup, deploy steps, migration procedures, environment-specific gotchas. Do **not** wrap core identity (tech stack, build command, project layout) — those need to stay always-on.

### Nested CLAUDE.md (monorepos and multi-package repos)

Claude Code merges nested `CLAUDE.md` files: when working in `apps/api/handlers/foo.ts`, it loads root `CLAUDE.md` + `apps/CLAUDE.md` + `apps/api/CLAUDE.md` if they exist. Use this for monorepos:

- Root `CLAUDE.md`: project identity, top-level layout, shared commands
- `packages/<name>/CLAUDE.md`: package-specific tooling, test command, gotchas
- `apps/<name>/CLAUDE.md`: app-specific build, deploy, runtime quirks

Reference: OpenAI's Codex repo uses 88 nested CLAUDE.md files. For a 5+ package monorepo, a single 500-line root file is worse than five 80-line nested files.

### Hard Rules — Must Live in Hooks

CLAUDE.md text is advisory: empirical compliance is roughly 70%. For any rule where the 30% miss is unacceptable (force-pushing main, committing secrets, deleting prod data, bypassing pre-commit), encode it as a hook with `exit 2` so Claude is mechanically blocked, not asked nicely.

CLAUDE.md may *describe* the rule for human readers, but the **enforcement** must be a hook. If you find yourself writing `MUST NEVER` about a destructive action without a backing hook, you're shipping a 30%-broken safety net.

**Verification:**
- [ ] < 200 lines (hard target; 60 lines optimal)
- [ ] Every instruction is specific and verifiable
- [ ] No content that belongs in rules, skills, or hooks
- [ ] No vague/obvious guidance ("write clean code")
- [ ] No content that restates README, package.json, or visible directory layout
- [ ] No big architecture overviews / directory listings (Claude can `ls`)
- [ ] Uses emphasis words (`MUST`, `NEVER`) sparingly but effectively
- [ ] Every `MUST NEVER` about a destructive/irreversible action has a backing hook
- [ ] Task-specific instructions wrapped in `<important if="...">` conditional blocks where appropriate
- [ ] Monorepo: subdirectory-specific guidance moved to nested `CLAUDE.md` files, not crammed into root

## Task 4: Add Project Content

**Goal:** Add project-specific information that helps agent work effectively. Use the section structure from [references/examples.md](references/examples.md) as a starting point.

**Token efficiency:**
- CLAUDE.md loads every session — every line costs tokens
- Move domain knowledge to skills (loaded on-demand)
- Split focused conventions into `.claude/rules/<name>.md` (still loads every session, but keeps CLAUDE.md scannable)
- Link to detailed docs instead of inlining them

**Verification:** Total < 200 lines. Every line earns its place.

## Task 5: Validate Structure

**Goal:** Verify CLAUDE.md is effective and efficient.

**Checklist:**
- [ ] < 200 lines total
- [ ] Every instruction is specific and verifiable
- [ ] No content duplicated in `.claude/rules/` (rules are auto-loaded into context — do NOT Read or Grep rule files; compare against auto-loaded rule content already in context)
- [ ] No multi-step workflows (belongs in skills)
- [ ] No linter-enforceable rules (use hooks instead)
- [ ] Referenced paths actually exist
- [ ] Commands actually work

**Verification:** All checklist items pass.

## Task 6: REFACTOR - Quality Review

**Goal:** Have CLAUDE.md reviewed by claudemd-reviewer subagent.

```
Agent tool:
- subagent_type: "rcc:claudemd-reviewer"
- prompt: "Review CLAUDE.md at [path]"
```

**Interpret YAML output:**
- `pass: true` → Proceed to Task 7
- `pass: false` → Fix all issues listed, re-run reviewer, repeat until `pass: true`

**Verification:** claudemd-reviewer returns YAML with `pass: true`.

## Task 7: Test with New Session

**Goal:** Verify CLAUDE.md works in practice.

**Process:**
1. Start new Claude Code session in project
2. Ask Claude to perform common tasks
3. Verify it uses correct commands, follows conventions
4. Check it doesn't do things the CLAUDE.md says not to
5. If Claude asks questions answered in CLAUDE.md → phrasing is ambiguous, fix it

**Signs of a good CLAUDE.md:**
- Claude uses the right build/test commands without asking
- Claude follows project conventions automatically
- Claude doesn't need correction on documented gotchas

**Signs of a bad CLAUDE.md:**
- Claude ignores instructions → file too long, instruction lost in noise
- Claude asks questions answered in CLAUDE.md → phrasing is ambiguous
- Claude follows CLAUDE.md but breaks things → instructions are wrong/outdated

**Verification:** Claude follows documented conventions correctly over 5+ turns.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "Skip baseline test, I know what's needed"
- "Instructions can be general guidance"
- "Put all project details in CLAUDE.md"
- "200 lines is too restrictive"
- "Skip reviewer, it's obviously good"
- "Add instructions for things a linter can check"
- "Include standard language conventions"
- "Restate the README so Claude has the context handy" (it doesn't help — see ETH 2026 study, ~3% drop in success rate)
- "A big architecture overview helps Claude find files faster" (false — measured zero improvement on time-to-first-relevant-file)
- "Writing 'NEVER force-push' here will stop it" (no — that's ~70% compliance; needs a hook)
- "Cram every monorepo package's quirks into root CLAUDE.md" (use nested CLAUDE.md per package)
- "Always-on prose for test setup is fine" (use `<important if="writing tests">` instead)

**All of these mean: You're about to create a bloated, ineffective CLAUDE.md.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I know what instructions are needed" | You know what YOU think. Baseline reveals actual gaps. |
| "Instructions can be vague for flexibility" | Vague instructions = Claude interprets freely = no control. |
| "Everything goes in CLAUDE.md" | CLAUDE.md = always loaded = expensive. Use skills and rules. |
| "More instructions = better coverage" | More instructions = more noise = important ones get lost. |
| "Standard practices need documenting" | Claude already knows standard practices. Document the exceptions. |
| "Linter rules belong here" | Linter rules belong in linters + hooks. Deterministic > advisory. |

## References

- [references/examples.md](references/examples.md) — Complete CLAUDE.md example and good/bad instructions
- [references/flowchart.md](references/flowchart.md) — Full creation flowchart (Tasks 1–7)
- [../../references/prompt-design-principles.md](../../references/prompt-design-principles.md) — 5-skeleton framework, failure-mode reverse engineering, conditional dispatch, completion semantics
- Scaffold script: `${CLAUDE_SKILL_DIR}/scripts/init_claude_md.py` — generates initial CLAUDE.md from project structure
