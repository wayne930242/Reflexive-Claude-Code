# SKILL.md Specification

Version 1.2 — synced against https://code.claude.com/docs/en/skills.md (re-verify via fetching-claude-docs before relying on this file).

## YAML Frontmatter

Per the official spec **all fields are optional**; only `description` is recommended (Claude uses it to decide when to load the skill).
`name` defaults to the directory name.
House rule: always set `name` and `description` explicitly.

| Field | Description |
|-------|-------------|
| `name` | Display name. Defaults to directory name. House: gerund form, lowercase, hyphens, max 64 chars |
| `description` | What the skill does + when to use it. Third person, max 1024 chars. See formula below |
| `when_to_use` | Extra trigger context appended to `description` in the skill listing (combined text capped at 1,536 chars) |
| `argument-hint` | Autocomplete hint, e.g., `[issue-number]` |
| `arguments` | Named positional arguments for `$name` substitution (space-separated string or YAML list) |
| `disable-model-invocation` | `true` = only manual `/name` invocation; description removed from Claude's context |
| `user-invocable` | `false` = hidden from `/` menu, only Claude invokes |
| `allowed-tools` | Tools auto-approved when skill activates (space/comma-separated or YAML list) |
| `disallowed-tools` | Tools removed from Claude's pool while the skill is active; clears on next user message |
| `model` | Model override while the skill is active. Accepts the same values as `/model`, or `inherit` |
| `effort` | Effort level: `low`, `medium`, `high`, `xhigh`, `max` — available levels depend on the model |
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
| `$name` | Named argument declared in the `arguments` frontmatter list (names map to positions in order) |
| `${CLAUDE_SESSION_ID}` | Current session ID — useful for session-specific temp files |
| `${CLAUDE_EFFORT}` | Current effort level (`low`–`max`) — adapt instructions to the active effort setting |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md — use to reference bundled scripts/data regardless of CWD |
| `${CLAUDE_PROJECT_DIR}` | Project root directory (same path hooks receive) — reference project-local scripts independent of install location |

Plugin skills also have access to (defined in the official plugins reference):

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
- Keep identical to the containing directory name (the directory name is what users type after `/`)
- Avoid: `helper`, `utils`, reserved words (`anthropic`, `claude`)

## Description Formula

```
[What it does]. [Key capabilities]. Use when [specific triggers].
```

Both parts are required: the capability statement lets Claude pick the right skill among 100+ candidates; the "Use when..." clause supplies the triggers.
Do NOT enumerate internal workflow steps — state capability, not procedure.

**Always write in third person** (description is injected into system prompt).

**Good**:
```yaml
description: Creates semantic git commits. Analyzes staged changes and generates conventional commit messages. Use when committing code or managing git history.
```

**Bad**:
```yaml
description: Use when committing code.              # triggers-only, no capability statement
description: I can help you with git stuff.         # first person
description: First stages files, then writes the message, then commits.  # enumerates workflow steps
```

## Body Guidelines

- Use imperative form ("Run the script" not "You should run")
- SKILL.md is overview; move detailed content to `references/` (loaded on-demand)
- Keep body < 300 lines (house rule; official recommendation is < 500). Once loaded, the body stays resident in context for the rest of the session — every line is a recurring token cost. Body length does NOT affect activation; activation depends only on `name` + `description`
- No "When to use" sections (put in description)
- Include workflow checklists for complex tasks

## Shared Conventions

If a convention appears in multiple skills, extract to `.claude/rules/`:

- Use `writing-rules` skill to create shared convention
- Skills automatically inherit rules (auto-injected)
- Keep only skill-specific details in SKILL.md

**Rule of thumb**: Rules = conventions shared across skills.
