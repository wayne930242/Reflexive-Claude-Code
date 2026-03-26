# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A **skills-driven Agentic Context Engineering** workflow for Claude Code with TDD-based skill design.

## Core Philosophy

The agent maintains and refactors its own core prompts and agent system — not external documents or memory banks.

**Skills-driven Agentic Context Engineering** means:
- Before each task, the agent reviews the skill library for relevant capabilities
- Users explicitly trigger learning moments through skills like `reflecting`
- Through deliberate teaching, the agent integrates learnings into its skill library
- Skills are abstract, reusable, and link to reference directories with examples and documentation

## What's New in v8.2.0

- **New `refactoring-plugins` skill**: Plugin migration and refactoring against official Claude Code best practices
  - Cross-platform Python health check script (`validate_plugin.py`, supports `uv run`)
  - Integrates official `claude plugin validate` CLI
  - 8-category plugin health checklist (manifest, structure, skills, commands, agents, paths, version sync, distribution)
  - Skill trigger overlap detection across all skills
  - New `/refactor-plugin` command

## Plugins

This marketplace provides two plugins:

### rcc (v8.2.0)

Core ACE workflow with TDD-based skills, task enforcement, and quality reviewers.

**Skills:**

| Skill | Description |
|-------|-------------|
| `writing-skills` | TDD-based skill creation with baseline testing and review |
| `writing-claude-md` | Create CLAUDE.md with standard markdown format |
| `writing-subagents` | Create subagent configurations for `.claude/agents/` |
| `writing-rules` | Create rule files for `.claude/rules/` with conventions |
| `writing-hooks` | Create hooks for static analysis and code quality |
| `reflecting` | Reflect on conversation, classify learnings, integrate |
| `improving-skills` | Optimize a skill through targeted improvements |
| `refactoring-skills` | Analyze and consolidate all skills |
| `initializing-projects` | Initialize new project with framework and agent system |
| `migrating-agent-systems` | Route to analysis or brainstorming based on project state |
| `analyzing-agent-systems` | Scan and detect weaknesses in existing agent systems |
| `brainstorming-workflows` | Role-based workflow exploration for agent system design |
| `planning-agent-systems` | Plan agent system components with traceability |
| `applying-agent-systems` | Execute component plan via writing-* skill chain |
| `reviewing-agent-systems` | Quality review with all 5 reviewer agents |
| `refactoring-agent-systems` | Fix issues from review report |
| `creating-plugins` | Scaffold a new Claude Code plugin |
| `refactoring-plugins` | Refactor plugins against official best practices with health check |
| `advising-architecture` | Validate approach, classify knowledge type, check for component conflicts |

**Agent System Skill Chain:**

```
migrating-agent-systems (router)
  ├─ Existing system → analyzing-agent-systems → brainstorming-workflows → ...
  └─ New project → brainstorming-workflows → planning-agent-systems
       → applying-agent-systems → reviewing-agent-systems → refactoring-agent-systems
```

**Subagents (Reviewers):**

| Agent | Description |
|-------|-------------|
| `skill-reviewer` | Quality review for skills |
| `claudemd-reviewer` | Quality review for CLAUDE.md |
| `rule-reviewer` | Quality review for rules |
| `hook-reviewer` | Quality review for hooks |
| `subagent-reviewer` | Quality review for subagents |

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

## Skill Design Principles

All skills follow TDD-based design with these components:

| Component | Purpose |
|-----------|---------|
| **Task Initialization** | Mandatory TaskCreate before any action |
| **TDD Mapping** | RED → GREEN → REFACTOR phases |
| **Verification Criteria** | Objective checks for each task |
| **Red Flags** | Anti-rationalization triggers |
| **Rationalizations Table** | Counter-arguments for common excuses |
| **Flowchart** | Visual process diagram |
| **Reviewer Gate** | Quality review before completion |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Work Session                                   │
├─────────────────────────────────────────────────────────────────┤
│  1. Task 1        │  Consult advising-architecture               │
│  2. RED Phase     │  Baseline test - observe failures           │
│  3. GREEN Phase   │  Create component addressing failures       │
│  4. REFACTOR      │  Quality review via reviewer subagent       │
│  5. Validate      │  Test in real usage                         │
└─────────────────────────────────────────────────────────────────┘
```

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
│   │   ├── skills/          # All skills
│   │   ├── agents/          # Reviewer subagents
│   │   └── commands/        # Command aliases
│   └── rcc-dev/             # Development helper plugin
└── README.md
```

## Credits

This project's skill design patterns are inspired by:

- **[superpowers](https://github.com/anthropics/claude-code-superpowers)** - The TDD-based skill design, task enforcement, and verification patterns are adapted from the superpowers plugin by Anthropic. Special thanks for pioneering the "discipline-enforcing skill" pattern with Red Flags and Rationalization tables.

- **Agentic Context Engineering (ACE) Framework**:
  > Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

## License

MIT
