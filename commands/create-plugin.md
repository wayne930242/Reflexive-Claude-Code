---
name: create-plugin
description: Scaffold a new Claude Code plugin with proper structure
arguments:
  - name: name
    description: Plugin name (kebab-case, e.g., my-plugin)
    required: true
  - name: type
    description: Plugin type - skill, command, or full (default: full)
    required: false
---

# Create Plugin Command

Create a new Claude Code plugin with the specified name and type.

## Process

### 1. Validate Input

- Ensure name is kebab-case (lowercase, hyphens only)
- Default type to "full" if not specified

### 2. Create Directory Structure

Based on type:

**Full Plugin** (default):
```
<name>/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── example.md
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
├── skills/
│   └── <name>/
│       └── SKILL.md
└── README.md
```

**Command Only**:
```
<name>/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── <name>.md
└── README.md
```

### 3. Generate Files

Create plugin.json with:
- Name from argument
- Placeholder description
- Version 1.0.0
- Author from git config

Create appropriate skill/command templates.

### 4. Output

Display:
- Created file structure
- Next steps for customization
- Installation command for testing

## Example Usage

```
/create-plugin my-awesome-tool
/create-plugin code-reviewer skill
/create-plugin deploy-helper command
```
