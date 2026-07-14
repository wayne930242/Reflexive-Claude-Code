# Stop Event Self-Verify (Ralph Wiggum / L-Thread)

When the agent tries to end its turn, block until deterministic checks pass — turning a one-shot agent into a loop that won't quit until the work is actually done.

**Use when:** long-running tasks, refactors, migrations, anything where "I think I'm done" is unreliable.

## Hook script

```python
# .claude/hooks/stop_verify.py
import json, subprocess, sys

data = json.load(sys.stdin)
# Avoid infinite loop: respect stop_hook_active to bail after one retry
if data.get("stop_hook_active"):
    sys.exit(0)

result = subprocess.run(["pytest", "-x", "--tb=short"], capture_output=True, text=True)
if result.returncode != 0:
    print(result.stdout[-2000:], file=sys.stderr)
    sys.exit(2)  # Block stop, feed stderr to Claude
sys.exit(0)
```

## settings.json registration

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/stop_verify.py",
        "timeout": 120
      }]
    }]
  }
}
```

**Critical:** always check `stop_hook_active` to bail after one retry — otherwise the agent loops forever on unfixable failures.
