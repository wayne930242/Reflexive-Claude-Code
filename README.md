# Reflexive Claude Code

A **reflexive meta-framework** for Claude Code that enables Claude to introspect, optimize, and evolve its own agent system configurations.

## Core Philosophy

This plugin provides Claude with **reflexive capabilities** - the ability to:

- **Self-examine**: Analyze existing CLAUDE.md configurations, skills, and commands
- **Self-improve**: Refactor and optimize agent system components
- **Self-extend**: Create new skills and commands following best practices
- **Self-govern**: Establish constitution mechanisms for consistent AI behavior

By giving Claude tools to understand and improve its own configuration, users can build more effective, well-structured Claude Code agent systems through collaborative refinement.

## Skills

Auto-activated capabilities based on context.

| Skill | Description | Trigger |
|-------|-------------|---------|
| `write-skill` | Create effective SKILL.md files following Anthropic's official patterns | "Help me write a skill for...", "Create a new skill..." |
| `write-command` | Create slash commands with proper YAML frontmatter and argument handling | "Help me write a command...", "Create a slash command..." |
| `write-plugin` | Create complete plugin packages with manifests, commands, skills, and marketplaces | "Create a plugin for...", "Package this as a plugin..." |

## Commands

Manually invoked actions for agent system optimization.

| Command | Description | Usage |
|---------|-------------|-------|
| `/create-plugin` | Scaffold a new Claude Code plugin with proper structure | `/create-plugin <name> [type]` |
| `/refactor-skills` | Analyze and refactor all skills - consolidate, optimize, remove redundancy | `/refactor-skills` |
| `/refactor-claude-md` | Refactor CLAUDE.md with constitution mechanism for consistent AI behavior | `/refactor-claude-md [path] [mode]` |

### Command Details

**`/create-plugin <name> [type]`**
- `name`: Plugin name in kebab-case (required)
- `type`: `skill`, `command`, or `full` (default: `full`)

**`/refactor-claude-md [path] [mode]`**
- `path`: Path to CLAUDE.md or project directory (default: current directory)
- `mode`: `analyze`, `refactor`, or `generate` (default: `analyze`)

The refactor-claude-md command includes a **constitution mechanism** with self-reinforcing laws:
1. Collaborative Decision Making
2. Project-Specific Architecture Law
3. Quality Gates
4. Code Style Compliance
5. Communication Discipline
6. Self-Reinforcing Display

## Use Cases

### Building a New Agent System
```
User: Help me create a CLAUDE.md for my TypeScript project
Claude: [Uses write-skill patterns + /refactor-claude-md generate]
```

### Optimizing Existing Configuration
```
User: My CLAUDE.md is getting too long and messy
Claude: [Uses /refactor-claude-md refactor to optimize and add constitution]
```

### Creating Reusable Components
```
User: I want to package my workflow as a shareable plugin
Claude: [Uses write-plugin skill + /create-plugin command]
```

### Skill Consolidation
```
User: I have too many overlapping skills, help me clean up
Claude: [Uses /refactor-skills to analyze, merge, and optimize]
```

## Installation

```bash
# From GitHub
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install Reflexive-Claude-Code@wayne930242

# From local path
/plugin install /path/to/Reflexive-Claude-Code
```

## Project Structure

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace definition
├── commands/
│   ├── create-plugin.md     # Plugin scaffolding
│   ├── refactor-skills.md   # Skill optimization
│   └── refactor-claude-md.md # CLAUDE.md refactoring
├── skills/
│   ├── write-skill/         # Skill authoring guide
│   ├── write-command/       # Command authoring guide
│   └── write-plugin/        # Plugin authoring guide
└── README.md
```

## License

MIT
