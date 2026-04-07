"""Tests for validate_frontmatter.py hook script."""
import importlib.util
import json
import subprocess
import sys
import types
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


def _load_module() -> types.ModuleType:
    """Load validate_frontmatter as a module without executing main()."""
    spec = importlib.util.spec_from_file_location("validate_frontmatter", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_parse_frontmatter_returns_fields():
    mod = _load_module()
    text = "---\nname: my-skill\ndescription: does stuff\n---\n\n# Body"
    result = mod.parse_frontmatter(text)
    assert result == {"name": "my-skill", "description": "does stuff"}


def test_parse_frontmatter_no_frontmatter_returns_none():
    mod = _load_module()
    assert mod.parse_frontmatter("# No frontmatter here") is None


def test_parse_frontmatter_empty_block_returns_empty_dict():
    mod = _load_module()
    assert mod.parse_frontmatter("---\n---\n") == {}
