# Static Checks Reference

Complete hook examples for common static analysis scenarios.

## JavaScript/TypeScript Ecosystem

### ESLint with Auto-fix

```python
#!/usr/bin/env python3
"""ESLint hook with auto-fix capability."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    ext = Path(file_path).suffix.lower()
    if ext not in (".js", ".jsx", ".ts", ".tsx", ".mjs"):
        sys.exit(0)

    # First, try to auto-fix
    subprocess.run(
        ["npx", "eslint", "--fix", file_path],
        capture_output=True,
    )

    # Then check for remaining errors
    result = subprocess.run(
        ["npx", "eslint", "--format", "stylish", "--max-warnings", "0", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Unfixable ESLint errors:", file=sys.stderr)
        print(result.stdout[:500], file=sys.stderr)
        sys.exit(2)

    print(f"ESLint passed: {file_path}")

if __name__ == "__main__":
    main()
```

### Prettier + ESLint Combined

```python
#!/usr/bin/env python3
"""Combined Prettier and ESLint check."""

import json
import subprocess
import sys
from pathlib import Path

EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".json", ".md"}

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path or Path(file_path).suffix.lower() not in EXTENSIONS:
        sys.exit(0)

    # Auto-format with Prettier
    subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True)

    # Run ESLint for JS/TS files
    if Path(file_path).suffix.lower() in {".js", ".jsx", ".ts", ".tsx"}:
        result = subprocess.run(
            ["npx", "eslint", "--fix", "--max-warnings", "0", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout[:500], file=sys.stderr)
            sys.exit(2)

    print(f"Formatted and linted: {file_path}")

if __name__ == "__main__":
    main()
```

### TypeScript Strict Check

```python
#!/usr/bin/env python3
"""TypeScript strict type checking hook."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path or Path(file_path).suffix.lower() not in (".ts", ".tsx"):
        sys.exit(0)

    # Run tsc with strict settings
    result = subprocess.run(
        [
            "npx", "tsc",
            "--noEmit",
            "--strict",
            "--skipLibCheck",
            "--pretty", "false",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        # Filter for current file only
        file_name = Path(file_path).name
        errors = [
            line for line in result.stdout.split("\n")
            if file_name in line
        ]

        if errors:
            print("TypeScript errors:", file=sys.stderr)
            print("\n".join(errors[:10]), file=sys.stderr)
            sys.exit(2)

if __name__ == "__main__":
    main()
```

## Python Ecosystem

### Ruff (Fast Python Linter)

```python
#!/usr/bin/env python3
"""Ruff linting and formatting hook."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path or not file_path.endswith(".py"):
        sys.exit(0)

    # Auto-format
    subprocess.run(["ruff", "format", file_path], capture_output=True)

    # Auto-fix safe issues
    subprocess.run(["ruff", "check", "--fix", file_path], capture_output=True)

    # Check for remaining issues
    result = subprocess.run(
        ["ruff", "check", "--output-format", "concise", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Ruff errors:", file=sys.stderr)
        print(result.stdout[:500], file=sys.stderr)
        sys.exit(2)

    print(f"Ruff passed: {file_path}")

if __name__ == "__main__":
    main()
```

### MyPy Type Checking

```python
#!/usr/bin/env python3
"""MyPy strict type checking hook."""

import json
import subprocess
import sys

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path or not file_path.endswith(".py"):
        sys.exit(0)

    result = subprocess.run(
        [
            "mypy",
            "--strict",
            "--no-error-summary",
            "--show-column-numbers",
            file_path,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        errors = result.stdout.strip().split("\n")[:10]
        print("Type errors:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

### Python Security Check (Bandit)

```python
#!/usr/bin/env python3
"""Bandit security check hook."""

import json
import subprocess
import sys

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path or not file_path.endswith(".py"):
        sys.exit(0)

    result = subprocess.run(
        ["bandit", "-f", "txt", "-ll", file_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 and "No issues identified" not in result.stdout:
        print("Security issues found:", file=sys.stderr)
        print(result.stdout[:500], file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

## Multi-Language Hooks

### Universal Formatter

```python
#!/usr/bin/env python3
"""Universal auto-formatter for multiple languages."""

import json
import subprocess
import sys
from pathlib import Path

FORMATTERS = {
    ".py": ["ruff", "format"],
    ".js": ["npx", "prettier", "--write"],
    ".jsx": ["npx", "prettier", "--write"],
    ".ts": ["npx", "prettier", "--write"],
    ".tsx": ["npx", "prettier", "--write"],
    ".json": ["npx", "prettier", "--write"],
    ".md": ["npx", "prettier", "--write"],
    ".yaml": ["npx", "prettier", "--write"],
    ".yml": ["npx", "prettier", "--write"],
    ".go": ["gofmt", "-w"],
    ".rs": ["rustfmt"],
}

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    ext = Path(file_path).suffix.lower()
    formatter = FORMATTERS.get(ext)

    if formatter:
        cmd = formatter + [file_path]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            print(f"Formatted: {file_path}")

if __name__ == "__main__":
    main()
```

### Protected Files Check

```python
#!/usr/bin/env python3
"""Prevent modification of protected files."""

import json
import sys
from pathlib import Path

PROTECTED = [
    ".env",
    ".env.local",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    ".git/",
    "node_modules/",
    "__pycache__/",
]

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    path = Path(file_path)

    for protected in PROTECTED:
        if protected in str(path) or path.name == protected.rstrip("/"):
            print(f"Cannot modify protected file: {file_path}", file=sys.stderr)
            sys.exit(2)

if __name__ == "__main__":
    main()
```

## Configuration Examples

### Full Static Check Setup

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format.py",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint.py",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protected.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### TypeScript Project Setup

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/prettier_eslint.py",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/typecheck.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Python Project Setup

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/ruff.py",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/mypy.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```
