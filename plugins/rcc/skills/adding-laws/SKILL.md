---
name: adding-laws
description: Adds a new law to the CLAUDE.md constitution. Use when establishing new immutable constraints that must be enforced in every response.
---

# Adding Laws

Add a new law to the `<law>` block in CLAUDE.md.

## Process

### 1. Locate CLAUDE.md

Search for CLAUDE.md in:
1. Project root (`./CLAUDE.md`)
2. `.claude/` directory (`.claude/CLAUDE.md`)

If not found, suggest `migrating-agent-systems` or `initializing-projects` skill.

### 2. Parse Existing Laws

Read the `<law>` block and identify:
- Current number of laws
- Format pattern (e.g., `**Law N: Name**` with bullet points)

### 3. Gather New Law Details

Ask for:
- **Law Name**: Short name (e.g., "Error Handling")
- **Constraints**: Specific rules for this law

Format: `"Name: constraint1, constraint2"`
Example: `"Testing: Run tests before commit, Maintain 80% coverage"`

### 4. Format New Law

```markdown
**Law N: [Law Name]**
- [Constraint 1]
- [Constraint 2]
```

N = (current max law number) + 1

### 5. Insert Law

Insert before `</law>`, after the last existing law.

### 6. Validate

- [ ] Law number is sequential
- [ ] Format matches existing laws
- [ ] `<law>` block remains valid
- [ ] No duplicate law names
