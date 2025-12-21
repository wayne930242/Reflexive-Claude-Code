---
name: add-law
description: Add a new law to the CLAUDE.md constitution
arguments:
  - name: law_content
    description: Law description (format: "Name: constraint1, constraint2")
    required: false
---

# Add Law to Constitution

Add a new law to the `<law>` block in CLAUDE.md.

## Process

### 1. Locate CLAUDE.md

Search for CLAUDE.md in:
1. Project root (`./CLAUDE.md`)
2. `.claude/` directory (`.claude/CLAUDE.md`)

If not found, inform user and suggest `/migration` or `/init-project`.

### 2. Parse Existing Laws

Read the `<law>` block and identify:
- Current number of laws
- Format pattern (e.g., `**Law N: Name**` with bullet points)

### 3. Gather New Law Details

If `$ARGUMENTS` provided, parse it:
- Format: `"Name: constraint1, constraint2"`
- Example: `"Testing: Run tests before commit, Maintain 80% coverage"`

If not provided, ask:
- **Law Name**: Short name (e.g., "Error Handling")
- **Constraints**: Specific rules for this law

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

## Example Usage

```
/add-law
/add-law "Testing: Run tests before commit"
/add-law "Documentation: Update docs with code changes, Keep README current"
```
