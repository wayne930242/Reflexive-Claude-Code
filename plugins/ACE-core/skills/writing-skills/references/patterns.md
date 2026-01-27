# Common Skill Patterns

## Pattern 1: High-Level Guide with References

Keep SKILL.md lean, link to detailed docs:

```markdown
# PDF Processing

## Quick start
Extract text: `python scripts/extract.py input.pdf`

## Advanced
- **Form filling**: See [forms.md](references/forms.md)
- **Encryption**: See [security.md](references/security.md)
```

## Pattern 2: Domain-Specific Organization

For multi-domain skills, organize by domain:

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── marketing.md
```

Claude loads only relevant domain file.

## Pattern 3: Framework Variants

For skills supporting multiple frameworks:

```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

## Pattern 4: Script-Heavy Skills

When operations need deterministic reliability:

```
image-editor/
├── SKILL.md (usage guide)
└── scripts/
    ├── resize.py
    ├── rotate.py
    └── convert.py
```

Benefits: Token efficient, consistent results.

## Pattern 5: Extract Shared Conventions to Rules

When multiple skills share the same convention, extract to `.claude/rules/`:

```
# BEFORE: Convention duplicated in multiple skills
skills/
├── api-client/SKILL.md     # "Use async/await..."
├── data-fetcher/SKILL.md   # "Use async/await..."
└── webhook-handler/SKILL.md # "Use async/await..."

# AFTER: Convention extracted to rule
.claude/rules/
└── async-conventions.md    # Shared convention

skills/
├── api-client/SKILL.md     # Skill-specific only
├── data-fetcher/SKILL.md
└── webhook-handler/SKILL.md
```

**Action**: Use `write-rules` skill to create shared conventions.

## Anti-Patterns

### ❌ Deeply Nested References
Keep references one level deep from SKILL.md.

### ❌ Duplicate Conventions Across Skills
If same guideline appears in multiple skills → extract to `.claude/rules/` using `write-rules` skill.

### ❌ Verbose Explanations
Claude already knows basics—add only non-obvious knowledge.

### ❌ Auxiliary Files
No README.md, CHANGELOG.md in skills.
