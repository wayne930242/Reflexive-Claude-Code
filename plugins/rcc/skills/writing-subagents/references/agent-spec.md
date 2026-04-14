# Agent File Specification

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase with hyphens: `code-reviewer` |
| `description` | Yes | Include "Use proactively when..." for auto-invoke |
| `tools` | No | CSV list; omit = inherit all |
| `disallowedTools` | No | Tools to exclude (more flexible than allowlist) |
| `model` | No | `sonnet`, `opus`, `haiku`, `inherit`, or full model ID |
| `maxTurns` | No | Maximum agentic turns |
| `skills` | No | Auto-load skills when invoked |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, `plan` |
| `effort` | No | `low`, `medium`, `high`, `max` (Opus 4.6 only) |
| `isolation` | No | `worktree` = run in temporary git worktree |
| `background` | No | `true` = always run in background |
| `memory` | No | Persistent memory scope: `user`, `project`, `local` |
| `mcpServers` | No | Available MCP servers |
| `hooks` | No | Lifecycle hooks |

**Plugin agents security note:** Plugin agents do NOT support `hooks`, `mcpServers`, or `permissionMode`.

## Skill with `context: fork` vs Custom Agent

| Approach | When to Use |
|----------|-------------|
| Skill + `context: fork` | Guidance-oriented, needs skill body as instructions |
| Custom agent file | Worker-oriented, needs specialized system prompt |
| Built-in subagent type | Standard tasks (explore, plan, general-purpose) |

### Context Isolation

**CRITICAL: Context isolation = context amnesia.** When using `context: fork` or custom agents:
- Forked context does NOT inherit the main conversation
- Only receives: skill body (or agent system prompt) + `$ARGUMENTS` (or agent prompt)
- **Design `argument-hint` to demand sufficient context**

Good:
```yaml
argument-hint: "[file-or-directory-path] [specific-requirement]"
```
Forces user to provide target and intent.

Bad:
No argument-hint -> user types `/my-skill` with no args -> forked agent has zero context.

## Tool Permissions

**CRITICAL: Subagents CANNOT request permissions at runtime.** Unlike the main conversation where Claude can ask the user for tool approval, subagents only have access to tools declared upfront in their `tools` field.

**Rules:**
- `tools` field = the COMPLETE set of available tools. No additions at runtime.
- Omitting `tools` = inherit ALL tools (use only when you trust the agent fully)
- Use `disallowedTools` as an alternative: inherit all EXCEPT listed tools
- Test tool access — verify the agent can do everything it needs

## Model Selection — Three-Layer Architecture

| Layer | Model | Role | Tool Constraint |
|-------|-------|------|-----------------|
| Orchestration (simple dispatch) | `haiku` | Explicit task list, direct assignment, no ambiguity | **Must have tools** (TaskCreate, Agent) — no tools = cannot orchestrate |
| Orchestration (complex decomposition) | `sonnet` | Ambiguous requirements, multi-level decisions, dynamic routing | Must have tools |
| Implementation | `sonnet` | Write, edit, analyze, implement | Full tools |
| Quality gate / Advisor | `opus` | Architectural reasoning, overlap detection, pass/fail judgment | Read-only only (`Read, Grep, Glob`) |

**Opus constraints (all required):**
1. Output must be structured and mechanically executable by downstream Sonnet (`{pass, issues[{file, line_range, action, reason}]}`)
2. Must have a revision loop (fail → Sonnet fixes → re-review). Without this, Opus review = expensive logger.
3. Judge only — no rewrites, no spec changes, no open-ended suggestions

**Haiku constraints:**
- As orchestrator: must have tools (TaskCreate, Agent dispatch)
- Zero-tool Haiku only works when content is pre-injected for pure reasoning — not suitable for document review (requires judgment)

**Use `inherit` when:** the agent does not need specific model capabilities; let the parent decide.

## Isolation Guide

| Use Case | Isolation | Rationale |
|----------|-----------|-----------|
| Read-only reviewer | (none) | No file changes, no conflict risk |
| Code generation that may conflict | `worktree` | Isolated git worktree prevents conflicts with main workspace |
| Parallel writing agents | `worktree` | Each gets its own copy of the repo |

## Effort Guide

| Use Case | Effort | Rationale |
|----------|--------|-----------|
| Static analysis, review | `medium` | Sufficient for pattern matching and checklist evaluation |
| Complex architecture decisions | `high` | Needs deeper reasoning |
| Simple formatting, lookup | `low` | Minimal reasoning needed |
