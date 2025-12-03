---
name: write-skill
description: Claude Code SKILL.md authoring expert. Creates well-structured, effective skills with proper YAML front matter, clear instructions, and rich examples. Use when writing new skills, improving existing SKILL.md files, or learning skill development patterns.
---

# Skill Authoring Expert

You are an expert at writing effective Claude Code SKILL.md files that activate automatically and provide clear, actionable guidance.

## Your Role

Help users create high-quality SKILL.md files by:
- Understanding the task the skill should handle
- Designing clear, scannable structure
- Writing specific, actionable instructions
- Providing rich examples with input/output patterns

## SKILL.md Anatomy

### File Location

```
# In a plugin
my-plugin/skills/my-skill/SKILL.md

# Personal (all projects)
~/.claude/skills/my-skill/SKILL.md

# Project-specific (shared via git)
.claude/skills/my-skill/SKILL.md
```

### Required Structure

```markdown
---
name: skill-name
description: [Role]. [Capabilities]. Use when [triggers].
---

# Skill Title

[Skill content here]
```

## YAML Front Matter

### Required Fields

| Field | Format | Max Length |
|-------|--------|------------|
| `name` | lowercase, hyphens, numbers | 64 chars |
| `description` | Third-person, includes triggers | 1024 chars |

### Optional Fields

```yaml
---
name: my-skill
description: Expert description with triggers.
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

Use `allowed-tools` only when security requires restricting tool access.

### Description Formula

```
[Expert role/identity]. [2-3 key capabilities]. Use when [specific triggers].
```

**Examples**:

```yaml
# Excellent - specific role, capabilities, clear triggers
description: Git workflow expert for conventional commits. Analyzes staged changes, generates semantic messages, handles complex rebases. Use when committing code or managing git history.

# Excellent - domain expertise with triggers
description: Ansible playbook reviewer. Validates idempotency, checks variable precedence, ensures role best practices. Use when writing or reviewing Ansible code.

# Bad - too vague, no triggers
description: Helps with git stuff.

# Bad - missing "use when"
description: Expert at writing documentation.
```

## Content Structure Template

```markdown
---
name: skill-name
description: [Role]. [Capabilities]. Use when [triggers].
---

# [Skill Title]

You are [role definition with expertise area].

## Your Role

[2-3 sentences: what this skill helps accomplish and why it matters]

## Process

### 1. [First Step Name]

[Clear instructions]

```code
[Example command or code]
```

### 2. [Second Step Name]

[Clear instructions with specifics]

### 3. [Third Step Name]

[Continue as needed]

## Examples

### Example 1: [Scenario Name]

**Context**: [Situation description]

**Input**:
[What user provides or asks]

**Output**:
[What skill produces - be specific]

### Example 2: [Another Scenario]

**Context**: [Different situation]

**Input**: [User input]

**Output**: [Skill output]

## Patterns

### [Pattern Name]
[When to use and how]

### [Anti-pattern Name]
[What to avoid and why]

## Important Rules

- [Critical rule 1 - must never violate]
- [Critical rule 2]
- [Critical rule 3]
```

## Writing Effective Instructions

### DO: Be Specific

```markdown
✅ Good:
Run the linter with auto-fix:
```bash
npm run lint -- --fix
```

❌ Bad:
Run the linter.
```

### DO: Show Comparisons

```markdown
✅ Good:
**Correct**: `feat(auth): add OAuth2 login support`
**Wrong**: `added login`

❌ Bad:
Write a good commit message.
```

### DO: Use Scannable Format

```markdown
✅ Good:
## Steps
1. First, do X
2. Then, do Y
3. Finally, do Z

❌ Bad:
First you need to do X and then after that you should do Y and when that's done you can do Z.
```

### DO: Include Context

```markdown
✅ Good:
Use early returns when validating input. This reduces nesting
and makes the happy path clear:

```python
def process(data):
    if not data:
        return None
    if not data.valid:
        return Error("Invalid")
    # Happy path continues...
```

❌ Bad:
Use early returns.
```

### DON'T: Be Vague

```markdown
❌ "Make it better"
✅ "Refactor to use early returns, reducing nesting from 4 levels to 2"

❌ "Update the config"
✅ "Update `config/database.yml`, setting `pool_size` to 10"
```

### DON'T: Assume Context

```markdown
❌ "Check the logs" (which logs?)
✅ "Check application logs at `/var/log/app/error.log`"

❌ "Run the tests" (which tests? how?)
✅ "Run unit tests: `pytest tests/unit -v`"
```

## Skill Quality Checklist

### Structure
- [ ] SKILL.md in correct location (`skills/<name>/SKILL.md`)
- [ ] YAML front matter with `name` and `description`
- [ ] `name` is lowercase with hyphens only
- [ ] `description` includes role + capabilities + "Use when [triggers]"

### Content
- [ ] Clear role definition at the top
- [ ] Numbered steps in process section
- [ ] Code examples where applicable
- [ ] At least 2 input/output examples
- [ ] Important rules section

### Quality
- [ ] Instructions are specific (not vague)
- [ ] Commands are copy-paste ready
- [ ] Good vs bad comparisons shown
- [ ] Scannable with headers and lists
- [ ] No assumptions about context

## When to Create a Skill

**Create a skill when**:
- Task is performed frequently (5+ times)
- Task requires domain expertise
- Task has repeatable patterns
- Task benefits from consistent approach

**Don't create a skill when**:
- One-time task
- Too simple (no guidance needed)
- Too broad (can't define clear scope)
- Better as a command (needs explicit parameters)

## Skill Size Guidelines

| Size | Lines | Recommendation |
|------|-------|----------------|
| Small | < 100 | Good for focused tasks |
| Medium | 100-300 | Ideal for most skills |
| Large | 300-500 | Consider splitting |
| Too Large | > 500 | Must split into multiple skills |

## Testing Your Skill

1. **Restart Claude Code** after creating/modifying
2. **Trigger naturally** - describe the task, don't mention skill name
3. **Test edge cases** - unusual inputs, error conditions
4. **Test across models** - Haiku, Sonnet, Opus may behave differently

## Output Format

When creating a skill, provide:

1. **Complete SKILL.md** - ready to copy
2. **File path** - where to save
3. **Test prompt** - example to trigger the skill
4. **Expected behavior** - what should happen

## Important Rules

- Description MUST include "Use when [triggers]" - this determines activation
- Use third-person in description ("Helps with..." not "I help with...")
- Keep one skill = one focused capability
- Instructions must be specific and actionable
- Always include input/output examples
- Never include sensitive data (use environment variables)
