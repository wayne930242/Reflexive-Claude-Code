# Component Specifications

## Rules (`.claude/rules/`)

**Purpose**: Constraints that MUST be followed. Auto-injected into context.

**Format**:
```yaml
---
paths: src/api/**/*.ts  # Optional: conditional trigger
---

# Rule Title

- Constraint 1
- Constraint 2
```

**Guidelines**:
- < 50 lines per file (auto-injected = token expensive)
- No procedures, only constraints
- Use `paths:` for domain-specific rules
- No `paths:` = global rule

**Glob Patterns**:
| Pattern | Matches |
|---------|---------|
| `**/*.ts` | All TypeScript files |
| `src/api/**` | All files under src/api/ |
| `*.md` | Markdown in root only |
| `{src,lib}/**/*.ts` | Multiple directories |

---

## Skills (`.claude/skills/`)

**Purpose**: Capabilities and how-to knowledge. Claude decides when to use.

**Structure**:
```
skill-name/
├── SKILL.md           # < 200 lines
├── references/        # Detailed docs
├── scripts/           # Executable code
└── assets/            # Templates
```

**Frontmatter**:
```yaml
---
name: skill-name
description: [What]. [Capabilities]. Use when [triggers].
---
```

**Guidelines**:
- Trigger in description, not body
- < 200 lines in SKILL.md
- Move details to references/
- Imperative voice

---

## Commands (`.claude/commands/`)

**Purpose**: User-triggered workflows. Explicit `/command` invocation.

**Format**:
```yaml
---
name: command-name
description: What this command does
arguments:
  - name: arg1
    description: Argument description
    required: false
---

# Command Title

Instructions for executing the command...
```

**Guidelines**:
- Don't duplicate skill content
- Reference skills instead: "Use the `write-skill` skill to..."
- Focus on workflow orchestration
- Can be longer (not auto-injected)

---

## Subagents (`.claude/agents/`)

**Purpose**: Specialized agents with isolated context.

**Format**:
```yaml
---
name: agent-name
description: When to use this agent. Use proactively when [triggers].
tools: Read, Grep, Glob, Bash
model: sonnet
skills: skill1, skill2
---

System prompt for the agent...
```

**Guidelines**:
- Limit tools to what's needed
- Use `skills:` to auto-load relevant skills
- Clear description for automatic invocation
- Isolated context = good for large tasks

---

## CLAUDE.md

**Purpose**: High-level project overview. Auto-injected.

**Structure**:
```markdown
# Project Name

One-line description.

## Quick Reference

### Commands
- `npm run build`: Build project
- `npm test`: Run tests

### Key Paths
- `src/`: Source code
- `tests/`: Test files

## Imports

@.claude/rules/constitution.md
```

**Guidelines**:
- < 300 lines
- Use `@import` for modularity
- High-level only, details in rules/skills
- No procedures (use skills)
