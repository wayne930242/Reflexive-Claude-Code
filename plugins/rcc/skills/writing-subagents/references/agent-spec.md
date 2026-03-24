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

## Model Selection

| Model | Use Case | Cost |
|-------|----------|------|
| `haiku` | Fast exploration, simple validation | $ |
| `sonnet` | Balanced (default) | $$ |
| `opus` | Complex reasoning, architecture | $$$ |
