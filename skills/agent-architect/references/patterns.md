# Architectural Patterns

## Pattern 1: Layered Rules

For projects with distinct domains, layer rules by path:

```
.claude/rules/
├── 00-constitution.md    # Global (no paths:)
├── 10-code-style.md      # Global
├── api/
│   └── validation.md     # paths: src/api/**
├── frontend/
│   └── components.md     # paths: src/components/**
└── testing/
    └── coverage.md       # paths: **/*.test.ts
```

**Benefits**: Only relevant rules loaded per context.

---

## Pattern 2: Skill with Script Validation

For tasks requiring deterministic validation:

```
skills/
└── data-migration/
    ├── SKILL.md
    ├── scripts/
    │   ├── validate_schema.py
    │   └── dry_run.py
    └── references/
        └── schema-spec.md
```

**SKILL.md** provides guidance, **scripts/** ensure correctness.

---

## Pattern 3: Command Orchestration

Commands orchestrate, skills provide knowledge:

```markdown
# deploy.md command

## Process

1. Invoke `agent-architect` skill to verify structure
2. Run validation: `python scripts/validate.py`
3. Use `deployment` skill for actual deployment
4. Use `write-rules` skill if new constraints discovered
```

Commands = workflow glue, Skills = reusable knowledge.

---

## Pattern 4: Reflexive Learning Loop

```
Work Session
    │
    ├─► Discover important pattern
    │       │
    │       └─► Is it a constraint?
    │           ├─ Yes → Remind user: /reflect → write-rules
    │           └─ No → Remind user: /reflect → write-skill
    │
    └─► /reflect command
            │
            ├─► Invoke agent-architect for classification
            ├─► Invoke write-rules OR write-skill
            └─► Update skill library
```

---

## Pattern 5: Subagent Specialization

```yaml
# .claude/agents/code-reviewer.md
---
name: code-reviewer
description: Review code for quality and security. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
skills: security-review, code-style
---
```

Subagent loads relevant skills automatically via `skills:` field.

---

## Pattern 6: Constitution as Modular Rules

Instead of monolithic `<law>` blocks:

```
.claude/rules/
├── 00-constitution.md      # Core laws (global)
├── 01-communication.md     # Law 5: Concise responses
├── 02-skill-discovery.md   # Law 6: Check skills first
├── 03-parallel-work.md     # Law 7: Use agents
└── 04-reflection.md        # Reflexive law
```

Each law is a separate, focused file.
