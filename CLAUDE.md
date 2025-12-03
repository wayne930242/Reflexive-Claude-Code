# CLAUDE.md

This repository contains Claude Code skills (plugins) for enhanced productivity.

## Project Overview

**weihung-claude-plugin** is a collection of reusable Claude Code skills that can be installed globally or per-project.

## Repository Structure

```
weihung-claude-plugin/
├── .claude/
│   └── skills/           # Claude Code skills
│       └── write-skill/  # Meta-skill for creating skills
├── CLAUDE.md             # This file
└── README.md             # Project documentation
```

## Skills Development

### Creating New Skills

1. Create a new directory under `.claude/skills/`
2. Add a `SKILL.md` file with proper YAML front matter
3. Follow the structure defined in `write-skill`

### Testing Skills

1. Copy the skill to `~/.claude/skills/` for personal testing
2. Start a new Claude Code session
3. Trigger the skill by describing a relevant task

## Key Principles

1. **Clear descriptions** - Skills are invoked based on their description
2. **Specific instructions** - Provide exact steps, not vague guidance
3. **Rich examples** - Show input/output patterns
4. **Focused scope** - One skill = one well-defined capability
