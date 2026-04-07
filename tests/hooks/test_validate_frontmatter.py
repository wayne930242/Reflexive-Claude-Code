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


def test_extract_markdown_links_relative_only():
    mod = _load_module()
    text = "[foo](references/foo.md) [bar](https://example.com) [baz](./scripts/run.sh)"
    result = mod.extract_markdown_links(text)
    assert "references/foo.md" in result
    assert "https://example.com" not in result
    assert "./scripts/run.sh" in result


def test_check_skill_md_extra_field_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ntags: foo\n---\n# Body\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("tags" in w for w in warnings)


def test_check_skill_md_allowed_fields_no_warn(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: Use when x.\n---\n# Body\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("extra frontmatter" in w for w in warnings)


def test_check_skill_md_broken_link_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    content = "---\nname: x\ndescription: y\n---\n\n[ref](references/missing.md)\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("missing.md" in w for w in warnings)


def test_check_skill_md_valid_link_no_warn(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "real.md").write_text("# Real")
    content = "---\nname: x\ndescription: y\n---\n\n[ref](references/real.md)\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("broken link" in w for w in warnings)


def test_check_skill_md_orphaned_file_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "orphan.md").write_text("# Orphan")
    (skill_dir / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\n# No links\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("orphan.md" in w for w in warnings)


def test_check_skill_md_hooks_only_var_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    content = "---\nname: x\ndescription: y\n---\n\nUse ${CLAUDE_PLUGIN_ROOT}/data here.\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("CLAUDE_PLUGIN_ROOT" in w for w in warnings)
