---
name: reflect
description: Reflect on conversation learnings and integrate into skill library. Consolidates successful/failed experiences into abstract, reusable skills.
arguments:
  - name: focus
    description: Optional focus area to reflect on (e.g., "error-handling", "testing")
    required: false
---

# Reflection Protocol

Analyze the current conversation to extract learnings and integrate them into the skill library.

## Process

### 1. Conversation Analysis

Review the conversation history to identify:

- **Successes**: What worked well? What patterns led to good outcomes?
- **Failures**: What didn't work? What caused errors or required multiple attempts?
- **New Knowledge**: Project-specific insights, domain knowledge, or techniques discovered
- **Repeated Patterns**: Actions performed multiple times that could be abstracted

### 2. Skill Library Review

Before creating new skills, scan existing skills:

```
skills/
├── write-skill/
├── write-command/
├── write-plugin/
└── [other skills...]
```

Determine:
- Can learnings enhance an existing skill?
- Is a new skill warranted, or would it overlap?
- Are there skills that should be merged or deprecated?

### 3. Knowledge Extraction

For each significant learning, structure it as:

```yaml
Learning:
  context: [When this applies]
  insight: [What was learned]
  abstraction_level: [high/medium/low - how generalizable?]
  action: [enhance_existing | create_new | document_only]
```

### 4. Skill Integration

**If enhancing existing skill:**
- Add pattern to existing SKILL.md
- Move detailed examples to `references/` directory

**If creating new skill:**
- Use `write-skill` patterns
- Ensure abstraction level is appropriate (not too project-specific)
- Create `references/` directory for:
  - Code examples from this session
  - Detailed documentation
  - Edge cases encountered

**If documenting only:**
- Add to appropriate `references/` file
- Link from relevant skill

### 5. Skill Refactoring

After integration, run `/refactor-skills` to:
- Consolidate overlapping skills
- Ensure consistent abstraction levels
- Remove redundancy

## Abstraction Guidelines

Skills should be **abstract enough** to apply across projects:

| Too Specific | Good Abstraction |
|--------------|------------------|
| "Fix TypeScript error TS2345 in UserService" | "Resolve type mismatches in service layers" |
| "Add loading state to ProductList component" | "Implement loading states in data-fetching components" |
| "Configure Jest for this monorepo" | "Set up testing in monorepo architectures" |

## Output Format

After reflection, provide:

1. **Summary**: Key learnings from session
2. **Actions Taken**: Skills created/enhanced
3. **Skill Map**: Updated skill relationships

```
Session Learnings:
- [Learning 1]: Integrated into [skill-name]
- [Learning 2]: New skill created: [skill-name]
- [Learning 3]: Documented in [skill]/references/[file]

Skills Modified:
- [skill-name]: [what changed]

Recommendations:
- [Any suggested follow-up actions]
```

## When to Reflect

- At end of significant work sessions
- After resolving complex problems
- When discovering reusable patterns
- Before context window fills up
