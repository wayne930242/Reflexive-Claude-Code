# Task Initialization Protocol

When a skill declares a **Tasks** list, create the task list BEFORE any other action:

```
TaskCreate for EACH task in the skill's Tasks list:
- Subject: "[<skill-name>] Task N: <action>"
- ActiveForm: "<doing action>"
```

**Execution rules:**

1. `TaskUpdate status="in_progress"` BEFORE starting each task
2. `TaskUpdate status="completed"` ONLY after the task's verification passes
3. If a task fails → stay in_progress, diagnose, retry
4. NEVER skip to the next task until the current one is completed
5. At the end, `TaskList` to confirm all tasks completed
