# rcc Plugin

Skills-driven Agentic Context Engineering (ACE) for Claude Code.

## What This Plugin Provides

A complete toolkit for building, analyzing, and maintaining Claude Code agent systems with structured workflows and automated quality review.

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `migrating-agent-systems` | "setup agent", "migrate agent system" | Detect maturity and route to correct pipeline |
| `analyzing-agent-systems` | "analyze agent system", "audit agent config" | 11-category weakness checklist |
| `brainstorming-workflows` | "explore workflows", "brainstorm workflows" | Workflow discovery and Anthropic pattern mapping |
| `planning-agent-systems` | Called by brainstorming | Component planning with dependency graph |
| `applying-agent-systems` | "apply agent plan" | Build components in dependency order |
| `reviewing-agent-systems` | "review agent system", "check quality" | Quality review after creation |
| `refactoring-agent-systems` | "cleanup agent system", "refactor agent setup" | Clean up and consolidate components |
| `writing-claude-md` | "create CLAUDE.md", "setup project" | CLAUDE.md creation and improvement |
| `writing-rules` | "add convention", "add rule" | Path-scoped rule creation |
| `writing-skills` | "create a skill", "write a skill" | Skill authoring |
| `writing-subagents` | "create agent", "add reviewer" | Subagent creation |
| `writing-hooks` | "add hook", "enforce linting" | Hook creation |
| `advising-architecture` | "classify component", "check component type" | Component type classification |
| `reflecting` | "reflect", "what did we learn" | Session learning extraction |
| `learning-from-failures` | After failures or debug sessions | Failure pattern archival |
| `migrating-plugins` | "setup plugin", "migrate plugin" | Plugin setup and migration routing |
| `validating-plugins` | "validate plugin", "audit skills" | Plugin structure validation |
| `refactoring-plugins` | "refactor plugin", "plugin health check" | Plugin health check and fixes |
| `creating-plugins` | "create plugin", "scaffold plugin" | New plugin scaffolding |
| `improving-skills` | "improve skill", "optimize skill" | Single skill optimization |
| `refactoring-skills` | "refactor skills", "consolidate skills" | Multi-skill consolidation |
| `initializing-projects` | "new project", "initialize project" | Project bootstrap |

## Quality Reviewers (Agents)

| Agent | Model | Reviews |
|-------|-------|---------|
| `claudemd-reviewer` | sonnet | CLAUDE.md instruction quality |
| `rule-reviewer` | opus | Rule frontmatter, glob coverage, duplication |
| `skill-reviewer` | opus | Skill structure, triggers, overlap |
| `subagent-reviewer` | opus | Agent frontmatter, tools, model selection |
| `hook-reviewer` | opus | Exit codes, registration, security |

## Commands

- `/rcc:init` — Initialize new project with Claude Code agent system
- `/rcc:init-plugin` — Scaffold a new plugin package
- `/rcc:migrate` — Migrate existing agent system
- `/rcc:migrate-plugin` — Setup or migrate a plugin
- `/rcc:reflect` — Analyze session and extract learnings

## Installation

```bash
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install rcc@rcc
```
