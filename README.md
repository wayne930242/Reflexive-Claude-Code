# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A **skills-driven Agentic Context Engineering** workflow for Claude Code.

## Core Philosophy

The agent maintains and refactors its own core prompts and agent system — not external documents or memory banks.

**Skills-driven Agentic Context Engineering** means:
- Before each task, the agent reviews the skill library for relevant capabilities
- Users explicitly trigger learning moments through commands like `/reflect`
- Through deliberate teaching, the agent integrates learnings into its skill library
- Skills are abstract, reusable, and link to reference directories with examples and documentation

## Plugins

This marketplace provides two plugins:

### ACE-core (v1.2.0)

Core ACE workflow with reflection, skill consolidation, CLAUDE.md refactoring, and skill/command authoring tools.

**Skills:**

| Skill | Description | Trigger |
|-------|-------------|---------|
| `write-skill` | Create effective SKILL.md files following Anthropic's official patterns | "Help me write a skill for...", "Create a new skill..." |
| `write-command` | Create slash commands with proper YAML frontmatter and argument handling | "Help me write a command...", "Create a slash command..." |

**Commands:**

| Command | Description | Usage |
|---------|-------------|-------|
| `/reflect` | Reflect on conversation, extract learnings, integrate into skill library | `/reflect [focus]` |
| `/refactor-skills` | Analyze and consolidate all skills - merge, optimize, remove redundancy | `/refactor-skills` |
| `/refactor-claude-md` | Refactor CLAUDE.md with constitution mechanism | `/refactor-claude-md [path] [mode]` |
| `/improve-skill` | Optimize a skill by analyzing conventions and researching best practices | `/improve-skill <skill-path>` |

### RCC-dev-helper (v1.0.0)

Development helper tools for creating Claude Code plugins with complete manifests, commands, skills, and marketplaces.

**Skills:**

| Skill | Description | Trigger |
|-------|-------------|---------|
| `write-plugin` | Create complete plugin packages with manifests, commands, skills, and marketplaces | "Create a plugin for...", "Package this as a plugin..." |

**Commands:**

| Command | Description | Usage |
|---------|-------------|-------|
| `/create-plugin` | Scaffold a new Claude Code plugin | `/create-plugin <name> [type]` |

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│                   Work Session                          │
├─────────────────────────────────────────────────────────┤
│  1. Before Task     │  Review skill library             │
│  2. Do Work         │  Just work normally               │
│  3. /reflect        │  Extract learnings → skills       │
│  4. /refactor-skills│  Consolidate & optimize           │
└─────────────────────────────────────────────────────────┘
```

Each skill links to a directory with:
- `SKILL.md` — Abstract instructions
- `references/` — Detailed docs, code examples
- `scripts/` — Executable utilities

## Installation

```bash
# From GitHub
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install ACE-core@weihung-marketplace
# or
/plugin install RCC-dev-helper@weihung-marketplace

# From local path
/plugin install /path/to/Reflexive-Claude-Code
```

## Project Structure

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   ├── marketplace.json     # Marketplace definition
│   ├── ACE-core.json        # ACE-core plugin manifest
│   └── RCC-dev-helper.json  # RCC-dev-helper plugin manifest
├── commands/
│   ├── reflect.md           # ACE-core: session reflection
│   ├── refactor-skills.md   # ACE-core: skill consolidation
│   ├── refactor-claude-md.md # ACE-core: CLAUDE.md refactoring
│   ├── improve-skill.md     # ACE-core: skill optimization
│   └── create-plugin.md     # RCC-dev-helper: plugin scaffolding
├── skills/
│   ├── write-skill/         # ACE-core: creates skills
│   ├── write-command/       # ACE-core: creates commands
│   └── write-plugin/        # RCC-dev-helper: creates plugins
└── README.md
```

## Inspiration

This project is inspired by the **Agentic Context Engineering (ACE)** framework:

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

The ACE framework's modular approach of **Generate → Reflect → Curate** directly influenced this project's skills-driven workflow, where users explicitly trigger learning moments and guide the agent's self-improvement through deliberate teaching.

## License

MIT
