# Official Plugin Structure Rules

## Directory Layout

| Rule | Correct | Wrong |
|------|---------|-------|
| Manifest location | `.claude-plugin/plugin.json` | root `plugin.json` |
| Components location | `skills/`, `commands/`, `agents/` at root | Inside `.claude-plugin/` |
| Paths in config | Relative `./` or `${CLAUDE_PLUGIN_ROOT}` | Absolute `/Users/...` |
| Skill naming | gerund form (`writing-skills`) | noun form (`skill-writer`) |
| Version format | semver `1.2.3` | arbitrary `v1` |
| Persistent data | `${CLAUDE_PLUGIN_DATA}` | Local temp paths |

## Execution Order

Fix issues in this order to avoid cascading problems:

1. **Manifest fixes** — required fields, naming, version
2. **Structure fixes** — move misplaced directories, remove orphans
3. **Skill fixes** — frontmatter, naming, line count, triggers
4. **Command fixes** — frontmatter, skill references
5. **Agent fixes** — isolation, tool lists, descriptions
6. **Version sync** — align plugin.json, marketplace.json, READMEs
7. **Path fixes** — replace absolute paths with variables

## Environment Variables

### Plugin Variables (substituted in skills, agents, hooks, MCP/LSP configs)

| Variable | Purpose | Survives Update? |
|----------|---------|-----------------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation directory (absolute path) | No — changes on update |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory (`~/.claude/plugins/data/{id}/`) | Yes — auto-created on first reference |

### Skill Variables (substituted in SKILL.md content)

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md — reference bundled scripts/data |
| `${CLAUDE_SESSION_ID}` | Current session ID — session-specific temp files |
| `$ARGUMENTS` / `$ARGUMENTS[N]` / `$N` | Arguments passed when invoking the skill |

### User Config Variables (declared in plugin.json `userConfig`)

| Variable | Purpose |
|----------|---------|
| `${user_config.KEY}` | Inline substitution in MCP/LSP configs, hook commands, skill/agent content |
| `CLAUDE_PLUGIN_OPTION_<KEY>` | Exported as env var to plugin subprocesses |

### Shell Context

Skills can inject live data using `!` commands (preprocessing before Claude sees content):
- Inline: `` !`git status` ``
- Multi-line: `` ```! `` code block
- Shell selection: `shell: powershell` frontmatter (requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`)
- Disable: `"disableSkillShellExecution": true` in settings

## Naming Conventions

| Component | Convention | Example |
|-----------|-----------|---------|
| Plugin name | kebab-case | `my-plugin` |
| Skill name | gerund form | `writing-skills` |
| Skill description | "Use when..." triggers | `Use when creating new skills` |
| Command file | kebab-case `.md` | `refactor-plugin.md` |
| Agent file | kebab-case `.md` | `skill-reviewer.md` |

## Auto-Discovery Defaults

If omitted from `plugin.json`, Claude Code auto-scans these paths:

| Component | Default Path | Purpose |
|-----------|-------------|---------|
| Skills | `skills/` | Capabilities (SKILL.md per subdirectory) |
| Commands | `commands/` | Slash command aliases |
| Agents | `agents/` | Subagent definitions |
| Output styles | `output-styles/` | Response formatting |
| Hooks | `hooks/hooks.json` | Lifecycle hooks (PreToolUse, PostToolUse, etc.) |
| MCP | `.mcp.json` | MCP server configurations (tool integrations) |
| LSP | `.lsp.json` | Language server configurations |

**Hooks, MCP, and LSP are key for agent engineering plugins** — they allow a plugin to provide not just skills but also automated enforcement (hooks), external tool access (MCP), and language intelligence (LSP).
