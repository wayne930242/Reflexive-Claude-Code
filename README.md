# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A **skills-driven Agentic Context Engineering** workflow for Claude Code.

## Core Philosophy

The agent maintains and refactors its own core prompts and agent system — not external documents or memory banks.

**Skills-driven Agentic Context Engineering** means:
- Before each task, the agent reviews the skill library for relevant capabilities
- Users explicitly trigger learning moments through commands like `/rcc:reflect`
- Through deliberate teaching, the agent integrates learnings into its skill library
- Skills are abstract, reusable, and link to reference directories with examples and documentation

## Plugins

This marketplace provides two plugins:

### ACE-core (v5.0.0)

Core ACE workflow with reflection, architecture guidance, modular rules, and authoring tools.

**Skills:**

| Skill | Description | Trigger |
|-------|-------------|---------|
| `agent-architect` | Architecture advisor for holistic guidance on component design | "Review architecture...", "Help me restructure..." |
| `write-claude-md` | Create CLAUDE.md with `<law>` constitution | "Help me write CLAUDE.md...", "Create project setup..." |
| `write-subagent` | Create subagent configurations for `.claude/agents/` | "Create a subagent...", "Set up a code reviewer agent..." |
| `write-skill` | Create effective SKILL.md files following Anthropic's official patterns | "Help me write a skill for...", "Create a new skill..." |
| `write-command` | Create slash commands with proper YAML frontmatter and argument handling | "Help me write a command...", "Create a slash command..." |
| `write-rules` | Create rule files for `.claude/rules/` with conventions | "Add a coding convention...", "Create a rule for..." |
| `write-hook` | Create hooks for static analysis and code quality | "Add a linting hook...", "Set up type checking..." |

**Commands:**

| Command | Description | Usage |
|---------|-------------|-------|
| `/rcc:init-project` | Initialize new project with framework, best practices, and agent system | `/rcc:init-project [path]` |
| `/rcc:reflect` | Reflect on conversation, classify learnings, integrate | `/rcc:reflect [focus]` |
| `/rcc:refactor-skills` | Analyze and consolidate all skills - merge, optimize, remove redundancy | `/rcc:refactor-skills` |
| `/rcc:migration` | Migrate existing systems to best practices architecture | `/rcc:migration [path]` |
| `/rcc:improve-skill` | Optimize a skill by analyzing conventions and researching best practices | `/rcc:improve-skill <skill-path>` |
| `/rcc:add-law` | Add a new law to the CLAUDE.md constitution | `/rcc:add-law [law_content]` |

### RCC-dev-helper (v1.0.0)

Development helper tools for creating Claude Code plugins with complete manifests, commands, skills, and marketplaces.

**Skills:**

| Skill | Description | Trigger |
|-------|-------------|---------|
| `write-plugin` | Create complete plugin packages with manifests, commands, skills, and marketplaces | "Create a plugin for...", "Package this as a plugin..." |

**Commands:**

| Command | Description | Usage |
|---------|-------------|-------|
| `/rcc:create-plugin` | Scaffold a new Claude Code plugin | `/rcc:create-plugin <name> [type]` |

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Context                          │
├─────────────────────────────────────────────────────────────────┤
│  Auto-Injected                     │  On-Demand                  │
│  ─────────────                     │  ─────────                  │
│  • CLAUDE.md (high-level)          │  • Skills (capabilities)    │
│  • .claude/rules/*.md (conventions)│  • Commands (user-triggered)│
│    └─ paths: conditional trigger   │  • Subagents (isolated ctx) │
└─────────────────────────────────────────────────────────────────┘
```

| Component | Location | Trigger | Token Impact |
|-----------|----------|---------|--------------|
| **Rules** | `.claude/rules/*.md` | Auto-inject | High (< 50 lines) |
| **Skills** | `.claude/skills/*/SKILL.md` | Claude decides | Medium (< 200 lines) |
| **Commands** | `.claude/commands/*.md` | User `/command` | Low |
| **Subagents** | `.claude/agents/*.md` | Task tool | Isolated |
| **CLAUDE.md** | `./CLAUDE.md` | Auto-inject | High (< 300 lines) |

## Core Constitution

CLAUDE.md uses `<law>` blocks for Self-Reinforcing Display:

| Law | Purpose |
|-----|---------|
| **Communication** | Concise, actionable responses |
| **Skill Discovery** | Check available skills before starting work |
| **Rule Consultation** | Check `.claude/rules/` for domain conventions |
| **Parallel Processing** | Use Task tool for independent operations |
| **Reflexive Learning** | Remind user to `/rcc:reflect` on important discoveries |
| **Self-Reinforcing Display** | Display `<law>` block at start of every response |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Work Session                                   │
├─────────────────────────────────────────────────────────────────┤
│  1. Before Task     │  Review skill library                      │
│  2. Do Work         │  Just work normally                        │
│  3. /rcc:reflect    │  Classify → Rules or Skills → Integrate    │
│  4. /refactor-*     │  Consolidate & optimize                    │
└─────────────────────────────────────────────────────────────────┘
```

Each skill links to a directory with:
- `SKILL.md` — Abstract instructions (< 200 lines)
- `references/` — Detailed docs loaded on-demand
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
│   ├── init-project.md      # ACE-core: project initialization
│   ├── reflect.md           # ACE-core: session reflection
│   ├── refactor-skills.md   # ACE-core: skill consolidation
│   ├── migration.md         # ACE-core: system migration
│   ├── improve-skill.md     # ACE-core: skill optimization
│   ├── add-law.md           # ACE-core: add constitution law
│   └── create-plugin.md     # RCC-dev-helper: plugin scaffolding
├── skills/
│   ├── agent-architect/     # ACE-core: architecture advisor
│   ├── write-claude-md/     # ACE-core: creates CLAUDE.md
│   ├── write-subagent/      # ACE-core: creates subagents
│   ├── write-skill/         # ACE-core: creates skills
│   ├── write-command/       # ACE-core: creates commands
│   ├── write-rules/         # ACE-core: creates rules
│   ├── write-hook/          # ACE-core: creates hooks
│   └── write-plugin/        # RCC-dev-helper: creates plugins
└── README.md
```

## Inspiration

This project is inspired by the **Agentic Context Engineering (ACE)** framework:

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

The ACE framework's modular approach of **Generate → Reflect → Curate** directly influenced this project's skills-driven workflow, where users explicitly trigger learning moments and guide the agent's self-improvement through deliberate teaching.

## License

MIT
