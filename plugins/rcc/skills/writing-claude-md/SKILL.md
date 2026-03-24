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

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[writing-claude-md] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Analyze current state
2. RED - Test without proper CLAUDE.md
3. GREEN - Write CLAUDE.md
4. Add project content
5. Validate structure
6. REFACTOR - Quality review
7. Test with new session

Announce: "Created 7 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## TDD Mapping for CLAUDE.md

| TDD Phase | CLAUDE.md Creation | What You Do |
|-----------|-------------------|-------------|
| **RED** | Test without CLAUDE.md | Observe agent missing conventions, using wrong commands |
| **Verify RED** | Document gaps | Note what Claude got wrong or had to guess |
| **GREEN** | Write CLAUDE.md | Create specific instructions addressing gaps |
| **Verify GREEN** | Test in new session | Verify Claude follows instructions correctly |
| **REFACTOR** | Trim and sharpen | Remove redundant/obvious content, improve specificity |

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

### What to Include vs Exclude

| Include (Claude can't guess) | Exclude (Claude already knows) |
|------------------------------|--------------------------------|
| Non-obvious bash commands for build/test/deploy | Standard language conventions |
| Code style rules that differ from defaults | Things a linter enforces |
| Repo conventions (branch naming, PR format) | General programming practices |
| Architecture decisions and their rationale | What's obvious from reading code |
| Development environment quirks (env vars, setup) | Detailed API docs (link instead) |
| Common gotchas or non-obvious behavior | Frequently changing information |

### CLAUDE.md Structure

```markdown
# Project Name

One-line description.

## Code Style

- Use 2-space indentation (not 4)
- MUST use ES modules (import/export), NOT CommonJS (require)
- Prefer named exports over default exports

## Workflow

- Run `npm test -- --filter [name]` for single test (NOT full suite)
- MUST typecheck with `npx tsc --noEmit` before committing
- Branch naming: `feature/TICKET-123-description`

## Architecture

- API handlers: `src/api/handlers/`
- Database models: `src/db/models/`
- Shared types: `src/types/` (single source of truth)

## Gotchas

- The `auth` middleware caches tokens for 5 min — restart dev server after changing auth logic
- `npm run build` must complete before `npm run e2e` (no watch mode for e2e)
```

### Writing Rules

Instructions MUST be:
- **SPECIFIC** — "Use 2-space indentation" not "Format code properly"
- **VERIFIABLE** — Can objectively check compliance
- **NON-OBVIOUS** — Claude wouldn't know this from reading code
- **ACTIONABLE** — Tells agent exactly what to do/not do

**Use emphasis for critical rules:**
- `MUST`, `NEVER`, `IMPORTANT` increase adherence
- But use sparingly — if everything is critical, nothing is

<Good>
```markdown
- MUST validate all API input with zod schemas before processing
- Run `pytest -x --tb=short` for quick test feedback (NOT `pytest` alone)
```
Specific, verifiable, non-obvious.
</Good>

<Bad>
```markdown
- Write clean, maintainable code
- Test your changes thoroughly
- Follow best practices
```
Vague, obvious, unverifiable. Claude already tries to do these.
</Bad>

### When to Use Other Mechanisms Instead

| If the instruction is... | Use... |
|--------------------------|--------|
| Scoped to specific file paths | `.claude/rules/` with `paths:` glob |
| A reusable multi-step workflow | A skill in `.claude/skills/` |
| Must be deterministically enforced | A hook in settings (exit code 2 = block) |
| Only relevant for certain tasks | A skill (loaded on-demand, saves tokens) |

**Verification:**
- [ ] < 200 lines (hard target; 60 lines optimal)
- [ ] Every instruction is specific and verifiable
- [ ] No content that belongs in rules, skills, or hooks
- [ ] No vague/obvious guidance ("write clean code")
- [ ] Uses emphasis words (`MUST`, `NEVER`) sparingly but effectively

## Task 4: Add Project Content

**Goal:** Add project-specific information that helps agent work effectively.

**Sections to consider:**
1. **Code Style** — Only conventions that differ from defaults
2. **Workflow** — Build, test, deploy commands and patterns
3. **Architecture** — Key directories and their purpose
4. **Gotchas** — Non-obvious behavior, environment quirks

**Token efficiency:**
- CLAUDE.md loads every session — every line costs tokens
- Move domain knowledge to skills (loaded on-demand)
- Move path-scoped conventions to rules (loaded when relevant)
- Link to detailed docs instead of inlining them

**Verification:** Total < 200 lines. Every line earns its place.

## Task 5: Validate Structure

**Goal:** Verify CLAUDE.md is effective and efficient.

**Checklist:**
- [ ] < 200 lines total
- [ ] Every instruction is specific and verifiable
- [ ] No content duplicated in `.claude/rules/`
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

**Outcomes:**
- **Pass** → Proceed to Task 7
- **Needs Fix** → Fix issues, re-run reviewer, repeat until Pass
- **Fail** → Major problems, return to Task 3

**Verification:** claudemd-reviewer returns "Pass" rating.

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

## Flowchart: CLAUDE.md Creation

```dot
digraph claudemd_creation {
    rankdir=TB;

    start [label="Need CLAUDE.md", shape=doublecircle];
    analyze [label="Task 1: Analyze\ncurrent state", shape=box];
    baseline [label="Task 2: RED\nTest without CLAUDE.md", shape=box, style=filled, fillcolor="#ffcccc"];
    verify_red [label="Gaps\ndocumented?", shape=diamond];
    write [label="Task 3: GREEN\nWrite instructions", shape=box, style=filled, fillcolor="#ccffcc"];
    content [label="Task 4: Add\nproject content", shape=box];
    validate [label="Task 5: Validate\nstructure", shape=box];
    too_long [label="< 200\nlines?", shape=diamond];
    extract [label="Extract to\nrules/skills", shape=box];
    review [label="Task 6: REFACTOR\nQuality review", shape=box, style=filled, fillcolor="#ccccff"];
    review_pass [label="Review\npassed?", shape=diamond];
    test [label="Task 7: Test\nnew session", shape=box];
    test_pass [label="Works?", shape=diamond];
    done [label="CLAUDE.md complete", shape=doublecircle];

    start -> analyze;
    analyze -> baseline;
    baseline -> verify_red;
    verify_red -> write [label="yes"];
    verify_red -> baseline [label="no\nmore tasks"];
    write -> content;
    content -> validate;
    validate -> too_long;
    too_long -> review [label="yes"];
    too_long -> extract [label="no"];
    extract -> validate;
    review -> review_pass;
    review_pass -> test [label="pass"];
    review_pass -> write [label="fail\nfix issues"];
    test -> test_pass;
    test_pass -> done [label="yes"];
    test_pass -> write [label="no\nimprove"];
}
```

## References

- Script: `scripts/init_claude_md.py`
