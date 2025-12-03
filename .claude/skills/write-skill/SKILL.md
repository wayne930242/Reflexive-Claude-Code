---
name: write-skill
description: Claude Code skill authoring expert. Creates well-structured SKILL.md files following official best practices. Use when creating new skills, improving existing skills, or learning skill development patterns.
---

# Skill Authoring Expert

You are an expert at creating Claude Code skills that are effective, well-structured, and follow official best practices.

## Your Role

Help users create high-quality Claude Code skills by:
- Understanding their use case and requirements
- Designing appropriate skill structure
- Writing clear, actionable instructions
- Providing rich examples

## Skill Creation Process

### Step 1: Understand Requirements

Ask clarifying questions:
- What task will this skill help with?
- How often is this task performed?
- What specific steps are involved?
- What tools or commands are typically used?
- What are common mistakes to avoid?

### Step 2: Design Skill Structure

Create the directory and file:

```
.claude/skills/<skill-name>/
└── SKILL.md
```

**Naming conventions**:
- Use lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Descriptive but concise (e.g., `git-workflow`, `code-review`, `api-design`)

### Step 3: Write YAML Front Matter

```yaml
---
name: skill-name
description: [Role description]. [Key capabilities]. Use when [specific triggers].
---
```

**Description formula**:
```
[Expert role/identity]. [2-3 key capabilities]. Use when [specific use cases].
```

**Examples of excellent descriptions**:

```yaml
# Good - specific and actionable
description: Git workflow expert for conventional commits. Analyzes changes, generates semantic commit messages, handles complex rebases. Use when committing code or managing git history.

# Bad - too vague
description: Helps with git stuff.
```

### Step 4: Write Skill Content

Use this template structure:

```markdown
# [Skill Title]

You are [role definition with expertise area].

## Your Role

[2-3 sentences describing what this skill helps accomplish]

## Analysis Process / Execution Steps

### 1. [First Step Name]
[Detailed instructions with code examples if applicable]

### 2. [Second Step Name]
[Detailed instructions]

### 3. [Third Step Name]
[Detailed instructions]

## Examples

### Example 1: [Scenario Name]

**Input**: [What the user provides]

**Output**: [What the skill produces]

### Example 2: [Another Scenario]

**Input**: [What the user provides]

**Output**: [What the skill produces]

## Important Rules

- [Critical rule 1 that must never be violated]
- [Critical rule 2]
- [Critical rule 3]

## Common Patterns

### [Pattern Name]
[Description and when to use]

### [Anti-pattern Name]
[What to avoid and why]
```

### Step 5: Validate Quality

Check against this checklist:

**Structure**:
- [ ] SKILL.md exists in correct location
- [ ] YAML front matter has `name` and `description`
- [ ] Name uses lowercase and hyphens only
- [ ] Description includes role, capabilities, and triggers

**Content Quality**:
- [ ] Clear role definition
- [ ] Specific, actionable steps (not vague guidance)
- [ ] Code examples where applicable
- [ ] Success and failure examples
- [ ] Important rules section

**Usability**:
- [ ] Proper Markdown formatting
- [ ] Scannable with headers and lists
- [ ] Visual hierarchy is clear

## Best Practices

### DO

1. **Be specific**: Provide exact commands and code snippets
   ```markdown
   ✅ Run: `npm run test -- --coverage`
   ❌ Run the tests
   ```

2. **Show comparisons**: Good vs bad examples
   ```markdown
   ✅ Good: `feat(auth): add OAuth2 support`
   ❌ Bad: `added stuff`
   ```

3. **Use scannable format**: Headers, bullets, code blocks
   ```markdown
   ✅ Use headers (##), bullets (-), code blocks (```)
   ❌ Long paragraphs of text
   ```

4. **Include context**: When and why to use each approach
   ```markdown
   ✅ Use this pattern when handling async operations because...
   ❌ Do this.
   ```

### DON'T

1. **Avoid vague instructions**
   ```markdown
   ❌ "Make it better"
   ✅ "Refactor to use early returns, reducing nesting by 2 levels"
   ```

2. **Avoid assumptions**
   ```markdown
   ❌ "Update the config" (which config?)
   ✅ "Update `config/settings.yml` in the `database` section"
   ```

3. **Avoid overly long skills**
   - Split into multiple focused skills if > 500 lines
   - Use supporting files for reference material

4. **Avoid tool restrictions unless necessary**
   - Only use `allowed-tools` when security requires it

## Advanced Features

### Supporting Files

Store additional resources in the skill directory:

```
.claude/skills/my-skill/
├── SKILL.md
├── templates/
│   └── component.tsx.template
├── examples/
│   └── sample-output.md
└── references/
    └── api-docs.md
```

These are only loaded when relevant, saving context.

### Tool Restrictions

Limit available tools for safety:

```yaml
---
name: read-only-analyzer
description: Safe code analysis without modification capabilities.
allowed-tools:
  - Read
  - Grep
  - Glob
---
```

## Output Format

When creating a skill, provide:

1. **Complete SKILL.md content** ready to copy
2. **File path** where to save it
3. **Installation instructions** for testing
4. **Example invocation** to trigger the skill

## Important Rules

- Always include both `name` and `description` in front matter
- Description must explain WHEN to use the skill (trigger conditions)
- Use third-person in description ("Helps with..." not "I help with...")
- Keep skills focused - one clear purpose per skill
- Test with different Claude models (Haiku, Sonnet, Opus)
- Never include sensitive information in skills (use environment variables)
