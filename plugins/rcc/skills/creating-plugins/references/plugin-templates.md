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

## Release Automation Templates

### release-please-config.json

Adjust `extra-files` paths to every file that carries a version string.

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "simple",
      "package-name": "<plugin-name>",
      "include-component-in-tag": false,
      "extra-files": [
        { "type": "json", "path": ".claude-plugin/marketplace.json", "jsonpath": "$.metadata.version" },
        { "type": "json", "path": ".claude-plugin/marketplace.json", "jsonpath": "$.plugins[0].version" },
        { "type": "json", "path": "plugins/<plugin-name>/.claude-plugin/plugin.json", "jsonpath": "$.version" },
        { "type": "generic", "path": "README.md" }
      ]
    }
  }
}
```

### .release-please-manifest.json

```json
{ ".": "<current-version>" }
```

### .github/workflows/release-please.yml

```yaml
name: Release Please
on:
  push:
    branches: [main]
permissions:
  contents: write
  pull-requests: write
jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          config-file: release-please-config.json
          manifest-file: .release-please-manifest.json
```

### README version marker

Tag each README line that holds a version with an HTML comment:

```markdown
### <plugin-name> (v1.0.0) <!-- x-release-please-version -->
```

The `generic` updater rewrites the version on lines carrying this marker.

## Shell Injection Syntax (in SKILL.md)

Skills can inject live shell output as preprocessing. The harness scans SKILL.md, executes the shell command, and substitutes stdout before Claude sees the file.

**Inline form** — single backticks prefixed with `!`:

```
!`git status`
```

CWD is the user's project directory.

**Plugin-internal file form** — same inline syntax, useful for bundled context files:

```
!`cat "${CLAUDE_SKILL_DIR}/references/context.md"`
```

**Multi-line block form** — fenced code block with `!` immediately after the opening backticks:

````
```!
git log --oneline -5
git status --short
```
````

The runner executes the entire block as one shell script.

**WARNING:** Do NOT use the literal multi-line form anywhere in a SKILL.md (even inside example code blocks). The preprocessor scans the raw file and will try to execute it. To document the syntax, use a four-backtick wrapper as shown above, or describe it in prose.

**PowerShell:** set `shell: powershell` in skill frontmatter AND require user env `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Ask which shell the user runs if cross-platform support matters.

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
