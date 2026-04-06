# Anthropic Workflow Patterns

## Six Production Patterns

Use these to classify workflows during exploration. Match user answers to patterns:

| Pattern | Signal from User Answers |
|---------|------------------------|
| **Prompt Chaining** | "First I do X, then Y, then Z" — clear sequential steps |
| **Routing** | "It depends on whether..." — input classification needed |
| **Parallelization** | "I run these at the same time" or independent tasks |
| **Orchestrator-Workers** | "I plan first, then delegate parts" — dynamic subtask creation |
| **Evaluator-Optimizer** | "I review and revise until..." — generate-critique loops |
| **Autonomous Agent** | "I figure it out as I go" — open-ended exploration |

## Complexity Ladder

Prefer the lowest level that works:

| Level | Component | Overhead |
|-------|-----------|----------|
| 1 | CLAUDE.md instruction | Zero |
| 2 | Rule file with path glob | Scoped convention |
| 3 | Hook | Automated enforcement |
| 4 | Single skill | Repeatable workflow |
| 5 | Skill chain | Multi-step workflow |
| 6 | Multi-agent with subagents | Parallel/isolated work |
