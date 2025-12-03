# Weihung Claude Plugin

A collection of Claude Code skills for enhanced productivity.

## Installation

Copy the `.claude/skills/` directory to your home directory or project:

```bash
# For personal use (available in all projects)
cp -r .claude/skills/* ~/.claude/skills/

# For project use (shared with team via git)
cp -r .claude/skills/* your-project/.claude/skills/
```

## Available Skills

### write-skill

A meta-skill that helps you create well-structured Claude Code skills following best practices.

**Usage**: Ask Claude to help you create a new skill, and this skill will be automatically invoked.

## Structure

```
.claude/skills/
└── write-skill/
    └── SKILL.md
```

## License

MIT
