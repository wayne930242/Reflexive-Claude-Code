# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

A Claude Code plugin marketplace for **skills-driven Agentic Context Engineering (ACE)** — build, analyze, and maintain agent systems with TDD-based workflows.

## What This Does

Reflexive Claude Code gives Claude Code a complete toolkit for managing its own agent system: CLAUDE.md, rules, skills, subagents, and hooks. Every component goes through a TDD cycle (RED → GREEN → REFACTOR) with automated quality review.

**Key capabilities:**

- **Build agent systems from scratch** — detect project maturity, explore workflows, plan architecture, then create all components in dependency order
- **Analyze existing systems** — 11-category weakness checklist covering routing, context management, security, rules health, and cross-tool migration
- **Validate on every edit** — PostToolUse hook checks frontmatter, broken links, orphaned files, and invalid variables in real time
- **Enforce quality gates** — 5 specialized reviewer agents (skill, CLAUDE.md, rule, hook, subagent) run after every creation or modification

## Installation

```bash
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install rcc@rcc
```

## How It Works

### Agent System Pipeline

The full pipeline runs through 6 stages, each a dedicated skill:

```
migrate → analyze → brainstorm → plan → apply → review → refactor
```

| Stage | Skill | What it does |
|-------|-------|-------------|
| **Migrate** | `migrating-agent-systems` | Detect maturity (None/Seed/Partial/Established), propose rules refactoring, route to correct chain |
| **Analyze** | `analyzing-agent-systems` | Scan all components, run 11-category weakness checklist, produce Rules Health Summary |
| **Brainstorm** | `brainstorming-workflows` | Explore workflows with complexity ladder (L1-L6), map to Anthropic patterns |
| **Plan** | `planning-agent-systems` | Architecture flowchart first, then dependency-driven component plan |
| **Apply** | `applying-agent-systems` | Invoke writing-* skills in order: CLAUDE.md → rules → hooks → skills → agents |
| **Review** | `reviewing-agent-systems` | Run all 5 reviewer agents, produce structured report |

### Quality Checks

**11-category weakness analysis** (via `analyzing-agent-systems`):

| # | Category | Key checks |
|---|----------|-----------|
| 1 | Routing / Triggers | Vague descriptions, overlapping triggers, missing handoffs |
| 2 | Context Management | Oversized CLAUDE.md, eager loading, context pollution |
| 3 | Workflow Continuity | Broken chains, missing verification gates |
| 4 | Redundancy / Conflicts | Duplicate rules, contradicting instructions |
| 5 | Security / Safety | Unprotected sensitive files, excessive permissions |
| 6 | Observability | Missing structured output, opaque routing |
| 7 | Architecture / Scaling | Flat topology, over-orchestration |
| 8 | Constitution Stability | Procedures in CLAUDE.md, vague instructions |
| 9 | Project Context | Missing deployment docs, language coverage gaps |
| 10 | Cross-Tool Migration | Unimported `.cursorrules`, copilot instructions |
| 11 | Rules Health | Lines > 50, missing `paths:`, dead globs, session-start > 300 lines |

**Rules Health Summary** (produced during analysis):

| Metric | Threshold |
|--------|-----------|
| CLAUDE.md lines | > 200 = warning |
| Session-start total (CLAUDE.md + global rules) | > 300 = warning |
| Individual rule lines | > 50 = warning |
| Path-scoped rule with 0 file matches | dead glob |
| Procedural content in rules | should be a skill |

**Real-time validation hook** (`validate_frontmatter.py`):
- Fires on every Edit/Write to skill, agent, or rule files
- Checks for invalid frontmatter fields against official spec
- Detects broken markdown links and orphaned files in skill directories
- Outputs `additionalContext` so Claude can self-correct immediately

### Component Writing Skills

Each `writing-*` skill follows TDD with a reviewer gate:

| Skill | Creates | Reviewer |
|-------|---------|----------|
| `writing-claude-md` | `CLAUDE.md` | `claudemd-reviewer` |
| `writing-rules` | `.claude/rules/*.md` | `rule-reviewer` |
| `writing-hooks` | `.claude/hooks/*` | `hook-reviewer` |
| `writing-skills` | `.claude/skills/*/SKILL.md` | `skill-reviewer` |
| `writing-subagents` | `.claude/agents/*.md` | `subagent-reviewer` |

### Model Recommendations

| Use Case | Model |
|----------|-------|
| Implementation, code generation | `sonnet` |
| Planning, architecture design | `opus` |
| Read-only analysis, review | `sonnet` |
| Simple lookup, exploration | `haiku` |

## Full Skill List

### rcc (v9.4.1)

| Skill | Purpose |
|-------|---------|
| `migrating-agent-systems` | Maturity-graded routing with rules refactoring proposal |
| `migrating-plugins` | Plugin maturity detection, routes to create or validate+refactor |
| `analyzing-agent-systems` | 11-category weakness detection with Rules Health Summary |
| `brainstorming-workflows` | Complexity ladder + Anthropic pattern mapping |
| `planning-agent-systems` | Architecture-first planning with dependency ordering |
| `applying-agent-systems` | Execute component plan via writing-* chain |
| `reviewing-agent-systems` | Run all 5 reviewer agents |
| `refactoring-agent-systems` | Fix issues from review report |
| `writing-skills` | TDD-based skill creation |
| `writing-claude-md` | CLAUDE.md with standard format |
| `writing-subagents` | Subagent config with model/isolation guide |
| `writing-rules` | Rules with decision tree and content validation |
| `writing-hooks` | Hooks for static analysis and quality gates |
| `reflecting` | Extract learnings, route to skills or rules |
| `improving-skills` | Optimize a single skill |
| `refactoring-skills` | Consolidate and deduplicate across skills |
| `advising-architecture` | Classify knowledge type, validate approach |
| `initializing-projects` | Bootstrap new project with agent system |
| `creating-plugins` | Scaffold a new Claude Code plugin |
| `refactoring-plugins` | Health-check plugins against official best practices |
| `validating-plugins` | Batch scan all plugin files for errors |

### rcc-dev (v2.0.1)

| Skill | Purpose |
|-------|---------|
| `writing-plugins` | Create complete plugin packages |
| `creating-plugins` | Scaffold plugin structure |

## Project Structure

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   ├── rcc/
│   │   ├── skills/          # 20 skills
│   │   ├── agents/          # 5 reviewer subagents
│   │   └── hooks/           # Frontmatter validation hook
│   └── rcc-dev/
└── README.md
```

## Credits

- **[superpowers](https://github.com/anthropics/claude-code-superpowers)** — TDD-based skill design and discipline-enforcing patterns adapted from Anthropic's superpowers plugin.
- **Agentic Context Engineering (ACE)**:
  > Zhang, Q., et al. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618.

## License

MIT
