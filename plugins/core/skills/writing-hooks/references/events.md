# Hook Events Reference

Complete guide to hook events and their input/output formats.

## Event Overview

| Event | Timing | Primary Use | Can Block |
|-------|--------|-------------|-----------|
| `PreToolUse` | Before tool executes | Validate/block operations | Yes |
| `PostToolUse` | After tool completes | Format/lint/validate output | Yes |
| `UserPromptSubmit` | User sends prompt | Add context/validate input | Yes |
| `PermissionRequest` | Permission needed | Auto-approve/deny | Yes |
| `Stop` | Claude finishes | Continue/stop agent | Yes |
| `SessionStart` | Session begins | Load context/env | Yes |
| `SessionEnd` | Session ends | Cleanup/logging | No |
| `Notification` | Notification sent | Custom alerts | No |
| `PreCompact` | Before compacting | Prevent/modify | No |

## Input Format (JSON via stdin)

### Common Fields (All Events)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/session.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

### PreToolUse / PostToolUse

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_use_id": "toolu_01ABC...",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "..."
  }
}
```

**Common Tool Inputs:**

| Tool | Input Fields |
|------|--------------|
| `Write` | `file_path`, `content` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Read` | `file_path`, `offset`, `limit` |
| `Bash` | `command`, `description`, `timeout` |
| `Glob` | `pattern`, `path` |
| `Grep` | `pattern`, `path`, `glob` |

### PostToolUse Additional Fields

```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Bash",
  "tool_result": {
    "stdout": "...",
    "stderr": "...",
    "exitCode": 0
  }
}
```

### UserPromptSubmit

```json
{
  "hook_event_name": "UserPromptSubmit",
  "prompt": "User's message here"
}
```

### PermissionRequest

```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test"
  },
  "permission_type": "dangerous_command"
}
```

## Output Format

### Exit Codes

| Code | Effect |
|------|--------|
| 0 | Success - continue execution |
| 2 | Block - prevent action, stderr fed to Claude |
| Other | Warning - continue, stderr shown in verbose |

### JSON Output (Advanced)

Return JSON in stdout for sophisticated control:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  },
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Optional feedback"
}
```

**Permission Decisions (PreToolUse):**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved by hook"
  }
}
```

Values: `"allow"`, `"deny"`, `"ask"`

## Matchers

### Pattern Syntax

| Pattern | Matches |
|---------|---------|
| `Write` | Exact match |
| `Write\|Edit` | Either tool |
| `Bash` | Bash commands |
| `Notebook.*` | Regex pattern |
| `*` | All tools |
| `mcp__.*` | All MCP tools |

### Common Matchers for Static Checks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": "..."}]
      }
    ]
  }
}
```

## Event-Specific Examples

### PreToolUse: Block Dangerous Patterns

```python
#!/usr/bin/env python3
import json, sys, re

data = json.load(sys.stdin)
tool = data.get("tool_name")
input_data = data.get("tool_input", {})

if tool == "Bash":
    cmd = input_data.get("command", "")
    dangerous = [r"rm\s+-rf\s+/", r"chmod\s+777", r"curl.*\|.*bash"]
    for pattern in dangerous:
        if re.search(pattern, cmd):
            print(f"Blocked dangerous: {pattern}", file=sys.stderr)
            sys.exit(2)

sys.exit(0)
```

### PostToolUse: Auto-format

```python
#!/usr/bin/env python3
import json, subprocess, sys

data = json.load(sys.stdin)
file_path = data.get("tool_input", {}).get("file_path", "")

if file_path.endswith((".js", ".ts")):
    subprocess.run(["npx", "prettier", "--write", file_path])
    print(f"Formatted: {file_path}")

sys.exit(0)
```

### UserPromptSubmit: Add Context

```python
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
prompt = data.get("prompt", "")

# Add git status context for code questions
if any(word in prompt.lower() for word in ["code", "fix", "refactor"]):
    import subprocess
    status = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True, text=True
    )
    print(f"Git status:\n{status.stdout}")

sys.exit(0)
```

### PermissionRequest: Auto-approve Safe

```python
#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
tool = data.get("tool_name")
input_data = data.get("tool_input", {})

# Auto-approve read-only commands
if tool == "Bash":
    cmd = input_data.get("command", "")
    safe_prefixes = ["ls", "cat", "grep", "find", "git status", "git log"]
    if any(cmd.strip().startswith(p) for p in safe_prefixes):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Read-only command"
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)  # Fall through to normal permission flow
```

## Environment Variables

Available in hook scripts:

| Variable | Description |
|----------|-------------|
| `CLAUDE_PROJECT_DIR` | Project root directory |
| `USER` | Current user |
| `HOME` | User home directory |
| `PATH` | System PATH |

## Debugging Hooks

### Test Hook Manually

```bash
echo '{"tool_name": "Write", "tool_input": {"file_path": "test.ts"}}' | \
  python3 .claude/hooks/lint.py
echo $?  # Check exit code
```

### Enable Verbose Mode

```bash
claude --verbose
```

Shows all hook stdout/stderr output.

### Common Issues

1. **Hook not running**: Check `settings.json` path and matcher
2. **Exit code ignored**: Ensure using `sys.exit(2)` to block
3. **Timeout**: Default 60s, adjust with `"timeout": N` in config
4. **Permission denied**: Run `chmod +x` on hook scripts
