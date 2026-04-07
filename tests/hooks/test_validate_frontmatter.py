"""Tests for validate_frontmatter.py hook script."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins/rcc/hooks/validate_frontmatter.py"


def run_hook(file_path: str, cwd: str) -> dict:
    """Run the hook script with given file_path and cwd, return parsed stdout."""
    stdin = json.dumps({
        "tool_input": {"file_path": file_path},
        "cwd": cwd
    })
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=stdin, capture_output=True, text=True
    )
    if result.stdout.strip():
        return json.loads(result.stdout)
    return {}
