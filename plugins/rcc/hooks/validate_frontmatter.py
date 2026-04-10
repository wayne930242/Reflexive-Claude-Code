#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Validate frontmatter and structure of SKILL.md, agent, rule files, and Claude Code configuration files (.claude/settings.json, hooks/hooks.json)."""

import json
import re
import subprocess
import sys
from pathlib import Path


SKILL_ALLOWED_FIELDS = {
    "name", "description", "argument-hint", "disable-model-invocation",
    "user-invocable", "allowed-tools", "model", "effort", "context",
    "agent", "hooks", "paths", "shell",
}
AGENT_ALLOWED_FIELDS = {
    "name", "description", "model", "tools",
    "disallowedTools", "permissionMode", "maxTurns", "skills",
    "mcpServers", "hooks", "memory", "background", "effort",
    "isolation", "color", "initialPrompt",
}
RULES_ALLOWED_FIELDS = {"paths"}
HOOKS_ONLY_VARS = {"${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_PLUGIN_DATA}"}

# Hook configuration validation
HOOK_EVENTS = {
    "PreToolUse", "PostToolUse", "Stop", "SubagentStop", "SessionStart",
    "SessionEnd", "UserPromptSubmit", "PreCompact", "Notification"
}
HOOK_TYPES = {"prompt", "command"}
COMMON_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "Ask",
    "Monitor", "TaskCreate", "TaskUpdate", "TaskGet", "TaskList"
}
# Plugin hooks.json allowed top-level fields
PLUGIN_HOOKS_ALLOWED_FIELDS = {"description", "hooks"}
# Settings.json should only contain hook events as top-level keys

# Agent configuration validation
VALID_MODELS = {"inherit", "sonnet", "opus", "haiku"}
VALID_EFFORT_LEVELS = {"low", "medium", "high", "max"}
BUILTIN_SUBAGENT_TYPES = {"Explore", "Plan", "general-purpose"}
VALID_COLORS = {"blue", "green", "red", "purple", "yellow", "orange", "pink", "gray", "cyan", "magenta"}


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Extract frontmatter fields. Returns None if no frontmatter block."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    fields: dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if ":" in line:
            key = line.split(":", 1)[0].strip()
            if key:
                fields[key] = line.split(":", 1)[1].strip()
    return fields


def extract_markdown_links(text: str) -> list[str]:
    """Return relative paths from markdown links [text](path), excluding http(s)."""
    pattern = r'\[(?:[^\]]*)\]\(([^)]+)\)'
    links = re.findall(pattern, text)
    return [l for l in links if not l.startswith("http://") and not l.startswith("https://")]


def check_skill_md(path: Path) -> list[str]:
    """Run all four checks on a SKILL.md file."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    skill_dir = path.parent

    # ① Extra frontmatter fields
    fields = parse_frontmatter(text)
    if fields is not None:
        for f in sorted(set(fields.keys()) - SKILL_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')

    # ② Broken markdown links
    for link in extract_markdown_links(text):
        target = skill_dir / link
        if not target.exists():
            warnings.append(f"broken link: {link}")

    # ③ Orphaned files
    # A file is considered referenced if EITHER condition is true:
    #   - it appears in a markdown link [text](path)
    #   - its relative path or filename is mentioned anywhere in the text
    # Either form is sufficient — one handles the other's edge cases.
    linked_normalized = {str(Path(l)).replace("\\", "/") for l in extract_markdown_links(text)}
    for f in skill_dir.rglob("*"):
        if f == path or f.is_dir():
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        in_link = rel in linked_normalized
        in_text = rel in text or f.name in text
        if not (in_link or in_text):
            warnings.append(f"orphaned file: {rel}")

    # ④ hooks-only variables used in SKILL.md content
    # Strip fenced code blocks and inline code spans first to avoid false positives
    # in documentation tables that mention these variables as examples.
    text_plain = re.sub(r"```[\s\S]*?```", "", text)
    text_plain = re.sub(r"`[^`\n]+`", "", text_plain)
    for var in HOOKS_ONLY_VARS:
        if var in text_plain:
            warnings.append(f"invalid variable in SKILL.md: {var} (hooks/hooks.json only)")

    return warnings


def check_agent_md(path: Path) -> list[str]:
    """Check agent frontmatter for extra fields and validate values."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if fields is not None:
        # Check for extra fields
        for f in sorted(set(fields.keys()) - AGENT_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')

        # Validate model field
        if "model" in fields:
            model_value = fields["model"].strip().strip('"')
            if model_value and model_value not in VALID_MODELS:
                warnings.append(f'invalid model "{model_value}" (valid: {", ".join(sorted(VALID_MODELS))})')

        # Validate effort field
        if "effort" in fields:
            effort_value = fields["effort"].strip().strip('"')
            if effort_value and effort_value not in VALID_EFFORT_LEVELS:
                warnings.append(f'invalid effort "{effort_value}" (valid: {", ".join(sorted(VALID_EFFORT_LEVELS))})')

        # Validate color field
        if "color" in fields:
            color_value = fields["color"].strip().strip('"')
            if color_value and color_value not in VALID_COLORS:
                warnings.append(f'invalid color "{color_value}" (valid: {", ".join(sorted(VALID_COLORS))})')

        # Validate tools field (basic check for JSON array format)
        if "tools" in fields:
            tools_value = fields["tools"].strip()
            if tools_value and not tools_value.startswith('['):
                warnings.append('tools field should be a JSON array like ["Read", "Write"]')
            elif tools_value:
                try:
                    import json
                    tools_list = json.loads(tools_value)
                    if isinstance(tools_list, list):
                        for tool in tools_list:
                            if isinstance(tool, str):
                                # Basic validation: check for common tool names or MCP pattern
                                if (tool not in COMMON_TOOLS and
                                    not tool.startswith("mcp__") and
                                    not tool == "*" and
                                    not re.match(r"^[A-Za-z][A-Za-z0-9]*$", tool)):
                                    warnings.append(f'potentially invalid tool name "{tool}" in tools array')
                except (json.JSONDecodeError, TypeError):
                    warnings.append('tools field must be valid JSON array')

        # Check for required fields
        if "name" not in fields:
            warnings.append('missing required field "name"')
        if "description" not in fields:
            warnings.append('missing required field "description"')

        # Validate name matches filename
        if "name" in fields:
            expected_name = path.stem  # filename without .md extension
            actual_name = fields["name"].strip().strip('"')
            if actual_name != expected_name:
                warnings.append(f'name "{actual_name}" should match filename "{expected_name}"')

    return warnings


def check_rules_md(path: Path) -> list[str]:
    """Check rules frontmatter for extra fields."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if fields is not None:
        for f in sorted(set(fields.keys()) - RULES_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')
    return warnings


def validate_hook_structure(hook_config: dict, hook_index: int) -> list[str]:
    """Validate individual hook configuration structure."""
    warnings: list[str] = []

    # Check required fields
    if "type" not in hook_config:
        warnings.append(f"hook[{hook_index}]: missing required field 'type'")
        return warnings

    hook_type = hook_config["type"]
    if hook_type not in HOOK_TYPES:
        warnings.append(f"hook[{hook_index}]: invalid type '{hook_type}' (must be: {', '.join(HOOK_TYPES)})")

    # Type-specific validation
    if hook_type == "prompt":
        if "prompt" not in hook_config:
            warnings.append(f"hook[{hook_index}]: 'prompt' type requires 'prompt' field")
    elif hook_type == "command":
        if "command" not in hook_config:
            warnings.append(f"hook[{hook_index}]: 'command' type requires 'command' field")

    # Optional timeout validation
    if "timeout" in hook_config:
        try:
            timeout = int(hook_config["timeout"])
            if timeout <= 0 or timeout > 300:
                warnings.append(f"hook[{hook_index}]: timeout should be 1-300 seconds")
        except (ValueError, TypeError):
            warnings.append(f"hook[{hook_index}]: timeout must be a number")

    return warnings


def validate_matcher(matcher: str, matcher_context: str) -> list[str]:
    """Validate hook matcher pattern."""
    warnings: list[str] = []

    if not matcher:
        warnings.append(f"{matcher_context}: matcher cannot be empty")
        return warnings

    # Check for common patterns
    if matcher == "*":
        return []  # Wildcard is always valid

    # Basic regex validation
    try:
        import re
        re.compile(matcher)
    except re.error as e:
        warnings.append(f"{matcher_context}: invalid regex pattern '{matcher}': {e}")
        return warnings

    # Check for common tool patterns
    tools_in_matcher = [t.strip() for t in matcher.split("|")]
    for tool in tools_in_matcher:
        if tool and not tool.startswith("mcp__") and tool not in COMMON_TOOLS and not re.match(r"^[A-Za-z][A-Za-z0-9]*$", tool):
            warnings.append(f"{matcher_context}: potentially invalid tool name '{tool}' in matcher")

    return warnings


def check_settings_json(path: Path) -> list[str]:
    """Validate .claude/settings.json format."""
    warnings: list[str] = []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        warnings.append(f"invalid JSON: {e}")
        return warnings
    except Exception as e:
        warnings.append(f"failed to read file: {e}")
        return warnings

    if not isinstance(data, dict):
        warnings.append("root must be an object")
        return warnings

    # Check for invalid top-level keys (should only be hook events)
    for key in data.keys():
        if key not in HOOK_EVENTS:
            warnings.append(f"invalid hook event '{key}' (valid events: {', '.join(sorted(HOOK_EVENTS))})")

    # Validate hook event structures
    for event_name, event_configs in data.items():
        if event_name not in HOOK_EVENTS:
            continue  # Already warned above

        if not isinstance(event_configs, list):
            warnings.append(f"'{event_name}': must be an array")
            continue

        for i, config in enumerate(event_configs):
            if not isinstance(config, dict):
                warnings.append(f"'{event_name}'[{i}]: must be an object")
                continue

            # Check required fields for hook configuration
            if "matcher" not in config:
                warnings.append(f"'{event_name}'[{i}]: missing required field 'matcher'")
            else:
                warnings.extend(validate_matcher(config["matcher"], f"'{event_name}'[{i}]"))

            if "hooks" not in config:
                warnings.append(f"'{event_name}'[{i}]: missing required field 'hooks'")
            elif not isinstance(config["hooks"], list):
                warnings.append(f"'{event_name}'[{i}]: 'hooks' must be an array")
            else:
                for j, hook in enumerate(config["hooks"]):
                    if isinstance(hook, dict):
                        warnings.extend(validate_hook_structure(hook, j))

    return warnings


def check_hooks_json(path: Path) -> list[str]:
    """Validate plugin hooks/hooks.json format."""
    warnings: list[str] = []

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        warnings.append(f"invalid JSON: {e}")
        return warnings
    except Exception as e:
        warnings.append(f"failed to read file: {e}")
        return warnings

    if not isinstance(data, dict):
        warnings.append("root must be an object")
        return warnings

    # Check for extra top-level fields
    for field in data.keys():
        if field not in PLUGIN_HOOKS_ALLOWED_FIELDS:
            warnings.append(f"extra top-level field: '{field}' (allowed: {', '.join(PLUGIN_HOOKS_ALLOWED_FIELDS)})")

    # Check hooks structure
    if "hooks" not in data:
        warnings.append("missing required field 'hooks'")
        return warnings

    hooks = data["hooks"]
    if not isinstance(hooks, dict):
        warnings.append("'hooks' must be an object")
        return warnings

    # Validate each hook event
    for event_name, event_configs in hooks.items():
        if event_name not in HOOK_EVENTS:
            warnings.append(f"invalid hook event 'hooks.{event_name}' (valid events: {', '.join(sorted(HOOK_EVENTS))})")
            continue

        if not isinstance(event_configs, list):
            warnings.append(f"'hooks.{event_name}': must be an array")
            continue

        for i, config in enumerate(event_configs):
            if not isinstance(config, dict):
                warnings.append(f"'hooks.{event_name}'[{i}]: must be an object")
                continue

            # Check required fields
            if "matcher" not in config:
                warnings.append(f"'hooks.{event_name}'[{i}]: missing required field 'matcher'")
            else:
                warnings.extend(validate_matcher(config["matcher"], f"'hooks.{event_name}'[{i}]"))

            if "hooks" not in config:
                warnings.append(f"'hooks.{event_name}'[{i}]: missing required field 'hooks'")
            elif not isinstance(config["hooks"], list):
                warnings.append(f"'hooks.{event_name}'[{i}]: 'hooks' must be an array")
            else:
                for j, hook in enumerate(config["hooks"]):
                    if isinstance(hook, dict):
                        warnings.extend(validate_hook_structure(hook, j))

    return warnings


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

        # .claude-plugin/ JSON files → run claude plugin validate on parent dir
        if path.parent.name == ".claude-plugin" and path.suffix == ".json":
            warnings = check_plugin_validate(path.parent.parent)
        elif path.name == "SKILL.md" and any(path.is_relative_to(sd) for sd in skill_dirs):
            warnings = check_skill_md(path)
        elif path.suffix == ".md" and any(path.is_relative_to(ad) for ad in agent_dirs):
            warnings = check_agent_md(path)
        elif path.suffix == ".md" and rules_dir.exists() and path.is_relative_to(rules_dir):
            warnings = check_rules_md(path)
        # .claude/settings.json validation
        elif path.name == "settings.json" and path.parent.name == ".claude":
            warnings = check_settings_json(path)
        # Plugin hooks/hooks.json validation
        elif path.name == "hooks.json" and path.parent.name == "hooks":
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
