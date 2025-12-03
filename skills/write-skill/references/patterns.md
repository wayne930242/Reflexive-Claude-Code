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

## Anti-Patterns

### ❌ Deeply Nested References
Keep references one level deep from SKILL.md.

### ❌ Duplicate Information
Don't repeat content in SKILL.md and references.

### ❌ Verbose Explanations
Claude already knows basics—add only non-obvious knowledge.

### ❌ Auxiliary Files
No README.md, CHANGELOG.md in skills.
