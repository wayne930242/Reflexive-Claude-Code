# Agent Model Selection — Three-Layer Architecture

| Layer | Model | Role | Tool Constraint |
|-------|-------|------|-----------------|
| Orchestration | `haiku` | Dispatch, task decomposition, routing | **Must have tools** (TaskCreate, Agent) |
| Implementation | `sonnet` | Write, analyze, modify | Full tools |
| Quality gate / Advisor | `opus` | Architectural reasoning, pass/fail judgment, design advice | Read-only (`Read, Grep, Glob`) |

**Opus** only has engineering value when its output is mechanically executable by downstream Sonnet AND a revision loop exists. No loop → Opus = expensive logger.

**Haiku** as orchestrator must have tools. Zero-tool Haiku only works for pre-injected content — not for judgment tasks.

**Use `inherit`** when the agent does not need specific model capabilities; let the parent decide.
