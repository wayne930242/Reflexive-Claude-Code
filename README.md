# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A **Skills-Driven Development (SDD)** framework for Claude Code.

## Core Philosophy

The agent maintains and refactors its own core prompts and agent system — not external documents or memory banks.

**Skills-Driven Development** means:
- Before each task, the agent reviews the skill library for relevant capabilities
- Users explicitly trigger learning moments through commands like `/reflect`
- Through deliberate teaching, the agent integrates learnings into its skill library
- Skills are abstract, reusable, and link to reference directories with examples and documentation

## Skills

Auto-activated capabilities based on context.

| Skill | Description | Trigger |
|-------|-------------|---------|
| `write-skill` | Create effective SKILL.md files following Anthropic's official patterns | "Help me write a skill for...", "Create a new skill..." |
| `write-command` | Create slash commands with proper YAML frontmatter and argument handling | "Help me write a command...", "Create a slash command..." |
| `write-plugin` | Create complete plugin packages with manifests, commands, skills, and marketplaces | "Create a plugin for...", "Package this as a plugin..." |

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/reflect` | Reflect on conversation, extract learnings, integrate into skill library | `/reflect [focus]` |
| `/refactor-skills` | Analyze and consolidate all skills - merge, optimize, remove redundancy | `/refactor-skills` |
| `/refactor-claude-md` | Refactor CLAUDE.md with constitution mechanism | `/refactor-claude-md [path] [mode]` |
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
/plugin install Reflexive-Claude-Code@wayne930242

# From local path
/plugin install /path/to/Reflexive-Claude-Code
```

## Project Structure

```
Reflexive-Claude-Code/
├── commands/
│   ├── reflect.md           # Core: session reflection
│   ├── refactor-skills.md   # Core: skill consolidation
│   ├── refactor-claude-md.md
│   └── create-plugin.md
├── skills/
│   ├── write-skill/         # Meta: creates skills
│   ├── write-command/
│   └── write-plugin/
└── .claude-plugin/
```

## Inspiration

This project is inspired by the **Agentic Context Engineering (ACE)** framework:

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

The ACE framework's modular approach of **Generate → Reflect → Curate** directly influenced this project's Skills-Driven Development workflow, where users explicitly trigger learning moments and guide the agent's self-improvement through deliberate teaching.

## License

MIT
