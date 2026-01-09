# Before/After Examples

## Example 1: Description

### ❌ Before (Bad)
```yaml
description: A skill for working with documents.
```

### ✅ After (Good)
```yaml
description: Create and edit Word documents with tracked changes and comments. Use when working with .docx files, adding comments, or reviewing document changes.
```

## Example 2: Body Length

### ❌ Before (Too Long)
```markdown
# Document Skill

## Introduction
This skill helps you work with documents...
[200+ lines of explanation]

## When to Use This Skill
Use this skill when you need to...
```

### ✅ After (Concise)
```markdown
# Document Skill

## Quick Start
Create document: `python scripts/create.py output.docx`

## Operations
- **Create**: See [create.md](references/create.md)
- **Edit**: See [edit.md](references/edit.md)
```

## Example 3: Instructions

### ❌ Before (Vague)
```markdown
Run the appropriate command to process the file.
```

### ✅ After (Specific)
```markdown
Extract text:
```bash
python scripts/extract.py input.pdf --output text.txt
```

## Example 4: Skill Structure

### ❌ Before (Flat)
```
my-skill/
├── SKILL.md (300 lines)
├── README.md
└── CHANGELOG.md
```

### ✅ After (Progressive)
```
my-skill/
├── SKILL.md (80 lines)
├── scripts/
│   └── process.py
└── references/
    ├── api.md
    └── examples.md
```

## Example 5: Shared Conventions

### ❌ Before (Duplicated in Multiple Skills)
```markdown
# api-client/SKILL.md
- Use async/await for all HTTP calls
- Handle errors with try/catch

# data-fetcher/SKILL.md
- Use async/await for all HTTP calls
- Handle errors with try/catch
```

### ✅ After (Extracted to Rule)
```yaml
# .claude/rules/async-conventions.md
---
paths: src/**/*.ts
---

# Async Conventions
- Use async/await for async operations
- Handle errors with try/catch
```

**Action**: Use `write-rules` skill to create shared conventions across skills.
