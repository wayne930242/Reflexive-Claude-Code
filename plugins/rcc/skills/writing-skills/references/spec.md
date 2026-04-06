# SKILL.md Specification

Version 1.1 (2026-01)

## YAML Frontmatter

### Required Fields

| Field | Format | Max Length |
|-------|--------|------------|
| `name` | gerund form, lowercase, hyphens | 64 chars |
| `description` | Third person, includes "Use when..." | 1024 chars |

### Optional Fields

| Field | Description |
|-------|-------------|
| `argument-hint` | Autocomplete hint, e.g., `[issue-number]` |
| `disable-model-invocation` | `true` = only manual `/name` invocation |
| `user-invocable` | `false` = hidden from `/` menu, only Claude invokes |
| `allowed-tools` | Tools auto-approved when skill activates (space-separated or YAML list) |
| `model` | Model override: `sonnet`, `opus`, `haiku`, or full ID |
| `effort` | Thinking effort: `low`, `medium`, `high`, `max` (Opus 4.6 only) |
| `context` | `fork` = run in isolated subagent context |
| `agent` | Subagent type for `context: fork` (`Explore`, `Plan`, `general-purpose`, or custom agent name) |
| `hooks` | Skill lifecycle hooks |
| `paths` | Glob patterns limiting auto-activation (comma-separated or YAML list) |
| `shell` | Shell for `!` commands: `bash` (default) or `powershell` |

## String Substitution Variables

These are replaced inline in SKILL.md content before Claude sees it:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking. If absent in content, appended as `ARGUMENTS: <value>` |
| `$ARGUMENTS[N]` or `$N` | Access specific argument by 0-based index (e.g., `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | Current session ID — useful for session-specific temp files |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md — use to reference bundled scripts/data regardless of CWD |

Plugin skills also have access to:

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Plugin installation directory (changes on update — do not write here) |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory that survives updates (`~/.claude/plugins/data/{id}/`) |

## Shell Context (Dynamic Context Injection)

Skills can inject live data using shell commands. Commands execute as preprocessing — output replaces the placeholder before Claude sees the content.

**Inline form:** `` !`<command>` ``

```markdown
## Current state
- Branch: !`git branch --show-current`
- Changed files: !`git diff --name-only`
```

**Multi-line form:** Open a fenced code block with `` ```! ``:

````markdown
## Environment
```!
node --version
npm --version
git status --short
```
````

**Key behaviors:**
- Each command executes immediately as preprocessing
- Claude only sees the rendered output, not the commands
- Use shell fallbacks: `` !`git status 2>/dev/null || echo "Not a git repo"` ``
- Can be disabled via `"disableSkillShellExecution": true` in settings

**PowerShell users:** Set `shell: powershell` in frontmatter AND ensure `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` is set in the environment. Ask the user which shell they use if the plugin needs cross-platform support.

## Name Requirements

Use **gerund form** (verb + -ing):
- `processing-pdfs`, `writing-documentation`, `analyzing-code`
- Lowercase letters, numbers, hyphens only
- Must match containing directory name
- Avoid: `helper`, `utils`, reserved words (`anthropic`, `claude`)

## Description Formula

```
[What it does]. [Key capabilities]. Use when [specific triggers].
```

**Always write in third person** (description is injected into system prompt).

**Good**:
```yaml
description: Creates semantic git commits. Analyzes staged changes and generates conventional commit messages. Use when committing code or managing git history.
```

**Bad**:
```yaml
description: I can help you with git stuff.
description: You can use this for git commits.
```

## Body Guidelines

- Use imperative form ("Run the script" not "You should run")
- SKILL.md is overview; move detailed content to `references/` (loaded on-demand)
- No "When to use" sections (put in description)
- Include workflow checklists for complex tasks

## Shared Conventions

If a convention appears in multiple skills, extract to `.claude/rules/`:

- Use `write-rules` skill to create shared convention
- Skills automatically inherit rules (auto-injected)
- Keep only skill-specific details in SKILL.md

**Rule of thumb**: Rules = conventions shared across skills.
