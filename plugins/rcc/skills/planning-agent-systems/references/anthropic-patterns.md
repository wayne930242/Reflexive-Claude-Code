# Anthropic Workflow Patterns

## Six Production Patterns

Map each workflow from the summary to one of these patterns:

| Pattern | When to Use | Example |
|---------|------------|---------|
| **Prompt Chaining** | Clear sequential steps, each transforms previous output | lint → test → deploy |
| **Routing** | Input classification determines handler | detect language → route to lang-specific rules |
| **Parallelization** | Independent tasks that can run concurrently | parallel code review + test run |
| **Orchestrator-Workers** | Central coordinator dynamically delegates subtasks | refactor planner spawning file-specific agents |
| **Evaluator-Optimizer** | Generate-then-critique loop | write skill → review skill → revise |
| **Autonomous Agent** | Open-ended, LLM decides next step | debugging with tool access |

## Flowchart Conventions

When drawing the architecture flowchart, use these DOT conventions:
- **Entry points** (doublecircle) — how the user triggers each workflow
- **Decision nodes** (diamond) — routing/classification points
- **Process nodes** (box) — skills, hooks, rules that execute
- **Data flow edges** — what artifact passes between nodes
- **Parallel lanes** — workflows that can run concurrently (use subgraph clusters)

```dot
// Example structure — adapt to actual workflows
digraph agent_architecture {
    rankdir=TB;

    // Entry points
    user_trigger [label="User\ntrigger", shape=doublecircle];

    // Routing
    classify [label="Classify\nintent", shape=diamond];

    // Workflow A (chain)
    subgraph cluster_workflow_a {
        label="Workflow A (Prompt Chaining)";
        a1 [label="Step 1\n[skill]", shape=box];
        a2 [label="Step 2\n[hook]", shape=box];
    }

    // Workflow B (parallel)
    subgraph cluster_workflow_b {
        label="Workflow B (Parallelization)";
        b1 [label="Task 1\n[skill]", shape=box];
        b2 [label="Task 2\n[skill]", shape=box];
    }

    user_trigger -> classify;
    classify -> a1 [label="type A"];
    classify -> b1 [label="type B"];
    classify -> b2 [label="type B"];
    a1 -> a2 [label="artifact.md"];
}
```

## Dependency Graph Template

From the flowchart, extract a dependency table:

| Component | Depends On | Depended By | Phase |
|-----------|-----------|-------------|-------|
| CLAUDE.md | (none) | all rules, skills | 1 |
| Rule: X | CLAUDE.md | Hook: Y | 1 |
| Hook: Y | Rule: X | (none) | 2 |
| Skill: Z | Rule: X | (none) | 2 |

Phase assignment rules:
- Phase 1: Components with no dependencies (foundation)
- Phase 2: Components depending only on Phase 1
- Phase 3+: Components depending on Phase 2+
- Within same phase: can be built in parallel
