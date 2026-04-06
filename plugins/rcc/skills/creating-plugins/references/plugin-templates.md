# Plugin Templates

## Manifest Format (plugin.json)

```json
{
  "name": "plugin-name",
  "description": "What this plugin does",
  "version": "1.0.0",
  "author": "Author Name",
  "skills": []
}
```

**Fields:**

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Plugin identifier (kebab-case) |
| `description` | Yes | One-line description |
| `version` | Yes | Semantic version |
| `author` | No | Author name or org |
| `skills` | No | Leave empty for auto-discovery |

Skills are auto-discovered from `skills/*/SKILL.md`. Only specify explicitly to limit exposure.

## Marketplace Structure (for multi-plugin repos)

```
<repo-root>/
├── .claude-plugin/
│   └── marketplace.json   # Lists all plugins
└── plugins/
    ├── <plugin-a>/        # Each plugin has its own .claude-plugin/
    └── <plugin-b>/
```

**marketplace.json** links to individual plugins with `"source": "./plugins/<name>"`.

## README Template

```markdown
# Plugin Name

One-line description.

## Installation

\`\`\`bash
claude plugin add <path-or-url>
\`\`\`

## Skills

| Skill | Description |
|-------|-------------|
| skill-name | What it does |

## Usage

[Examples of how to use the plugin]

## License

[License]
```
