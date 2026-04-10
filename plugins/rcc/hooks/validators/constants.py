"""Constants and enums for Claude Code configuration validation."""

# Skill frontmatter allowed fields
SKILL_ALLOWED_FIELDS = {
    "name", "description", "argument-hint", "disable-model-invocation",
    "user-invocable", "allowed-tools", "model", "effort", "context",
    "agent", "hooks", "paths", "shell",
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
    "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "SessionStart",
    "SessionEnd", "UserPromptSubmit", "PreCompact", "Notification"
}
HOOK_TYPES = {"prompt", "command"}

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

# Agent configuration enums
VALID_MODELS = {"inherit", "sonnet", "opus", "haiku"}
VALID_EFFORT_LEVELS = {"low", "medium", "high", "max"}
VALID_PERMISSION_MODES = {"default", "acceptEdits", "auto", "dontAsk", "bypassPermissions", "plan"}
VALID_MEMORY_SCOPES = {"user", "project", "local"}
VALID_ISOLATION_MODES = {"worktree"}
VALID_COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
BUILTIN_SUBAGENT_TYPES = {"Explore", "Plan", "general-purpose"}