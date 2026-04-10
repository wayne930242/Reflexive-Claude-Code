---
name: writing-rules
description: "Use when adding project conventions or scoping guidelines. For this plugin: use CLAUDE.md for all conventions. Use when user says 'add convention', 'scope guideline'. NOT for current workflow (rules mechanism not implemented)."
---

# Writing Rules

## Overview

**Writing rules IS creating scoped, auto-injected conventions.**

Rules auto-inject into context when files match their `paths:` glob. Keep them concise—every line costs tokens.

**Core principle:** Rules = path-scoped conventions with auto-injection. CLAUDE.md = broad project instructions. For this plugin project: use CLAUDE.md for all guidelines—rules mechanism not currently implemented.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Skill Steps
**Handoff:** none
**Next:** none

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[writing-rules] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Analyze requirements
2. RED - Test without rule
3. GREEN - Write rule file
4. Validate structure
5. REFACTOR - Quality review
6. Test activation

Announce: "Created 6 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## TDD Mapping for Rules

| TDD Phase | Rule Creation | What You Do |
|-----------|---------------|-------------|
| **RED** | Test without rule | Work on matching files, note inconsistencies |
| **Verify RED** | Document gaps | Note where conventions were forgotten |
| **GREEN** | Write rule | Create `.claude/rules/` file addressing gaps |
| **Verify GREEN** | Test injection | Verify rule activates on matching files |
| **REFACTOR** | Optimize scope | Tighten `paths:` globs, reduce line count |

## Task 1: Analyze Requirements

**Goal:** Understand what convention to encode and where it applies.

**Questions to answer:**
- What convention needs enforcement?
- Which files should this apply to?
- Does this belong in CLAUDE.md (broad, always loaded) or rules (path-scoped)?
- Does this rule already exist?

**Decision tree:**

```dot
digraph rule_decision {
    rankdir=TB;

    start [label="New directive needed", shape=doublecircle];
    q1 [label="Applies to\nall files?", shape=diamond];
    q3 [label="Contains steps\nor code?", shape=diamond];
    q4 [label="CLAUDE.md\nalready > 180 lines?", shape=diamond];

    claudemd [label="CLAUDE.md"];
    global_rule [label="Global rule\n(no paths)"];
    scoped_rule [label="Path-scoped rule"];
    skill [label="Not a rule\nuse writing-skills"];

    start -> q1;
    q1 -> q3 [label="yes"];
    q1 -> scoped_rule [label="no"];
    q3 -> skill [label="yes"];
    q3 -> q4 [label="no"];
    q4 -> global_rule [label="yes"];
    q4 -> claudemd [label="no"];
}
```

**Verification:** Can state the convention in one sentence and specify the glob pattern.

## Task 2: RED - Test Without Rule

**Goal:** Work on matching files WITHOUT the rule. Note where convention is forgotten.

**Process:**
1. Identify 2-3 files that would match the rule
2. Ask agent to modify those files
3. Observe if conventions are followed naturally
4. Document specific violations

**Verification:** Documented at least 1 instance where convention was not followed.

## Task 3: GREEN - Write Rule File

**Goal:** Create rule file addressing the gaps you documented.

### Rule Location

```
~/.claude/rules/             # User-level (global, all projects)
.claude/rules/               # Project-level
├── code-style.md            # Global rule (no paths:)
├── api/
│   └── conventions.md       # paths: ["src/api/**"]
└── testing/
    └── guidelines.md        # paths: ["**/*.test.ts"]
```

### Rule Format

```yaml
---
paths:                        # Omit for global rules
  - "src/api/**/*.ts"
---

# Rule Title

- Constraint 1 (imperative: "MUST", "NEVER")
- Constraint 2
```

### Injection Mechanism

Rules are Markdown content injected into context (same as CLAUDE.md):
- **No `paths`** → loaded at session start (always active, like CLAUDE.md)
- **With `paths`** → loaded when Claude reads a file matching the glob
- There is no special "rule blob" format — the rule body IS the injected content
- User-level `~/.claude/rules/` loads before project-level `.claude/rules/` (project takes precedence)
- Symlinks are supported for sharing rules across projects

### Writing Rules

**CRITICAL constraints:**
- **< 50 lines** - Auto-injected = expensive tokens
- **Imperative form** - "MUST use", not "try to use"
- **No procedures** - How-to belongs in skills
- **Specific globs** - Narrow scope = fewer injections

<Good>
```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API Conventions

- MUST validate all input with zod
- MUST return { data, error } shape
- NEVER expose internal errors to client
```
Specific, imperative, scoped.
</Good>

<Bad>
```yaml
---
# No paths = global!
---

# Guidelines

- Try to validate input
- Consider using consistent response shapes
- It's good practice to handle errors
```
Vague, unscoped, passive.
</Bad>

**Content validation checks:**

| Check | Fail condition | Action |
|-------|---------------|--------|
| Line count | > 50 lines | Must simplify or split |
| Procedural content | Contains numbered steps, multi-line code blocks | Extract to skill, rule keeps principle only |
| paths missing | Content targets specific file types but no `paths:` | Must add |
| Load budget | Adding this rule pushes session-start total > 300 lines | Warn, suggest path-scoped |

**Verification:**
- [ ] Has frontmatter with `paths:` (or intentionally global with justification)
- [ ] < 50 lines
- [ ] Imperative language ("MUST", "NEVER")
- [ ] No procedural content (steps, code blocks as process)
- [ ] Not duplicating existing rules or CLAUDE.md
- [ ] Session-start total (CLAUDE.md + global rules) still under 300 lines

## Task 4: Validate Structure

**Goal:** Verify rule file structure is correct.

**Checklist:**
- [ ] File is in `.claude/rules/` directory
- [ ] Frontmatter has valid `paths:` glob (or none for global)
- [ ] Body < 50 lines
- [ ] Uses imperative language
- [ ] No how-to instructions (belongs in skills)
- [ ] Not duplicating content already in CLAUDE.md

**Verification:** All checklist items pass.

## Task 5: REFACTOR - Quality Review

**Goal:** Have rule reviewed by rule-reviewer subagent.

```
Agent tool:
- subagent_type: "rcc:rule-reviewer"
- prompt: "Review rule at [path]"
```

**Outcomes:**
- **Pass** → Proceed to Task 6
- **Needs Fix** → Fix issues, re-run reviewer, repeat until Pass
- **Fail** → Major problems, return to Task 3

**Verification:** rule-reviewer returns "Pass" rating.

## Task 6: Test Activation

**Goal:** Verify rule actually activates on matching files.

**Process:**
1. Create/open a file matching the `paths:` pattern
2. Ask agent to modify it
3. Verify agent mentions or follows the rule
4. If global rule, verify it appears in all contexts

**Verification:**
- Rule activates when working on matching files
- Agent follows the conventions in the rule

## Glob Pattern Reference

| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/api/**` | All under src/api/ |
| `*.md` | Markdown in root only |
| `{src,lib}/**/*.ts` | Multiple directories |
| `**/*.{ts,tsx}` | Multiple extensions |
| `!**/node_modules/**` | Exclude pattern |

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "This should be in CLAUDE.md, but I'll make it a rule"
- "I don't need paths:, it applies everywhere"
- "50 lines is too restrictive"
- "Skip baseline, I know what's needed"
- "Add how-to instructions here"
- "One big rule is better than multiple small ones"
- "This rule applies to everything" (really? try adding paths)
- "I need to explain the steps" (that is a skill, not a rule)
- "Let me add a code example" (a rule is a directive, not a tutorial)

**All of these mean: You're about to create a weak rule. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "CLAUDE.md is overkill" | If it applies broadly to all work, it belongs in CLAUDE.md. |
| "Global rules are fine" | Global = always injected. Scope it properly. |
| "50 lines is arbitrary" | 50 lines × N matches = massive token cost. |
| "I can add procedures here" | Rules = what. Skills = how. Keep them separate. |
| "One comprehensive rule" | Multiple focused rules > one bloated rule. |

## Flowchart: Rule Creation

```dot
digraph rule_creation {
    rankdir=TB;

    start [label="Need rule", shape=doublecircle];
    analyze [label="Task 1: Analyze\nrequirements", shape=box];
    is_broad [label="Applies to\nall work?", shape=diamond];
    use_claudemd [label="Put in\nCLAUDE.md", shape=box, style=filled, fillcolor="#ffcccc"];
    baseline [label="Task 2: RED\nTest without rule", shape=box, style=filled, fillcolor="#ffcccc"];
    write [label="Task 3: GREEN\nWrite rule", shape=box, style=filled, fillcolor="#ccffcc"];
    validate [label="Task 4: Validate\nstructure", shape=box];
    review [label="Task 5: REFACTOR\nQuality review", shape=box, style=filled, fillcolor="#ccccff"];
    review_pass [label="Review\npassed?", shape=diamond];
    test [label="Task 6: Test\nactivation", shape=box];
    done [label="Rule complete", shape=doublecircle];

    start -> analyze;
    analyze -> is_broad;
    is_broad -> use_claudemd [label="yes"];
    is_broad -> baseline [label="no"];
    baseline -> write;
    write -> validate;
    validate -> review;
    review -> review_pass;
    review_pass -> test [label="pass"];
    review_pass -> write [label="fail"];
    test -> done;
}
```

## References

- [references/paths-patterns.md](references/paths-patterns.md) - Advanced glob patterns
- [references/examples.md](references/examples.md) - Rule examples by domain
