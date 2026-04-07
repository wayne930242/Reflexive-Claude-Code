# Frontmatter Validator Hook — Design Spec

Date: 2026-04-07

## Overview

A Claude Code plugin-level hook that validates SKILL.md, agent, and rule files after editing. Runs non-blocking checks and surfaces warnings via `systemMessage`. Also validates plugin manifests via `claude plugin validate`.

---

## Trigger

**Event:** `PostToolUse`
**Matcher:** `Edit|Write`
**Blocking:** No (exit 0, warn via `systemMessage`)

Path filtering is handled inside the script (not via `if` field), because `if` uses permission rule syntax that cannot do directory glob matching.

---

## File Discovery (Dynamic, Not Hardcoded)

The script discovers valid paths at runtime:

1. Walk CWD for all `.claude-plugin/plugin.json` files
   - Plugin root = parent of `.claude-plugin/`
   - Read `skills` and `agents` fields from plugin.json; fall back to `skills/` and `agents/` if absent
2. Also include `.claude/skills/` and `.claude/agents/` (project-level, non-plugin)

If the edited file is not in any discovered skill/agent/rule/manifest path → silent exit.

---

## Checks Per File Type

### SKILL.md (`${skill_root}/*/SKILL.md`)

| # | Check | Output |
|---|-------|--------|
| ① | Frontmatter extra fields (allowed: `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`) | WARN |
| ② | Markdown links `[text](path)` — relative path does not exist (resolved from SKILL.md dir) | WARN |
| ③ | Files in skill directory not mentioned in any SKILL.md markdown link (orphaned) | WARN |
| ④ | Content contains `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_PLUGIN_DATA}` (hooks-only variables, invalid in SKILL.md) | WARN |

### agents/*.md

| # | Check | Output |
|---|-------|--------|
| ① | Frontmatter extra fields (allowed: `name`, `description`, `model`, `context`, `tools`) | WARN |

### .claude/rules/*.md

| # | Check | Output |
|---|-------|--------|
| ① | Frontmatter extra fields (allowed: `paths`) | WARN |

### .claude-plugin/plugin.json or marketplace.json

| Check | Output |
|-------|--------|
| Run `claude plugin validate` | Pass through stdout/stderr as `systemMessage` |

---

## Script Design

### Files

```
plugins/rcc/
├── .claude-plugin/plugin.json   ← add "hooks": "./hooks/hooks.json"
└── hooks/
    ├── hooks.json
    └── validate_frontmatter.py
```

### hooks.json

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "uv run \"${CLAUDE_PLUGIN_ROOT}/hooks/validate_frontmatter.py\" 2>/dev/null || python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/validate_frontmatter.py\"",
          "timeout": 15
        }
      ]
    }
  ]
}
```

### validate_frontmatter.py

- **Runtime:** uv first (PEP 723 inline metadata), fallback `python3`
- **Dependencies:** stdlib only (`re`, `json`, `pathlib`, `subprocess`)
- **Input:** JSON from stdin (`tool_input.file_path`, `cwd`)
- **Output:** JSON `{ "systemMessage": "..." }` to stdout on warnings; silent exit 0 if clean

**Script flow:**

```
read stdin → get file_path, cwd
absolute_path = resolve(cwd, file_path)

discover_plugin_roots(cwd) → list of (skill_dir, agents_dir)
also check .claude/skills/, .claude/agents/, .claude/rules/

determine file_type:
  SKILL.md      → checks ①②③④
  agent .md     → check ①
  rules .md     → check ①
  plugin.json / marketplace.json → claude plugin validate
  else          → exit 0

collect warnings[]
if warnings → output systemMessage JSON
else        → exit 0
```

**Frontmatter parsing:** Regex-based extraction of `---` block, split on newlines, parse `key:` prefixes. No external YAML library needed for simple scalar frontmatter.

**Markdown link extraction (check ②③):** `re.findall(r'\[.*?\]\(([^)]+)\)', content)` — filter out `http(s)://` links, resolve remaining paths relative to SKILL.md directory.

---

## Output Format

Single `systemMessage` concatenating all warnings:

```
⚠ validate-frontmatter [path/to/SKILL.md]:
  - extra frontmatter field: "tags"
  - broken link: references/missing.md
  - orphaned file: references/old-draft.md
  - invalid variable: ${CLAUDE_PLUGIN_ROOT} (hooks-only, not valid in SKILL.md)
```

---

## Windows Support

- Primary: `uv run validate_frontmatter.py`
- Fallback: `python3 validate_frontmatter.py`
- No shell-specific syntax in the Python script itself → cross-platform

---

## What This Does NOT Catch (Out of Scope)

- Semantic correctness of description text
- Frontmatter value format validation (e.g., model name validity)
- Rules frontmatter validation beyond allowed fields
- Agent `tools` array value validation
