# Agent File Specification

Synced against https://code.claude.com/docs/en/sub-agents.md (re-verify via `fetching-claude-docs` before relying on this file).

## Configuration Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase with hyphens: `code-reviewer`. Hooks receive it as `agent_type`; the filename need not match |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Omit = inherit every tool available to subagents. To preload skills use `skills`, not `Skill` here |
| `disallowedTools` | No | Tools to deny, removed from the inherited or specified list |
| `model` | No | `sonnet`, `opus`, `haiku`, `fable`, a full model ID (e.g. `claude-opus-5`), or `inherit`. Defaults to `inherit` |
| `maxTurns` | No | Maximum agentic turns before the subagent stops |
| `skills` | No | Skills preloaded into the subagent's context at startup — full content injected, not just the description |
| `permissionMode` | No | `default`, `manual` (alias for `default`), `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `effort` | No | `low`, `medium`, `high`, `xhigh`, `max` — available levels depend on the model |
| `isolation` | No | `worktree` = run in a temporary git worktree, branched from the default branch, auto-removed if unchanged |
| `background` | No | `true` = always run in background. When unset, Claude chooses (background by default) |
| `memory` | No | Persistent memory scope: `user`, `project`, `local` |
| `mcpServers` | No | MCP servers available to this subagent |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `color` | No | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | No | Auto-submitted first user turn when run as the main session agent (`--agent`) |

**Plugin agents note:** `hooks`, `mcpServers`, and `permissionMode` are ignored for plugin subagents.

**Not valid here:** `context` and `agent` are *skill* frontmatter fields. A subagent file that sets them is malformed.

## Skill with `context: fork` vs Custom Agent

| Approach | When to Use |
|----------|-------------|
| Skill + `context: fork` | Guidance-oriented, needs skill body as instructions |
| Custom agent file | Worker-oriented, needs specialized system prompt |
| Built-in subagent type | Standard tasks (explore, plan, general-purpose) |

### Context Isolation

**Important: Context isolation = context amnesia.** A skill with `context: fork` and a custom agent both start without the main conversation:

| | System prompt | Task | Also loads |
|---|---|---|---|
| Skill with `context: fork` | From the `agent` type (`general-purpose` if omitted) | SKILL.md content | CLAUDE.md, except when the agent is `Explore` or `Plan` |
| Custom agent file | The agent's markdown body | The delegating prompt | Preloaded `skills` + CLAUDE.md |

- Neither sees your conversation history — **design `argument-hint` to demand sufficient context**
- The exception is the built-in `fork` subagent type (`/subtask`), which *does* inherit the full conversation, system prompt, tools, and model. That is a different mechanism from a skill's `context: fork`

Good:
```yaml
argument-hint: "[file-or-directory-path] [specific-requirement]"
```
Forces user to provide target and intent.

Bad:
No argument-hint -> user types `/my-skill` with no args -> forked agent has zero context.

## Tool Permissions

**Important: Subagents cannot request permissions at runtime.** Unlike the main conversation where Claude can ask the user for tool approval, subagents only have access to tools declared upfront in their `tools` field.

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
