# Plugin Health Checklist

## How to Use

For each category, check every item. Mark severity:
- **CRITICAL** — Must fix, plugin will not work correctly
- **WARNING** — Should fix, degrades quality or discoverability
- **INFO** — Nice to fix, minor improvement

---

## 1. Manifest Integrity

- [ ] `.claude-plugin/plugin.json` exists
- [ ] Valid JSON syntax (no trailing commas, correct quoting)
- [ ] `name` field present and kebab-case (`[a-z0-9-]+`)
- [ ] `name` avoids reserved words (`helper`, `utils`, `anthropic`, `claude`)
- [ ] `description` field present and descriptive
- [ ] `version` field follows semver (`MAJOR.MINOR.PATCH`)
- [ ] `author` field present with at least `name`
- [ ] `license` field present
- [ ] `keywords` array present for discoverability

## 2. Directory Structure

- [ ] Components (`skills/`, `commands/`, `agents/`) at plugin root, NOT inside `.claude-plugin/`
- [ ] No stale or orphaned directories
- [ ] No duplicate component names across directories
- [ ] `README.md` exists at plugin root
- [ ] No absolute paths in any configuration (use `${CLAUDE_PLUGIN_ROOT}`)
- [ ] No `../` path traversal in references

## 3. Skills Quality

- [ ] Every skill directory has `SKILL.md`
- [ ] Skill names use gerund form (verb+-ing)
- [ ] Frontmatter has `name` and `description`
- [ ] Description includes "Use when..." triggers
- [ ] Description is third person, not workflow summary
- [ ] SKILL.md under 300 lines (use `references/` for details)
- [ ] Has Task Initialization section with TaskCreate
- [ ] Has Red Flags section
- [ ] Has Common Rationalizations table
- [ ] Has Flowchart section (Graphviz DOT)
- [ ] No overlapping triggers between skills

## 4. Commands Quality

- [ ] Command files have YAML frontmatter with `description`
- [ ] Command invokes a skill (not inline logic)
- [ ] Command name matches the skill it invokes
- [ ] No orphan commands (pointing to non-existent skills)

## 5. Agents Quality

- [ ] Agent files have complete frontmatter (`name`, `description`, `model`, `context`, `tools`)
- [ ] Agents use `context: fork` for isolation
- [ ] Tools list follows principle of least privilege
- [ ] No agents with write access they don't need
- [ ] Agent descriptions start with "Use this agent..."
- [ ] No overlapping responsibilities between agents

## 6. Version Sync

- [ ] `plugin.json` version matches `marketplace.json` plugin entry
- [ ] `marketplace.json` metadata.version matches plugin versions
- [ ] README version badges/headers match actual version
- [ ] No version drift between localized READMEs

## 7. Hook Safety (if applicable)

- [ ] Hook scripts are executable (`chmod +x`)
- [ ] Hook timeouts are reasonable (< 30 seconds)
- [ ] Hooks use file path filtering (not checking all files)
- [ ] Hook exit codes are correct (0 = pass, non-zero = block)
- [ ] No hooks that silently modify files without user awareness

## 8. Distribution Readiness

- [ ] No hardcoded local paths
- [ ] No environment-specific assumptions
- [ ] `${CLAUDE_PLUGIN_ROOT}` used for self-references (not persistent data)
- [ ] `${CLAUDE_PLUGIN_DATA}` used for persistent data (not `${CLAUDE_PLUGIN_ROOT}`)
- [ ] No secrets or credentials in plugin files
- [ ] Plugin works after fresh install (no implicit dependencies)

## 9. Skill Variables & Shell Context

- [ ] Skills that reference bundled files use `${CLAUDE_SKILL_DIR}` (not relative `./` or hardcoded paths)
- [ ] Skills that need session-unique temp files use `${CLAUDE_SESSION_ID}` in the filename
- [ ] Skills accepting arguments document `$ARGUMENTS` usage and set `argument-hint` in frontmatter
- [ ] Skills using `!` shell commands have fallbacks for missing tools (e.g., `!`cmd 2>/dev/null || echo "not available"`)
- [ ] Skills needing PowerShell set `shell: powershell` in frontmatter and document `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` requirement
- [ ] No `!` commands that assume a specific CWD — use `${CLAUDE_SKILL_DIR}` for plugin-relative paths
- [ ] Skills using `context: fork` design `argument-hint` to carry sufficient context (forked context loses parent conversation)

---

## Cross-Component Checks

| Check | Components | Severity |
|-------|-----------|----------|
| Skill triggers don't overlap | All skills | WARNING |
| Commands map to existing skills | Commands → Skills | CRITICAL |
| Agent tool lists are minimal | All agents | WARNING |
| Version numbers are synchronized | plugin.json, marketplace.json, READMEs | CRITICAL |
| No duplicate logic across skills | All skills | WARNING |
| README documents all components | README vs actual | WARNING |
| Skills use `${CLAUDE_SKILL_DIR}` not `${CLAUDE_PLUGIN_ROOT}` for own files | All skills | WARNING |
| `!` commands work cross-platform or `shell` is set | All skills with shell context | INFO |
