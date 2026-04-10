#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Validate frontmatter and structure of SKILL.md, agent, rule files, and Claude Code configuration files."""

import json
import subprocess
import sys
from pathlib import Path

# Import modular validators
try:
    from validators.skill_validator import check_skill_md
    from validators.agent_validator import check_agent_md
    from validators.rules_validator import check_rules_md
    from validators.config_validator import check_settings_json, check_hooks_json
except ImportError:
    # Fallback for when script is run directly without package structure
    sys.path.append(str(Path(__file__).parent))
    from validators.skill_validator import check_skill_md
    from validators.agent_validator import check_agent_md
    from validators.rules_validator import check_rules_md
    from validators.config_validator import check_settings_json, check_hooks_json


def discover_skill_and_agent_dirs(cwd: Path) -> tuple[list[Path], list[Path]]:
    """Find valid skill and agent directories from plugin roots and .claude/."""
    skill_dirs: list[Path] = []
    agent_dirs: list[Path] = []

    for plugin_json_path in cwd.rglob(".claude-plugin/plugin.json"):
        plugin_root = plugin_json_path.parent.parent
        try:
            data = json.loads(plugin_json_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}

        for field, target_list in [("skills", skill_dirs), ("agents", agent_dirs)]:
            default = field  # "skills" or "agents"
            value = data.get(field, default)
            if isinstance(value, str):
                candidate = plugin_root / value
                if candidate.exists() and candidate not in target_list:
                    target_list.append(candidate)

    # Project-level .claude/skills and .claude/agents
    for subdir, target_list in [("skills", skill_dirs), ("agents", agent_dirs)]:
        candidate = cwd / ".claude" / subdir
        if candidate.exists() and candidate not in target_list:
            target_list.append(candidate)

    return skill_dirs, agent_dirs


def check_plugin_validate(plugin_dir: Path) -> list[str]:
    """Run `claude plugin validate` on plugin_dir (the dir containing .claude-plugin/)."""
    try:
        result = subprocess.run(
            ["claude", "plugin", "validate", str(plugin_dir)],
            capture_output=True, text=True, timeout=30
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0 and output:
            return [f"plugin validate: {line}" for line in output.splitlines() if line.strip()]
    except FileNotFoundError:
        pass  # claude CLI not available
    except Exception as e:
        return [f"plugin validate failed: {e}"]
    return []


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    try:
        file_path_str = data.get("tool_input", {}).get("file_path", "")
        cwd_str = data.get("cwd", "")
        if not file_path_str:
            sys.exit(0)

        cwd = Path(cwd_str) if cwd_str else Path.cwd()
        path = Path(file_path_str)
        if not path.is_absolute():
            path = cwd / path
        if not path.exists():
            sys.exit(0)

        skill_dirs, agent_dirs = discover_skill_and_agent_dirs(cwd)
        rules_dir = cwd / ".claude" / "rules"
        warnings: list[str] = []

        # Route to appropriate validator based on file type and location
        if path.parent.name == ".claude-plugin" and path.suffix == ".json":
            # .claude-plugin/ JSON files → run claude plugin validate on parent dir
            warnings = check_plugin_validate(path.parent.parent)
        elif path.name == "SKILL.md" and any(path.is_relative_to(sd) for sd in skill_dirs):
            # SKILL.md files in skill directories
            warnings = check_skill_md(path)
        elif path.suffix == ".md" and any(path.is_relative_to(ad) for ad in agent_dirs):
            # Agent .md files in agent directories
            warnings = check_agent_md(path)
        elif path.suffix == ".md" and rules_dir.exists() and path.is_relative_to(rules_dir):
            # Rule .md files in .claude/rules/
            warnings = check_rules_md(path)
        elif path.name == "settings.json" and path.parent.name == ".claude":
            # .claude/settings.json validation
            warnings = check_settings_json(path)
        elif path.name == "hooks.json" and path.parent.name == "hooks":
            # Plugin hooks/hooks.json validation
            warnings = check_hooks_json(path)

        if warnings:
            rel = path.relative_to(cwd) if path.is_relative_to(cwd) else path
            lines = "\n".join(f"  - {w}" for w in warnings)
            msg = f"⚠ validate-frontmatter [{rel}]:\n{lines}"
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": msg,
                },
                "systemMessage": msg,
            }))

    except Exception:
        pass  # never block Claude on validator errors (file may be mid-edit)

    sys.exit(0)


if __name__ == "__main__":
    main()
