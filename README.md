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

## What's New in v9.0.0

Major release aligning with current agent engineering best practices.

- **Architecture-first planning**: `planning-agent-systems` now requires drawing an architecture flowchart (DOT format) before deciding components — visualize entry points, decision branches, data flow, and parallel lanes before committing to any component
  - Maps workflows to Anthropic's six production patterns (Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer, Autonomous Agent)
  - Dependency-driven execution order replaces fixed order — phases assigned by dependency depth
  - Core vs enhancement classification for phased rollout
- **Simplicity-first brainstorming**: `brainstorming-workflows` adds a complexity ladder (Level 1-6) that challenges every workflow for the simplest viable approach before designing components
  - Two-layer classification: Anthropic workflow patterns + skill routing patterns
  - Walkthrough-style questions replace inventory-style questions across all role templates
  - Past failures exploration: "What have you tried before? What didn't work?"
- **10-category weakness analysis**: `analyzing-agent-systems` adds Category 10 (Cross-Tool Migration) for detecting `.cursorrules`, copilot instructions, and other AI tool configs
  - New checks: skill token budget (< 2,000 tokens), `disable-model-invocation`, `allowed-tools`, dynamic context injection, compaction strategy
  - Scans `.cursorrules`, `.github/copilot-instructions.md`, `.windsurfrules`, `.editorconfig`
- **Maturity-graded migration**: `migrating-agent-systems` replaces binary detection with 4-level maturity grading (None → Seed → Partial → Established)
  - Seed level imports other AI tool configs as starting context
  - Recommends English for all prompt files for optimal model performance
- **Progressive disclosure**: Templates and reference tables extracted to `references/` across all four skills — all SKILL.md files now under 200 lines

## What's New in v8.4.0

- **Project context completeness**: New weakness category (#9) checks for missing account names, directory conventions, deployment targets, language-specific hooks, and user-root gap analysis
  - `analyzing-agent-systems` now scans `~/.claude/` alongside `.claude/` and compares coverage
  - `reflecting` classification tree adds user-root scope — cross-project learnings route to `~/.claude/CLAUDE.md` or `~/.claude/rules/`

## What's New in v8.3.0

- **Formalized routing patterns**: All 20 skills now declare their routing pattern (Tree/Chain/Node/Skill Steps)
  - New `routing-patterns.md` reference document with selection guide and global routing map
  - Standardized `## Routing` section in every SKILL.md
  - `brainstorming-workflows` now teaches routing pattern selection during agent system design
  - `advising-architecture` decision tree includes routing pattern classification
  - `weakness-checklist` adds 7 routing-specific checks
  - Skill Chain Reference tables added to all entry-point skills
  - `writing-plugins` (rcc-dev) rewritten for full Law 7 compliance

## Plugins

This marketplace provides two plugins:

### rcc (v9.1.1)

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
| `migrating-agent-systems` | Maturity-graded routing with cross-tool config detection |
| `analyzing-agent-systems` | 10-category weakness detection with cross-tool migration checks |
| `brainstorming-workflows` | Walkthrough-based workflow exploration with complexity ladder |
| `planning-agent-systems` | Architecture-first planning with Anthropic pattern mapping |
| `applying-agent-systems` | Execute component plan via writing-* skill chain |
| `reviewing-agent-systems` | Quality review with all 5 reviewer agents |
| `refactoring-agent-systems` | Fix issues from review report |
| `creating-plugins` | Scaffold a new Claude Code plugin |
| `refactoring-plugins` | Refactor plugins against official best practices with health check |
| `advising-architecture` | Validate approach, classify knowledge type, check for component conflicts |

**Agent System Skill Chain:**

```
migrating-agent-systems (maturity-graded router)
  ├─ None → brainstorming-workflows → planning-agent-systems → ...
  ├─ Seed (other AI configs) → import configs → brainstorming-workflows → ...
  └─ Partial/Established → analyzing-agent-systems → brainstorming-workflows
       → planning-agent-systems → applying-agent-systems
       → reviewing-agent-systems → refactoring-agent-systems
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
