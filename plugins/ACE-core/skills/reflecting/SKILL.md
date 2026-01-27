---
name: reflecting
description: Analyzes conversation to extract learnings and integrate into skill library or rules. Consolidates experiences into reusable knowledge. Use when completing significant work, resolving complex problems, or discovering reusable patterns.
---

# Reflecting on Learnings

Analyze the current conversation to extract learnings and integrate them appropriately.

## Process

### 1. Analyze Conversation

Review conversation history to identify:
- **Successes**: Patterns that led to good outcomes
- **Failures**: Errors or multiple attempts needed
- **New Knowledge**: Project-specific insights discovered
- **Repeated Patterns**: Actions performed multiple times

### 2. Classify Learnings

Use the `agent-architect` skill to classify each learning:

```
Is it an IMMUTABLE LAW (must enforce every response)?
├─ Yes → <law> block in CLAUDE.md
└─ No → Is it a CAPABILITY (how to do)?
    ├─ Yes → Skill
    │   └─ Is it SHARED across multiple skills?
    │       ├─ Yes → Extract to Rule (.claude/rules/)
    │       └─ No → Keep in Skill
    └─ No → Documentation only
```

### 3. Extract Knowledge

For each significant learning:

```yaml
Learning:
  context: [When this applies]
  insight: [What was learned]
  classification: [rule | skill | documentation]
  action: [create_new | enhance_existing | document_only]
```

### 4. Integrate

| Classification | Action |
|---------------|--------|
| Immutable Law | Add to `<law>` block in CLAUDE.md |
| Skill | Use `writing-skills` skill |
| Shared Rule | Use `writing-rules` skill |
| Documentation | Add to appropriate `references/` |

### 5. Review Existing Components

```bash
ls .claude/rules/ 2>/dev/null
find . -name "SKILL.md" -type f
```

Determine if learnings enhance existing components or warrant new ones.

## Output Format

```markdown
## Session Learnings

### Rules Created/Updated
- [rule-file]: [constraint added]

### Skills Created/Updated
- [skill-name]: [capability added]

### Recommendations
- [Follow-up actions]
```
