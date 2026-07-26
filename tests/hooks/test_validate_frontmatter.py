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


def _load_utils() -> types.ModuleType:
    """Load validators.utils, where the parsing helpers live."""
    if str(SCRIPT.parent) not in sys.path:
        sys.path.insert(0, str(SCRIPT.parent))
    import validators.utils
    return validators.utils


def test_parse_frontmatter_returns_fields():
    utils = _load_utils()
    text = "---\nname: my-skill\ndescription: does stuff\n---\n\n# Body"
    result = utils.parse_frontmatter(text)
    assert result == {"name": "my-skill", "description": "does stuff"}


def test_parse_frontmatter_no_frontmatter_returns_none():
    utils = _load_utils()
    assert utils.parse_frontmatter("# No frontmatter here") is None


def test_parse_frontmatter_empty_block_returns_empty_dict():
    utils = _load_utils()
    assert utils.parse_frontmatter("---\n---\n") == {}


def test_extract_markdown_links_relative_only():
    utils = _load_utils()
    text = "[foo](references/foo.md) [bar](https://example.com) [baz](./scripts/run.sh)"
    result = utils.extract_markdown_links(text)
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


def test_check_skill_md_every_documented_field_no_warn(tmp_path):
    """Every field in the official Frontmatter reference table must be accepted.

    https://code.claude.com/docs/en/skills.md — a field missing from
    SKILL_ALLOWED_FIELDS makes the hook warn on a perfectly valid skill.
    """
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    frontmatter = "\n".join([
        "name: my-skill",
        "description: Use when x.",
        "when_to_use: When the user says y.",
        "argument-hint: '[slug]'",
        "arguments: slug format",
        "disable-model-invocation: true",
        "user-invocable: true",
        "allowed-tools: Read Grep",
        "disallowed-tools: AskUserQuestion",
        "model: sonnet",
        "effort: high",
        "context: fork",
        "agent: general-purpose",
        "background: false",
        "paths: src/**",
        "shell: bash",
    ])
    (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---\n# Body\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    extra = [w for w in warnings if "extra frontmatter" in w]
    assert extra == [], f"documented fields rejected: {extra}"


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


def test_check_skill_md_md_mentioned_in_text_no_warn(tmp_path):
    """.md file mentioned in plain text (not markdown link) should NOT warn."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "spec.md").write_text("# Spec")
    content = "---\nname: x\ndescription: y\n---\n\nSee references/spec.md for details.\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("spec.md" in w and "orphaned" in w for w in warnings)


def test_check_skill_md_orphaned_md_warns(tmp_path):
    """Unlisted .md reference file (not in link AND not in text) should warn."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "orphan.md").write_text("# Orphan")
    (skill_dir / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\n# No links\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("orphan.md" in w for w in warnings)


def test_check_skill_md_script_mentioned_in_text_no_warn(tmp_path):
    """Script referenced via ${CLAUDE_SKILL_DIR}/scripts/foo.py plain text should NOT warn."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "helper.py").write_text("# script")
    content = "---\nname: x\ndescription: y\n---\n\nRun `${CLAUDE_SKILL_DIR}/scripts/helper.py`\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("helper.py" in w and "orphaned" in w for w in warnings)


def test_check_skill_md_script_not_mentioned_warns(tmp_path):
    """Script that is never mentioned anywhere in SKILL.md should warn."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "unused.py").write_text("# unused")
    (skill_dir / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\n# No script refs\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("unused.py" in w for w in warnings)


def test_check_skill_md_ts_script_mentioned_no_warn(tmp_path):
    """TypeScript/Go/JS scripts mentioned via plain text should NOT warn."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True)
    (scripts_dir / "runner.ts").write_text("// ts script")
    (scripts_dir / "tool.go").write_text("// go script")
    content = (
        "---\nname: x\ndescription: y\n---\n\n"
        "Run `${CLAUDE_SKILL_DIR}/scripts/runner.ts`\n"
        "Also uses scripts/tool.go\n"
    )
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("runner.ts" in w or "tool.go" in w for w in warnings)


def test_check_skill_md_hooks_only_var_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    content = "---\nname: x\ndescription: y\n---\n\nUse ${CLAUDE_PLUGIN_ROOT}/data here.\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("CLAUDE_PLUGIN_ROOT" in w for w in warnings)


def test_check_skill_md_dot_slash_link_no_orphan_warn(tmp_path):
    """Links with ./ prefix should not cause orphan false positives."""
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "real.md").write_text("# Real")
    content = "---\nname: x\ndescription: y\n---\n\n[ref](./references/real.md)\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("real.md" in w and "orphaned" in w for w in warnings)


def test_check_agent_md_extra_field_warns(tmp_path):
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: inherit\ntools: []\ntags: bad\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert any("tags" in w for w in warnings)


def test_check_agent_md_allowed_fields_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: inherit\ntools: []\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert warnings == []


def test_check_agent_md_context_is_not_an_agent_field(tmp_path):
    """`context: fork` belongs to skills, not agents.

    https://code.claude.com/docs/en/sub-agents.md lists no `context` field; the
    official text places it in skills ("With `context: fork` in a skill").
    """
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\ncontext: fork\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert any("context" in w for w in warnings)


def test_check_agent_md_every_documented_field_no_warn(tmp_path):
    """Every field in the official subagent frontmatter table must be accepted."""
    mod = _load_module()
    frontmatter = "\n".join([
        "name: my-agent",
        "description: x",
        'tools: ["Read", "Grep"]',
        "disallowedTools: AskUserQuestion",
        "model: fable",
        "permissionMode: manual",
        "maxTurns: 10",
        "skills: my-skill",
        "mcpServers: slack",
        "memory: project",
        "background: true",
        "effort: xhigh",
        "isolation: worktree",
        "color: cyan",
        "initialPrompt: Start here.",
    ])
    (tmp_path / "my-agent.md").write_text(f"---\n{frontmatter}\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert warnings == [], f"documented fields rejected: {warnings}"


def test_check_agent_md_full_model_id_no_warn(tmp_path):
    """The model field accepts a full model ID, not only the aliases."""
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: claude-opus-5\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert not any("invalid model" in w for w in warnings)


def test_check_agent_md_bogus_model_warns(tmp_path):
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: gpt-4\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert any("invalid model" in w for w in warnings)


def test_check_rules_md_extra_field_warns(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("---\npaths: src/**\ntags: bad\n---\n# Rule\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert any("tags" in w for w in warnings)


def test_check_rules_md_paths_only_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("---\npaths: src/**\n---\n# Rule\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert warnings == []


def test_check_rules_md_no_frontmatter_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("# Rule without frontmatter\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert warnings == []


def test_discover_finds_plugin_skills_dir(tmp_path):
    mod = _load_module()
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    (plugin_dir / "skills").mkdir()
    skill_dirs, agent_dirs = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "skills" in skill_dirs


def test_discover_respects_custom_skills_field(tmp_path):
    mod = _load_module()
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x","skills":"custom-skills"}')
    (plugin_dir / "custom-skills").mkdir()
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "custom-skills" in skill_dirs


def test_discover_includes_claude_skills(tmp_path):
    mod = _load_module()
    (tmp_path / ".claude" / "skills").mkdir(parents=True)
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert tmp_path / ".claude" / "skills" in skill_dirs


def test_discover_skips_nonexistent_dirs(tmp_path):
    mod = _load_module()
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    # skills/ does NOT exist
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "skills" not in skill_dirs


def test_hook_silent_on_unrelated_file(tmp_path):
    """Files outside plugin paths produce no output."""
    (tmp_path / "random.md").write_text("---\ntags: foo\n---\n# hi\n")
    result = run_hook(str(tmp_path / "random.md"), str(tmp_path))
    assert result == {}


def test_hook_warns_on_skill_extra_field(tmp_path):
    """SKILL.md with extra frontmatter field triggers systemMessage."""
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    skill_dir = plugin_dir / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: x\ntags: bad\n---\n# Body\n")
    result = run_hook(str(skill_dir / "SKILL.md"), str(tmp_path))
    assert "systemMessage" in result
    assert "tags" in result["systemMessage"]


def test_hook_silent_on_valid_skill(tmp_path):
    """Valid SKILL.md produces no output."""
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    skill_dir = plugin_dir / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: x\n---\n# Body\n")
    result = run_hook(str(skill_dir / "SKILL.md"), str(tmp_path))
    assert result == {}
