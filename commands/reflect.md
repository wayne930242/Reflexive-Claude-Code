---
name: reflect
description: Reflect on conversation learnings and integrate into skill library or rules. Consolidates experiences into reusable knowledge.
arguments:
  - name: focus
    description: Optional focus area to reflect on (e.g., "error-handling", "testing")
    required: false
---

# Reflection Protocol

Analyze the current conversation to extract learnings and integrate them appropriately.

## Process

### 1. Conversation Analysis

Review the conversation history to identify:

- **Successes**: What worked well? What patterns led to good outcomes?
- **Failures**: What didn't work? What caused errors or required multiple attempts?
- **New Knowledge**: Project-specific insights, domain knowledge, or techniques discovered
- **Repeated Patterns**: Actions performed multiple times that could be abstracted

### 2. Invoke Architecture Advisor

Use the `agent-architect` skill to classify each learning:

```
Is it a CONSTRAINT (must follow)?
├─ Yes → Rule
└─ No → Is it a CAPABILITY (how to do)?
    ├─ Yes → Skill
    └─ No → Documentation only
```

### 3. Knowledge Extraction

For each significant learning, structure it as:

```yaml
Learning:
  context: [When this applies]
  insight: [What was learned]
  classification: [rule | skill | documentation]
  action: [create_new | enhance_existing | document_only]
```

### 4. Integration

**For Rules** (constraints, must-follow):
- Use the `write-rules` skill to create/update `.claude/rules/` files
- Consider if `paths:` scoping is needed
- Keep < 50 lines (auto-injected = token expensive)

**For Skills** (capabilities, how-to):
- If enhancing existing skill: `/improve-skill [skill-path]`
- If creating new skill: Use the `write-skill` skill
- Keep < 200 lines, use references/ for details

**For Documentation only:**
- Add to appropriate `references/` file
- Link from relevant skill's SKILL.md

### 5. Review Existing Components

Before creating new components, scan existing:

```bash
# Existing rules
ls .claude/rules/ 2>/dev/null

# Existing skills
find . -name "SKILL.md" -type f
```

Determine:
- Can learnings enhance an existing component?
- Is a new component warranted, or would it overlap?

### 6. Execution Checklist

Before completing reflection, ensure:

- [ ] Each learning classified as rule, skill, or documentation
- [ ] Rules created via `write-rules` skill (< 50 lines)
- [ ] Skills created via `write-skill` skill (< 200 lines)
- [ ] No redundancy with existing components
- [ ] Proper use of `paths:` for domain-specific rules

## Output Format

```markdown
## Session Learnings

### Rules Created/Updated
- [rule-file]: [constraint added]

### Skills Created/Updated
- [skill-name]: [capability added]

### Documentation Added
- [skill]/references/[file]: [content added]

### Recommendations
- [Any suggested follow-up actions]
```

## Abstraction Guidelines

| Too Specific | Good Abstraction |
|--------------|------------------|
| "Fix TypeScript error TS2345 in UserService" | Rule: "Type parameters MUST match" |
| "Add loading state to ProductList component" | Skill: "Implement loading states" |
| "API must validate user input" | Rule with `paths: src/api/**` |

## When to Reflect

- At end of significant work sessions
- After resolving complex problems
- When discovering reusable patterns
- Before context window fills up
