# Weihung Claude Plugin

A Claude Code plugin collection with tools for plugin development and productivity.

## Features

### Skills (Auto-Activated)

| Skill | Description |
|-------|-------------|
| `write-skill` | Plugin & skill authoring expert. Helps create well-structured plugins following Anthropic 2025 schema. |

### Commands (Explicit)

| Command | Description |
|---------|-------------|
| `/create-plugin <name> [type]` | Scaffold a new plugin with proper structure |

## Installation

### From GitHub (Recommended)

```bash
# Add marketplace
/plugin marketplace add weihung/weihung-claude-plugin

# Install plugin
/plugin install weihung-claude-plugin@weihung
```

### From Local Path

```bash
# Install directly
/plugin install /path/to/weihung-claude-plugin

# Or add as local marketplace
/plugin marketplace add ./weihung-claude-plugin
/plugin install weihung-claude-plugin@weihung-marketplace
```

## Plugin Structure

```
weihung-claude-plugin/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest
│   └── marketplace.json      # Marketplace manifest
├── commands/
│   └── create-plugin.md      # /create-plugin command
├── skills/
│   └── write-skill/
│       └── SKILL.md          # Auto-activated skill
├── .gitignore
└── README.md
```

## Usage Examples

### Auto-Activated Skill

Just ask Claude to help with plugin creation:

```
"Help me create a code review plugin"
"I want to build a skill for deployment automation"
"Create a new Claude Code plugin for API testing"
```

The `write-skill` skill activates automatically and guides you through the process.

### Explicit Command

Use the command for quick scaffolding:

```
/create-plugin my-new-plugin
/create-plugin code-reviewer skill
/create-plugin deploy-helper command
```

## Development

### Testing Locally

1. Clone this repository
2. Add as local marketplace:
   ```
   /plugin marketplace add ./weihung-claude-plugin
   ```
3. Install and test:
   ```
   /plugin install weihung-claude-plugin@weihung-marketplace
   ```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add your plugin/skill/command
4. Submit a pull request

## Resources

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins)
- [Plugin Marketplaces Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## License

MIT
