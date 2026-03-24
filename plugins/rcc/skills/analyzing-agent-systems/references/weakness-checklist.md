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
- [ ] Two or more skills have overlapping trigger conditions
- [ ] No fallback when no skill matches user request
- [ ] More than 20 skills loaded (route saturation risk)
- [ ] Skill triggers use jargon users wouldn't naturally say
- [ ] Infinite handoff loop possible between skills

## 2. Context Management

- [ ] Reviewer/analyzer subagents lack `context: fork` isolation
- [ ] CLAUDE.md exceeds 200 lines
- [ ] Skill SKILL.md exceeds 300 lines
- [ ] Reference files loaded eagerly instead of on-demand
- [ ] Subagent receives full parent conversation (context pollution)
- [ ] Handoff between skills loses intent or context
- [ ] Rule files exceed 50 lines

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
