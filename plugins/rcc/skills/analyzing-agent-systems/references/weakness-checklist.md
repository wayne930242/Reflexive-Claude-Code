# Agent System Weakness Checklist

## How to Use

For each category, check every item. Mark severity:
- **CRITICAL** — Must fix before system is usable
- **WARNING** — Should fix, causes degraded experience
- **INFO** — Nice to fix, minor improvement

---

## 1. Routing / Trigger Weaknesses

- [ ] Skill description is vague or generic (e.g., "improve code")
- [ ] Description summarizes workflow instead of stating triggers
- [ ] Description lacks concrete "Use when..." phrases with user-said examples
- [ ] Two or more skills have overlapping trigger conditions
- [ ] No fallback when no skill matches user request
- [ ] More than 20 skills loaded (route saturation risk)
- [ ] Skill triggers use jargon users wouldn't naturally say
- [ ] Infinite handoff loop possible between skills
- [ ] Skill has no declared routing pattern (Tree/Chain/Node/Skill Steps) in Routing section
- [ ] Chain skill missing handoff to next skill
- [ ] Tree skill flowchart missing decision point (diamond node)
- [ ] Node skill not using `context: fork` when analysis-only
- [ ] Skill Steps skill missing internal verification gates between tasks
- [ ] Handoff uses auto-invoke where user confirmation is needed (state-changing chains)
- [ ] Entry-point skill missing Skill Chain Reference table

## 2. Context Management

- [ ] Reviewer/analyzer subagents lack `context: fork` isolation
- [ ] CLAUDE.md exceeds 200 lines
- [ ] Skill SKILL.md exceeds 300 lines or ~2,000 tokens (activation quality degrades beyond this)
- [ ] Reference files loaded eagerly instead of on-demand via reference links
- [ ] Skill embeds large content inline instead of using `!command` for dynamic context injection
- [ ] Subagent receives full parent conversation (context pollution)
- [ ] Handoff between skills loses intent or context
- [ ] Rule files exceed 50 lines
- [ ] No compaction strategy — long conversations degrade without summarization checkpoints

## 3. Workflow Continuity

- [ ] Skill chain has a broken link (step N doesn't connect to N+1)
- [ ] Missing verification gate between tasks
- [ ] No error recovery path when a step fails
- [ ] Workflow exceeds 8 reasoning steps without checkpoint
- [ ] Re-running a skill produces side effects (not idempotent)
- [ ] Task list doesn't enforce sequential completion

## 4. Redundancy / Conflicts

- [ ] Two skills serve the same purpose
- [ ] Same convention appears in both CLAUDE.md and a rule file
- [ ] Same constraint appears in 2+ skills
- [ ] Rule contradicts CLAUDE.md instruction
- [ ] Hook enforces something already in a rule (duplicate layers)
- [ ] Personal and project settings conflict without clear precedence

## 5. Security / Safety

- [ ] No hook protecting sensitive files (.env, credentials, SSH keys)
- [ ] Subagent has write access it doesn't need
- [ ] Subagent used to write to `.claude/` directory (will be blocked)
- [ ] No input validation hook (UserPromptSubmit)
- [ ] Hook timeout too generous (>30 seconds)
- [ ] No file path filtering in hooks (checks all files, not just relevant ones)
- [ ] Skill with side effects (deploy, commit, delete) missing `disable-model-invocation: true`
- [ ] Skill missing `allowed-tools` restriction when it should be read-only or limited

## 6. Observability

- [ ] No structured output from skill invocations
- [ ] Routing decisions are opaque (can't tell why a skill was chosen)
- [ ] No report or summary produced after multi-step workflow
- [ ] Failed skill invocation produces no diagnostic output

## 7. Architecture / Scaling

- [ ] Flat topology — all skills at same level, no grouping
- [ ] Error in one skill cascades to downstream skills without cancellation
- [ ] Coordination overhead exceeds task complexity (over-orchestrated)
- [ ] Skills designed for hypothetical future requirements (YAGNI violation)

## 8. Constitution Stability

- [ ] CLAUDE.md uses custom XML tags instead of standard markdown
- [ ] Instructions are vague ("write clean code") instead of specific and verifiable
- [ ] No mechanism to detect instruction drift in long conversations
- [ ] CLAUDE.md contains domain knowledge that belongs in skills
- [ ] CLAUDE.md contains conventions that belong in rules
- [ ] CLAUDE.md contains procedures that belongs in skills

## 9. Project Context Completeness

- [ ] No account names or org identifiers documented (e.g., npm org, Expo account, cloud project)
- [ ] No directory convention documented (where plugins, scripts, configs go)
- [ ] No deployment target documented (servers, environments, deploy commands)
- [ ] Languages used in project have no matching PostToolUse hooks (e.g., Go without `go build`, TS without `tsc --noEmit`)
- [ ] Languages used in project have no matching rules in `.claude/rules/`
- [ ] User-root rules exist at `~/.claude/rules/` but project has no project-level specialization
- [ ] No `settings.local.json` for sensitive project-specific data (accounts, IPs, tokens)
- [ ] Project uses deployment tooling (rsync, Ansible, Docker) but has no deploy safety rules

## 10. Cross-Tool Migration

- [ ] Other AI tool configs exist (`.cursorrules`, `.github/copilot-instructions.md`, `.windsurfrules`) but not integrated into agent system
- [ ] Existing AI configs contain conventions/rules not reflected in CLAUDE.md or `.claude/rules/`
- [ ] Project has `.editorconfig` or linter configs with rules that should be mirrored in agent rules

## 11. Rules Health

- [ ] Individual rule file > 50 lines (token cost scales with matches)
- [ ] Rule has no `paths:` but content clearly targets specific file types or directories
- [ ] Rule content overlaps with another rule (partial or full duplication)
- [ ] Rule duplicates instructions already in CLAUDE.md
- [ ] Path-scoped rule glob matches zero files in the project (dead glob)
- [ ] CLAUDE.md + global rules (no `paths:`) total exceeds 300 lines (session-start context overload)
- [ ] CLAUDE.md single file exceeds 200 lines (official recommended limit)
- [ ] Rule or CLAUDE.md contains multi-step procedures (should be a skill, not a directive)
- [ ] Rule or CLAUDE.md contains code blocks used as process instructions (should be flowchart or skill)
