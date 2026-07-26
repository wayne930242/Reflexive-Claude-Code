"""Constants and enums for Claude Code configuration validation."""

# Skill frontmatter allowed fields.
# Source: https://code.claude.com/docs/en/skills.md — "Frontmatter reference" table.
# Keep in sync with that table; a missing entry makes the hook warn on valid skills.
SKILL_ALLOWED_FIELDS = {
    "name", "description", "when_to_use", "argument-hint", "arguments",
    "disable-model-invocation", "user-invocable", "allowed-tools",
    "disallowed-tools", "model", "effort", "context", "agent", "background",
    "hooks", "paths", "shell",
}

# Agent frontmatter allowed fields
AGENT_ALLOWED_FIELDS = {
    "name", "description", "model", "tools",
    "disallowedTools", "permissionMode", "maxTurns", "skills",
    "mcpServers", "hooks", "memory", "background", "effort",
    "isolation", "color", "initialPrompt",
}

# Rules frontmatter allowed fields
RULES_ALLOWED_FIELDS = {"paths"}

# Hook-only variables
HOOKS_ONLY_VARS = {"${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_PLUGIN_DATA}"}

# Hook configuration validation
HOOK_EVENTS = {
    # Session lifecycle
    "SessionStart", "SessionEnd",
    # Per-turn
    "UserPromptSubmit", "Stop", "StopFailure",
    # Tool execution
    "PreToolUse", "PostToolUse", "PostToolUseFailure",
    "PermissionRequest", "PermissionDenied",
    # Subagent
    "SubagentStart", "SubagentStop", "TeammateIdle",
    # Task
    "TaskCreated", "TaskCompleted",
    # Context
    "ConfigChange", "CwdChanged", "FileChanged", "InstructionsLoaded",
    # Compact
    "PreCompact", "PostCompact",
    # MCP
    "Elicitation", "ElicitationResult",
    # Notification
    "Notification",
    # Worktree
    "WorktreeCreate", "WorktreeRemove",
}
HOOK_TYPES = {"command", "http", "prompt", "agent"}

# Plugin hooks.json allowed top-level fields
PLUGIN_HOOKS_ALLOWED_FIELDS = {"description", "hooks"}

# Complete Claude Code tool list based on official documentation
CLAUDE_CODE_TOOLS = {
    "Agent", "AskUserQuestion", "Bash", "CronCreate", "CronDelete", "CronList",
    "Edit", "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree",
    "Glob", "Grep", "ListMcpResourcesTool", "LSP", "Monitor", "NotebookEdit",
    "PowerShell", "Read", "ReadMcpResourceTool", "SendMessage", "Skill",
    "TaskCreate", "TaskGet", "TaskList", "TaskOutput", "TaskStop", "TaskUpdate",
    "TeamCreate", "TeamDelete", "TodoWrite", "ToolSearch", "WebFetch", "WebSearch", "Write"
}

# Agent configuration enums.
# Source: https://code.claude.com/docs/en/sub-agents.md — frontmatter reference table.
VALID_MODELS = {"inherit", "sonnet", "opus", "haiku", "fable"}
# The model field also accepts a full model ID, e.g. "claude-opus-5". Aliases alone
# cannot cover those, so callers match this pattern before reporting an invalid model.
FULL_MODEL_ID_PATTERN = r"^claude-[a-z0-9.\[\]-]+$"
VALID_EFFORT_LEVELS = {"low", "medium", "high", "xhigh", "max"}
# "manual" is an alias for "default", available since Claude Code v2.1.200.
VALID_PERMISSION_MODES = {
    "default", "manual", "acceptEdits", "auto", "dontAsk", "bypassPermissions", "plan",
}
VALID_MEMORY_SCOPES = {"user", "project", "local"}
VALID_ISOLATION_MODES = {"worktree"}
VALID_COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
BUILTIN_SUBAGENT_TYPES = {"Explore", "Plan", "general-purpose"}