---
name: creating-plugins
description: Scaffolds a new Claude Code plugin with proper structure. Use when creating a new plugin package with skills and manifests.
---

# Creating Plugins

Create a new Claude Code plugin with the specified name and type.

## Process

### 1. Validate Input

- Ensure name is kebab-case (lowercase, hyphens only)
- Determine type: skill-only or full plugin

### 2. Create Directory Structure

**Full Plugin**:
```
<name>/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── <name>/
│       └── SKILL.md
└── README.md
```

**Skill Only**:
```
<name>/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── <name>/
        └── SKILL.md
```

### 3. Generate Files

Create plugin.json with:
- Name from input
- Placeholder description
- Version 1.0.0
- Author from git config

Create skill template following `writing-skills` skill patterns:
- Gerund naming convention
- Third-person description with "Use when..."
- Progressive disclosure structure

### 4. Output

Display:
- Created file structure
- Next steps for customization
- Installation command for testing:

```bash
claude plugin add <path-to-plugin>
```
