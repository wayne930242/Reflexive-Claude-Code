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

| Variable | Purpose |
|----------|---------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation directory (absolute path) |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory (`~/.claude/plugins/data/{id}/`) |

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

| Component | Default Path |
|-----------|-------------|
| Commands | `commands/` |
| Agents | `agents/` |
| Skills | `skills/` |
| Output styles | `output-styles/` |
| Hooks | `hooks/hooks.json` |
| MCP | `.mcp.json` |
| LSP | `.lsp.json` |
