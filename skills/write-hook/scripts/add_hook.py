#!/usr/bin/env python3
"""Add a static analysis hook to Claude Code project."""

import argparse
import json
import os
import stat
import sys
from pathlib import Path

TEMPLATES = {
    "lint": {
        "description": "Linting hook for code quality",
        "extensions": {
            "js": [".js", ".jsx", ".mjs"],
            "ts": [".ts", ".tsx"],
            "py": [".py"],
        },
        "script": '''#!/usr/bin/env python3
"""Linting hook - validates code quality after file changes."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    path = Path(file_path)
    ext = path.suffix.lower()

    # JavaScript/TypeScript linting
    if ext in (".js", ".jsx", ".ts", ".tsx", ".mjs"):
        result = subprocess.run(
            ["npx", "eslint", "--format", "compact", "--max-warnings", "0", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors = result.stdout.strip().split("\\n")[:5]
            print("ESLint errors:", file=sys.stderr)
            print("\\n".join(errors), file=sys.stderr)
            sys.exit(2)

    # Python linting
    elif ext == ".py":
        result = subprocess.run(
            ["ruff", "check", "--output-format", "concise", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors = result.stdout.strip().split("\\n")[:5]
            print("Ruff errors:", file=sys.stderr)
            print("\\n".join(errors), file=sys.stderr)
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
''',
    },
    "format": {
        "description": "Auto-formatting hook",
        "extensions": {
            "js": [".js", ".jsx", ".mjs", ".ts", ".tsx"],
            "py": [".py"],
            "md": [".md", ".mdx"],
        },
        "script": '''#!/usr/bin/env python3
"""Formatting hook - auto-formats files after changes."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    path = Path(file_path)
    ext = path.suffix.lower()

    # JavaScript/TypeScript/Markdown formatting
    if ext in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".json", ".md", ".mdx"):
        result = subprocess.run(
            ["npx", "prettier", "--check", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            subprocess.run(["npx", "prettier", "--write", file_path], capture_output=True)
            print(f"Auto-formatted: {file_path}")

    # Python formatting
    elif ext == ".py":
        subprocess.run(["ruff", "format", file_path], capture_output=True)
        print(f"Auto-formatted: {file_path}")

    sys.exit(0)

if __name__ == "__main__":
    main()
''',
    },
    "typecheck": {
        "description": "Type checking hook",
        "extensions": {
            "ts": [".ts", ".tsx"],
            "py": [".py"],
        },
        "script": '''#!/usr/bin/env python3
"""Type checking hook - validates types after file changes."""

import json
import subprocess
import sys
from pathlib import Path

def main():
    data = json.load(sys.stdin)
    file_path = data.get("tool_input", {}).get("file_path", "")

    if not file_path:
        sys.exit(0)

    path = Path(file_path)
    ext = path.suffix.lower()

    # TypeScript type checking
    if ext in (".ts", ".tsx"):
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "--pretty", "false"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            # Filter errors for this specific file
            errors = [
                line for line in result.stdout.split("\\n")
                if file_path in line or path.name in line
            ][:5]
            if errors:
                print("TypeScript errors:", file=sys.stderr)
                print("\\n".join(errors), file=sys.stderr)
                sys.exit(2)

    # Python type checking
    elif ext == ".py":
        result = subprocess.run(
            ["mypy", "--no-error-summary", file_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            errors = result.stdout.strip().split("\\n")[:5]
            print("Type errors:", file=sys.stderr)
            print("\\n".join(errors), file=sys.stderr)
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
''',
    },
    "custom": {
        "description": "Custom static analysis hook",
        "extensions": {},
        "script": '''#!/usr/bin/env python3
"""Custom static analysis hook template."""

import json
import sys

def main():
    data = json.load(sys.stdin)

    # Available fields:
    # - data["hook_event_name"]: PreToolUse, PostToolUse, etc.
    # - data["tool_name"]: Write, Edit, Bash, etc.
    # - data["tool_input"]: Tool-specific input (e.g., file_path, command)
    # - data["cwd"]: Current working directory

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Example: Check file operations
    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")

        # Add your validation logic here
        # To block: print to stderr and exit(2)
        # To warn: print to stderr and exit(1)
        # To pass: exit(0)

        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
''',
    },
}


def update_settings(settings_path: Path, hook_name: str, event: str, matcher: str):
    """Update or create settings.json with the new hook configuration."""
    settings = {}
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)

    hooks = settings.setdefault("hooks", {})
    event_hooks = hooks.setdefault(event, [])

    # Check if matcher already exists
    hook_config = {
        "type": "command",
        "command": f'"$CLAUDE_PROJECT_DIR"/.claude/hooks/{hook_name}.py',
        "timeout": 30,
    }

    for entry in event_hooks:
        if entry.get("matcher") == matcher:
            # Add to existing matcher
            entry.setdefault("hooks", []).append(hook_config)
            break
    else:
        # Create new matcher entry
        event_hooks.append({"matcher": matcher, "hooks": [hook_config]})

    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a static analysis hook for Claude Code"
    )
    parser.add_argument("name", help="Hook name (e.g., eslint_check)")
    parser.add_argument(
        "--type",
        "-t",
        choices=list(TEMPLATES.keys()),
        default="custom",
        help="Hook template type",
    )
    parser.add_argument(
        "--path",
        "-p",
        default=".claude/hooks",
        help="Output directory (default: .claude/hooks)",
    )
    parser.add_argument(
        "--event",
        "-e",
        default="PostToolUse",
        choices=["PreToolUse", "PostToolUse", "UserPromptSubmit"],
        help="Hook event (default: PostToolUse)",
    )
    parser.add_argument(
        "--matcher",
        "-m",
        default="Write|Edit",
        help="Tool matcher pattern (default: Write|Edit)",
    )
    parser.add_argument(
        "--no-config",
        action="store_true",
        help="Don't update settings.json",
    )

    args = parser.parse_args()

    # Determine project root
    project_dir = Path.cwd()
    hooks_dir = project_dir / args.path
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Create hook script
    hook_path = hooks_dir / f"{args.name}.py"
    template = TEMPLATES[args.type]

    if hook_path.exists():
        print(f"Error: {hook_path} already exists", file=sys.stderr)
        sys.exit(1)

    with open(hook_path, "w") as f:
        f.write(template["script"])

    # Make executable
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Created: {hook_path}")

    # Update settings.json
    if not args.no_config:
        settings_path = project_dir / ".claude" / "settings.json"
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        update_settings(settings_path, args.name, args.event, args.matcher)
        print(f"Updated: {settings_path}")

    print(f"\nHook '{args.name}' initialized successfully!")
    print(f"Type: {args.type} ({template['description']})")
    print(f"Event: {args.event}")
    print(f"Matcher: {args.matcher}")


if __name__ == "__main__":
    main()
