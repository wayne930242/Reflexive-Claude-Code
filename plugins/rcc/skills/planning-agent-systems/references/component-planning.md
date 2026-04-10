# Component Planning Reference

## Component Evaluation Table

For each component type, evaluate:

| Component | Input Sources | Decision |
|-----------|--------------|----------|
| CLAUDE.md | Workflow conventions + analysis constitution findings | Create / Modify / Keep |
| Rules | Workflow conventions + analysis path-match findings | Which rules, with paths: globs |
| Hooks | Workflow quality checks + analysis security findings | Which hooks, which events |
| Skills | Workflow repeated tasks | Which skills |
| Agents | Workflow isolated analysis needs | Which agents (read-only only) |

## Decision Criteria

- Does this component trace to a workflow need? → Create
- Does this fix an analysis weakness? → Create/Modify
- Does it already exist and work? → Keep
- Does it conflict with another component? → Modify/Delete
- Is it speculative? → **Don't create (YAGNI)**
- Is it core or enhancement? → Tag accordingly for phased rollout

## Size Constraints

- CLAUDE.md MUST stay under 200 lines
- Each rule MUST stay under 50 lines
- Each skill MUST stay under 300 lines (< 2,000 tokens for best activation)
- Skill descriptions MUST state concrete triggers, not summaries
- Skills with side effects MUST use `disable-model-invocation: true`
- Skills with restricted scope MUST use `allowed-tools` to limit access
- Agents MUST be read-only (no `.claude/` writes)
- All `.claude/` writes happen via main conversation, never subagents

## Script and Template Planning

For each planned skill, evaluate whether it needs automation support:

| Signal | Asset to Plan | Example |
|--------|--------------|---------|
| Skill creates files with boilerplate | `scripts/` scaffolder | `add_hook.py` in writing-hooks |
| Skill produces structured reports | `references/` template | `report-template.md` in analyzing |
| Skill validates file format | `scripts/` validator | `validate_skill.py` in writing-skills |
| Skill has a complex multi-file setup | `scripts/` initializer | `init_claude_md.py` in writing-claude-md |

**Decision:** If a skill will be invoked repeatedly and involves file creation or structured output, plan a script or template alongside it. Do not defer — scaffolders are part of the skill, not an afterthought.

## Available Writing Skills

| Component | Writing Skill | Notes |
|-----------|--------------|-------|
| CLAUDE.md | `writing-claude-md` | Uses official markdown format |
| Rules | `writing-rules` | One invocation per rule |
| Hooks | `writing-hooks` | One invocation per hook |
| Skills | `writing-skills` | One invocation per skill |
| Agents | `writing-subagents` | One invocation per agent |

## Conflict Checks

Before finalizing, verify:
- Will new components duplicate existing ones?
- Will new rules conflict with existing CLAUDE.md content?
- Will new hooks overlap with existing hooks?
