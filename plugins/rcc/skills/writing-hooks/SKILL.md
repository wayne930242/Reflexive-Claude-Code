---
name: writing-hooks
description: Use when creating Claude Code hooks for code quality, static analysis, or workflow automation. Use when user says "add hook", "enforce linting", "add pre-commit check", "block bad code".
---

# Writing Hooks

## Overview

**Writing hooks IS creating automated quality gates.**

Hooks run on Claude Code events (PreToolUse, PostToolUse, etc.) and can block actions with exit code 2.

**Core principle:** Hooks enforce what humans forget. Fast checks only—slow hooks kill productivity.

**Violating the letter of the rules is violating the spirit of the rules.**

## Routing

**Pattern:** Skill Steps
**Handoff:** none
**Next:** none

## Task Initialization (MANDATORY)

Before ANY action, create task list using TaskCreate:

```
TaskCreate for EACH task below:
- Subject: "[writing-hooks] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Tasks:**
1. Analyze requirements
2. RED - Test without hook
3. GREEN - Write hook script
4. Configure settings.json
5. Validate behavior
6. Test blocking
7. REFACTOR - Quality review

Announce: "Created 7 tasks. Starting execution..."

**Execution rules:**
1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after verification passes
3. If task fails → stay in_progress, diagnose, retry
4. NEVER skip to next task until current is completed
5. At end, `TaskList` to confirm all completed

## TDD Mapping for Hooks

| TDD Phase | Hook Creation | What You Do |
|-----------|---------------|-------------|
| **RED** | Test without hook | Write code, observe quality issues slip through |
| **Verify RED** | Document violations | Note specific issues that should be caught |
| **GREEN** | Write hook | Create script that catches those issues |
| **Verify GREEN** | Test blocking | Verify exit code 2 blocks violating code |
| **REFACTOR** | Optimize speed | Reduce hook runtime, filter file types |

## Task 1: Analyze Requirements

**Goal:** Understand what quality gate to create.

**Questions to answer:**
- What violation should be blocked?
- Which files should be checked?
- What tool/command performs the check?
- What event triggers the hook?
- What is the project's primary language? (check `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `*.csproj`, etc.)

**Event Selection:**

| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool runs | Block bad writes before they happen |
| `PostToolUse` | After tool runs | Validate written code |
| `UserPromptSubmit` | Before prompt processed | Add context to prompts |

**Verification:** Can describe the violation and the command to detect it.

## Task 2: RED - Test Without Hook

**Goal:** Write code WITHOUT the hook. Observe violations that slip through.

**Process:**
1. Ask agent to write code in the target file type
2. Intentionally introduce the violation (bad format, type error, etc.)
3. Observe that Claude Code doesn't catch it
4. Document the specific violation

**Verification:** Documented at least 1 violation that should have been caught.

## Task 3: GREEN - Write Hook Script

**Goal:** Create Python script that catches the violations you documented.

### Hook Structure

```
.claude/hooks/
├── eslint_check.py
├── prettier_check.py
└── typecheck.py
```

### Exit Code Contract

| Code | Meaning | Effect |
|------|---------|--------|
| 0 | Pass | Continue, stdout shown in verbose |
| 2 | Block | Action blocked, stderr fed to Claude |
| Other | Warning | Continue, stderr shown in verbose |

### Hook Template

See [references/static-checks.md](references/static-checks.md) for complete hook templates. For performance-optimized security hooks, see [references/performance-optimization.md](references/performance-optimization.md). Key pattern: read JSON from stdin, filter by extension, run check, exit 2 to block.

### Critical Requirements

- **Fast** - Under 5 seconds, hooks run synchronously
- **Performance constraints** - Total execution < 30s, parallel processing support
- **Graceful degradation** - Handle timeouts without blocking development
- **Filter files** - Only check relevant extensions  
- **Limit output** - First 5-10 errors, not all
- **Language** - Use project's primary language if detectable (Node.js script for JS/TS projects, Go for Go projects, etc.); default to Python when unclear or mixed
- **Progressive checks** - Fast/standard/thorough modes based on context
- **Cross-platform** - Must work on macOS, Linux, AND Windows

### Windows Compatibility (MANDATORY)

**CRITICAL:** Read [cross-platform-scripts.md](../../references/cross-platform-scripts.md) for full cross-platform rules covering paths, shell commands, line endings, and common pitfalls.

**Verification:**
- [ ] Script is executable (`chmod +x`) — skip on Windows
- [ ] Returns exit code 0 for valid files
- [ ] Returns exit code 2 for violations
- [ ] Runs under 5 seconds
- [ ] Uses `pathlib.Path` for all path operations
- [ ] No `shell=True` with string commands (use list args)
- [ ] No hardcoded `/tmp/` or path separators

## Task 4: Configure settings.json

**Goal:** Register hook in `.claude/settings.json`.

**CRITICAL:** Use `.claude/settings.json`, NOT `settings.local.json`. Settings are team-shared.

### Configuration Format

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/eslint_check.py",
          "timeout": 30
        }]
      }
    ]
  }
}
```

### Matcher Patterns

| Matcher | Matches |
|---------|---------|
| `Write\|Edit` | Write or Edit tools |
| `Bash` | Bash tool only |
| `.*` | All tools |

**Verification:**
- [ ] Hook registered in correct event
- [ ] Matcher targets correct tools
- [ ] Command path uses `$CLAUDE_PROJECT_DIR`
- [ ] Timeout is reasonable (5-30 seconds)

## Task 5: Validate Behavior

**Goal:** Verify hook script works correctly.

**Test command:**
```bash
echo '{"tool_input":{"file_path":"test.ts"}}' | .claude/hooks/your_hook.py
echo $?  # Should be 0 (pass) or 2 (block)
```

**Checklist:**
- [ ] Valid file returns exit code 0
- [ ] Invalid file returns exit code 2
- [ ] Errors go to stderr, info to stdout
- [ ] Completes under 5 seconds

**Verification:** Manual test passes for both valid and invalid inputs.

## Task 6: Test Blocking

**Goal:** Verify hook actually blocks bad code in Claude Code.

**Process:**
1. Ask Claude to write code with the violation
2. Observe hook blocks the action
3. Verify error message is fed back to Claude
4. Claude should fix and retry

**Verification:**
- Hook blocks violating code
- Claude receives feedback and fixes the issue

## Task 7: REFACTOR - Quality Review

**Goal:** Have hook reviewed by hook-reviewer subagent.

```
Agent tool:
- subagent_type: "rcc:hook-reviewer"
- prompt: "Review hook at [path/to/hook] with settings at [path/to/.claude/settings.json]"
```

**Interpret YAML output:**
- `pass: true` → Hook complete
- `pass: false` → Fix all issues listed, re-run reviewer, repeat until `pass: true`

**This is the REFACTOR phase:** Close loopholes identified by reviewer.

**Verification:** hook-reviewer returns YAML with `pass: true`.

## Common Hook Patterns

See [references/static-checks.md](references/static-checks.md) for linting, type checking, and auto-fix examples.

## Red Flags - STOP

These thoughts mean you're rationalizing. STOP and reconsider:

- "Hooks are overkill for this project"
- "I'll just remember to run linting"
- "5 seconds is too strict"
- "Check all files, not just changed ones"
- "Skip testing, the logic is simple"
- "Use settings.local.json for team hooks"

**All of these mean: You're about to create a weak hook. Follow the process.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll remember to lint" | You won't. Hooks enforce what humans forget. |
| "Slow hooks are thorough" | Slow hooks = disabled hooks. Keep it fast. |
| "Check everything" | Full project check = 30+ seconds. Check changed file only. |
| "settings.local.json" | Local = not shared. Team hooks go in settings.json. |
| "Simple logic doesn't need tests" | Hook failures are silent. Always test. |

## Flowchart: Hook Creation

```dot
digraph hook_creation {
    rankdir=TB;

    start [label="Need hook", shape=doublecircle];
    analyze [label="Task 1: Analyze\nrequirements", shape=box];
    baseline [label="Task 2: RED\nTest without hook", shape=box, style=filled, fillcolor="#ffcccc"];
    write [label="Task 3: GREEN\nWrite hook script", shape=box, style=filled, fillcolor="#ccffcc"];
    config [label="Task 4: Configure\nsettings.json", shape=box];
    validate [label="Task 5: Validate\nbehavior", shape=box];
    validate_pass [label="Tests\npassed?", shape=diamond];
    test [label="Task 6: Test\nblocking", shape=box];
    review [label="Task 7: REFACTOR\nQuality review", shape=box, style=filled, fillcolor="#ccccff"];
    review_pass [label="Review\npassed?", shape=diamond];
    done [label="Hook complete", shape=doublecircle];

    start -> analyze;
    analyze -> baseline;
    baseline -> write;
    write -> config;
    config -> validate;
    validate -> validate_pass;
    validate_pass -> test [label="yes"];
    validate_pass -> write [label="no"];
    test -> review;
    review -> review_pass;
    review_pass -> done [label="pass"];
    review_pass -> write [label="fail\nfix issues"];
}
```

## References

- [references/static-checks.md](references/static-checks.md) - Complete hook examples
- [references/events.md](references/events.md) - Hook events reference
- [references/performance-optimization.md](references/performance-optimization.md) - Performance-optimized security hooks with parallel execution
- [references/ai-security-checks.md](references/ai-security-checks.md) - AI-powered security validation patterns
- Scaffold script: `${CLAUDE_SKILL_DIR}/scripts/add_hook.py` — scaffolds a new hook file and registers it in settings.json
