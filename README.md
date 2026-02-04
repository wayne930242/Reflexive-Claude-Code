# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A **skills-driven Agentic Context Engineering** workflow for Claude Code.

## Core Philosophy

The agent maintains and refactors its own core prompts and agent system — not external documents or memory banks.

**Skills-driven Agentic Context Engineering** means:
- Before each task, the agent reviews the skill library for relevant capabilities
- Users explicitly trigger learning moments through skills like `reflecting`
- Through deliberate teaching, the agent integrates learnings into its skill library
- Skills are abstract, reusable, and link to reference directories with examples and documentation

## Plugins

This marketplace provides two plugins:

### rcc (v6.0.3)

Core ACE workflow with reflection, architecture guidance, modular rules, and skill authoring tools.

**Skills:**

| Skill | Description |
|-------|-------------|
| `agent-architect` | Architecture advisor for holistic guidance on component design |
| `project-discovery` | Deep project analysis for architecture planning |
| `writing-skills` | Create effective SKILL.md files following Anthropic's official patterns |
| `writing-claude-md` | Create CLAUDE.md with `<law>` constitution |
| `writing-subagents` | Create subagent configurations for `.claude/agents/` |
| `writing-rules` | Create rule files for `.claude/rules/` with conventions |
| `writing-hooks` | Create hooks for static analysis and code quality |
| `reflecting` | Reflect on conversation, classify learnings, integrate |
| `improving-skills` | Optimize a skill by analyzing conventions and researching best practices |
| `refactoring-skills` | Analyze and consolidate all skills - merge, optimize, remove redundancy |
| `hunting-skills` | Search external skills via claude-skills-mcp, adapt as new project skills |
| `refactoring-with-external-skills` | Refactor existing skills using external skill patterns |
| `adding-laws` | Add a new law to the CLAUDE.md constitution |
| `initializing-projects` | Initialize new project with framework, best practices, and agent system |
| `migrating-agent-systems` | Migrate existing systems to best practices architecture |

### rcc-dev (v2.0.1)

Development helper tools for creating Claude Code plugins with complete manifests, skills, and marketplaces.

**Skills:**

| Skill | Description |
|-------|-------------|
| `writing-plugins` | Create complete plugin packages with manifests, skills, and marketplaces |
| `creating-plugins` | Scaffold a new Claude Code plugin |

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Context                          │
├─────────────────────────────────────────────────────────────────┤
│  Auto-Injected                     │  On-Demand                  │
│  ─────────────                     │  ─────────                  │
│  • CLAUDE.md (high-level)          │  • Skills (capabilities)    │
│  • .claude/rules/*.md (conventions)│  • Subagents (isolated ctx) │
│    └─ paths: conditional trigger   │                             │
└─────────────────────────────────────────────────────────────────┘
```

| Component | Location | Trigger | Token Impact |
|-----------|----------|---------|--------------|
| **Rules** | `.claude/rules/*.md` | Auto-inject | High |
| **Skills** | `.claude/skills/*/SKILL.md` | Claude decides | Progressive disclosure |
| **Subagents** | `.claude/agents/*.md` | Task tool | Isolated |
| **CLAUDE.md** | `./CLAUDE.md` | Auto-inject | High |

## Core Constitution

CLAUDE.md uses `<law>` blocks for Self-Reinforcing Display:

| Law | Purpose |
|-----|---------|
| **Communication** | Concise, actionable responses |
| **Skill Discovery** | Check available skills before starting work |
| **Rule Consultation** | Check `.claude/rules/` for domain conventions |
| **Parallel Processing** | Use Task tool for independent operations |
| **Reflexive Learning** | Remind user to reflect on important discoveries |
| **Self-Reinforcing Display** | Display `<law>` block at start of every response |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Work Session                                   │
├─────────────────────────────────────────────────────────────────┤
│  1. Before Task     │  Review skill library                      │
│  2. Do Work         │  Just work normally                        │
│  3. Reflect         │  Classify → Rules or Skills → Integrate    │
│  4. Refactor        │  Consolidate & optimize                    │
└─────────────────────────────────────────────────────────────────┘
```

Each skill links to a directory with:
- `SKILL.md` — Abstract instructions (progressive disclosure)
- `references/` — Detailed docs loaded on-demand
- `scripts/` — Executable utilities

## Installation

```bash
# From GitHub
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install rcc@rcc
# or
/plugin install rcc-dev@rcc

# From local path
/plugin install /path/to/Reflexive-Claude-Code/plugins/rcc
```

## Project Structure

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   └── marketplace.json     # Marketplace definition
├── plugins/
│   ├── rcc/                 # Core ACE plugin
│   └── rcc-dev/             # Development helper plugin
├── skills/
│   ├── agent-architect/     # ACE-core: architecture advisor
│   ├── project-discovery/   # ACE-core: project analysis
│   ├── writing-skills/      # ACE-core: creates skills
│   ├── writing-claude-md/   # ACE-core: creates CLAUDE.md
│   ├── writing-subagents/   # ACE-core: creates subagents
│   ├── writing-rules/       # ACE-core: creates rules
│   ├── writing-hooks/       # ACE-core: creates hooks
│   ├── reflecting/          # ACE-core: session reflection
│   ├── improving-skills/    # ACE-core: skill optimization
│   ├── refactoring-skills/  # ACE-core: skill consolidation
│   ├── hunting-skills/      # ACE-core: external skill hunting
│   ├── refactoring-with-external-skills/  # ACE-core: refactor with external
│   ├── adding-laws/         # ACE-core: add constitution law
│   ├── initializing-projects/  # ACE-core: project initialization
│   ├── migrating-agent-systems/  # ACE-core: system migration
│   ├── writing-plugins/     # RCC-dev-helper: creates plugins
│   └── creating-plugins/    # RCC-dev-helper: plugin scaffolding
└── README.md
```

## Inspiration

This project is inspired by the **Agentic Context Engineering (ACE)** framework:

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

The ACE framework's modular approach of **Generate → Reflect → Curate** directly influenced this project's skills-driven workflow, where users explicitly trigger learning moments and guide the agent's self-improvement through deliberate teaching.

## License

MIT
