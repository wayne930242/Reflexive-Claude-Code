# Component Planning Reference

## Component Evaluation Table

For each component type, evaluate:

| Component | Input Sources | AI Security Considerations | Decision |
|-----------|--------------|---------------------------|----------|
| CLAUDE.md | Workflow conventions + analysis constitution findings | AI 生成程式碼規範 | Create / Modify / Keep |
| Rules | Workflow conventions + analysis path-match findings | 程式碼模式約束規則 | Which rules, with paths: globs |
| Hooks | Workflow quality checks + analysis security findings | AI 程式碼掃描、漏洞檢測 | Which hooks, which events |
| Skills | Workflow repeated tasks | 生成程式碼品質關卡 | Which skills |
| Agents | Workflow isolated analysis needs | 獨立安全審查代理 | Which agents (read-only only) |

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

## Skill Asset Planning

Each skill can bundle three types of supporting assets. Plan these alongside the skill, not as an afterthought.

```
my-skill/
├── SKILL.md           # Instructions (required)
├── references/        # On-demand documentation, examples
├── scripts/           # Executable scaffolders, validators
└── templates/         # Reusable file templates for output
```

| Signal | Asset Type | Directory | Example |
|--------|-----------|-----------|---------|
| Skill creates files with boilerplate | Scaffolder script | `scripts/` | `add_hook.py` in writing-hooks |
| Skill produces structured reports or configs | Output template | `templates/` | Report format, config skeleton |
| Skill validates file format or structure | Validator script | `scripts/` | `validate_skill.py` in writing-skills |
| Skill has complex multi-file setup | Initializer script | `scripts/` | `init_claude_md.py` in writing-claude-md |
| Skill references large documentation | Reference docs | `references/` | Checklists, pattern catalogs, examples |

**`references/`** = documentation Claude reads on demand (loaded via markdown links).
**`scripts/`** = executable code Claude runs (scaffolders, validators, initializers).
**`templates/`** = file skeletons Claude copies and fills in (report formats, config files, boilerplate).

**Decision:** If a skill will be invoked repeatedly and involves file creation or structured output, plan the corresponding asset. Scripts automate; templates standardize; references inform.

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
