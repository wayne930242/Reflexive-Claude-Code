"""Configuration file validation (settings.json, hooks.json)."""

import json
import re
from pathlib import Path
from .constants import (
    HOOK_EVENTS, HOOK_TYPES, PLUGIN_HOOKS_ALLOWED_FIELDS, CLAUDE_CODE_TOOLS
)


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
        re.compile(matcher)
    except re.error as e:
        warnings.append(f"{matcher_context}: invalid regex pattern '{matcher}': {e}")
        return warnings

    # Check for common tool patterns
    tools_in_matcher = [t.strip() for t in matcher.split("|")]
    for tool in tools_in_matcher:
        if tool and not tool.startswith("mcp__") and tool not in CLAUDE_CODE_TOOLS and not re.match(r"^[A-Za-z][A-Za-z0-9]*$", tool):
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