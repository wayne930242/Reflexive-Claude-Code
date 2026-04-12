# Targeted Exploration Questions

Question bank for exploring user workflows, organized by four exploration areas.
Ask one question at a time. Adapt follow-ups based on answers. Total 5-8 questions across all areas.

## 1. Pipeline Mode Exploration

**Goal:** Determine how workflows connect and what state management they need.

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| "How does this workflow usually start? Fixed entry point or situational?" | Startup mode | owner-pipe (fixed entry) vs chain-pipe (variable entry) |
| "If it breaks midway, how do you resume? Restart from scratch or pick up where you left off?" | State persistence needs | stateless pipe vs state persistence |
| "How many files does each step touch? Across how many modules?" | Work scope | simple skill (small scope) vs script-managed state (large scope) |
| "Do these steps have to run in order, or can some run in parallel?" | Pipeline topology | sequential pipeline vs parallel dispatch |
| "Who decides what to do next?" | Control ownership | owner-pipe (human decides) vs chain-pipe (auto-handoff) |
| "How many steps in this workflow? Who is responsible for each?" | Step count and responsibility | many steps → chain-pipe; few steps → owner-pipe |

**Selection strategy:** Ask startup mode first, then decide whether to ask about state and scope based on the answer.
If the first two questions are enough to determine pipeline mode, skip the rest.

## 2. Pain Point Discovery

**Goal:** Find where the current agent system fails or frustrates the user.

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| "When was the last time the agent felt unhelpful? What happened?" | Missing capability or broken chain | missing skill or rule |
| "Is there anything you think should be handled automatically but isn't?" | Automation gap | missing hook or skill |
| "Which mistakes have you been warned about more than twice?" | Repeated violations | rule or hook enforcement |
| "Has Claude ever responded in a way that felt wrong?" | Behavioral drift | rule or CLAUDE.md adjustment |
| "When does Claude feel too verbose or too terse?" | Communication style issues | communication rule |
| "Are there instructions you have to repeat every time?" | Instruction amnesia | CLAUDE.md or rule file |
| "Has the agent ever done something that took you time to fix?" | Out-of-control behavior | guardrail (rule or hook) |

**Selection strategy:** Ask about past failures first (first two questions), then decide whether to dig into communication style or behavioral issues.
If the user has no negative experiences, move on quickly.

## 3. Routine Task & Small Work Identification

**Goal:** Find repetitive tasks that could be automated.

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| "Is there anything you do every day that feels tedious?" | Automation candidate | agent or skill |
| "When searching code, do you have fixed patterns or things you frequently look for?" | Fixed search patterns | agent with specific search patterns |
| "Are there formatting or validation tasks that could be automated?" | Format/quality checks | PostToolUse hook |
| "Do you have a fixed set of steps when opening a new PR or branch?" | Process rituals | skill or hook |
| "Are there command combinations you wish could be done in one step?" | Command composition | command alias or skill |
| "Do you have regular reports or summaries to produce?" | Periodic tasks | scheduled agent or skill |
| "Is there work you think the agent can do faster than you?" | Delegation candidate | agent or skill |

**Selection strategy:** Ask about tedious tasks first, then supplement based on role.
For developers, ask more about search and formatting. For PMs, ask more about reports and processes.

## 4. Human-in-the-Loop Discovery

**Goal:** Find critical points in workflows where humans must review, approve, or intervene. Ensures agent system design includes appropriate confirmation gates and guardrails.

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| "Which steps do you absolutely need to review before moving on?" | Nodes requiring review checkpoints | skill with `user-confirmation` handoff |
| "Are there any operations that are hard to undo if done wrong?" | Destructive operations needing confirmation gates | hook (PreToolUse blocking) or skill confirmation gate |
| "In what situations do you want the agent to stop and ask you?" | User's trust boundary | guardrail rule or hook |
| "Are there steps that involve external people? Like sending emails, pushing code, deploying?" | External visibility boundary | skill confirmation gate |
| "What can the agent fully automate vs. what should it never do alone?" | Autonomy scope | automation vs confirmation boundary |
| "Are there processes that require multiple people to confirm?" | Multi-person approval needs | chain with user-confirmation handoff |

**Selection strategy:** Ask "hard to undo if done wrong" first, then decide whether to dig into external visibility and multi-person approval.
If the workflow is purely local development (no deploys, no external communication), shorten to 2-3 questions.

## General Guidelines

- Ask one question at a time
- Skip questions already answered by the analysis report
- Adapt follow-up questions based on answers — don't ask mechanically from the table
- Maximum 5-8 questions total (across all four areas)
- Prefer multiple-choice framing where possible
- Ask about failures before wishes
