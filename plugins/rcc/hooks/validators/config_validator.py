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
    prefix = f"hook[{hook_index}]"

    # Check required fields
    if "type" not in hook_config:
        warnings.append(f"{prefix}: missing required field 'type'")
        return warnings

    hook_type = hook_config["type"]
    if hook_type not in HOOK_TYPES:
        warnings.append(f"{prefix}: invalid type '{hook_type}' (must be: {', '.join(sorted(HOOK_TYPES))})")
        return warnings

    # Common optional fields valid for all hook types
    common_fields = {"type", "timeout", "if", "statusMessage", "once"}

    # Type-specific required + optional fields
    type_fields: dict[str, tuple[set[str], set[str]]] = {
        "command": ({"command"}, {"async", "shell"}),
        "http":    ({"url"}, {"headers", "allowedEnvVars"}),
        "prompt":  ({"prompt"}, {"model"}),
        "agent":   ({"prompt"}, {"model"}),
    }

    required, optional = type_fields.get(hook_type, (set(), set()))
    allowed = common_fields | required | optional

    # Check required fields for this type
    for field in required:
        if field not in hook_config:
            warnings.append(f"{prefix}: '{hook_type}' type requires '{field}' field")

    # Check for unknown fields
    for field in hook_config:
        if field not in allowed:
            warnings.append(f"{prefix}: unexpected field '{field}' for '{hook_type}' hook")

    # Optional timeout validation (max varies by type but 600 is safe upper bound)
    if "timeout" in hook_config:
        try:
            timeout = int(hook_config["timeout"])
            if timeout <= 0 or timeout > 600:
                warnings.append(f"{prefix}: timeout should be 1-600 seconds")
        except (ValueError, TypeError):
            warnings.append(f"{prefix}: timeout must be a number")

    # Validate 'async' is boolean for command hooks
    if "async" in hook_config and not isinstance(hook_config["async"], bool):
        warnings.append(f"{prefix}: 'async' must be a boolean")

    # Validate 'once' is boolean
    if "once" in hook_config and not isinstance(hook_config["once"], bool):
        warnings.append(f"{prefix}: 'once' must be a boolean")

    # Validate 'headers' is object for http hooks
    if "headers" in hook_config and not isinstance(hook_config["headers"], dict):
        warnings.append(f"{prefix}: 'headers' must be an object")

    # Validate 'allowedEnvVars' is array for http hooks
    if "allowedEnvVars" in hook_config and not isinstance(hook_config["allowedEnvVars"], list):
        warnings.append(f"{prefix}: 'allowedEnvVars' must be an array")

    return warnings


# Events where matcher matches tool names
TOOL_EVENTS = {
    "PreToolUse", "PostToolUse", "PostToolUseFailure",
    "PermissionRequest", "PermissionDenied",
}

# Events that don't support matcher at all
NO_MATCHER_EVENTS = {
    "UserPromptSubmit", "Stop", "TeammateIdle",
    "TaskCreated", "TaskCompleted",
    "WorktreeCreate", "WorktreeRemove", "CwdChanged",
}


def validate_matcher(matcher: str, matcher_context: str, event_name: str = "") -> list[str]:
    """Validate hook matcher pattern."""
    warnings: list[str] = []

    if not matcher:
        warnings.append(f"{matcher_context}: matcher cannot be empty")
        return warnings

    if matcher == "*":
        return []

    # Basic regex validation
    try:
        re.compile(matcher)
    except re.error as e:
        warnings.append(f"{matcher_context}: invalid regex pattern '{matcher}': {e}")
        return warnings

    # Tool name validation only for tool-related events
    if event_name in TOOL_EVENTS:
        tools_in_matcher = [t.strip() for t in matcher.split("|")]
        for tool in tools_in_matcher:
            if tool and not tool.startswith("mcp__") and tool not in CLAUDE_CODE_TOOLS and not re.match(r"^[A-Za-z][A-Za-z0-9]*$", tool):
                warnings.append(f"{matcher_context}: potentially invalid tool name '{tool}' in matcher")

    return warnings


def check_settings_json(path: Path) -> list[str]:
    """Validate .claude/settings.json format.

    settings.json supports many top-level keys (env, permissions, model, hooks, etc.).
    This validator only checks the 'hooks' field structure when present.
    """
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

    # Only validate the 'hooks' field — other top-level keys are valid settings
    hooks_data = data.get("hooks")
    if hooks_data is None:
        return warnings

    if not isinstance(hooks_data, dict):
        warnings.append("'hooks' must be an object")
        return warnings

    # Validate hook event structures inside 'hooks'
    for event_name, event_configs in hooks_data.items():
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

            # Check required fields for hook configuration
            if "matcher" not in config:
                warnings.append(f"'hooks.{event_name}'[{i}]: missing required field 'matcher'")
            else:
                warnings.extend(validate_matcher(config["matcher"], f"'hooks.{event_name}'[{i}]", event_name))

            if "hooks" not in config:
                warnings.append(f"'hooks.{event_name}'[{i}]: missing required field 'hooks'")
            elif not isinstance(config["hooks"], list):
                warnings.append(f"'hooks.{event_name}'[{i}]: 'hooks' must be an array")
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
                warnings.extend(validate_matcher(config["matcher"], f"'hooks.{event_name}'[{i}]", event_name))

            if "hooks" not in config:
                warnings.append(f"'hooks.{event_name}'[{i}]: missing required field 'hooks'")
            elif not isinstance(config["hooks"], list):
                warnings.append(f"'hooks.{event_name}'[{i}]: 'hooks' must be an array")
            else:
                for j, hook in enumerate(config["hooks"]):
                    if isinstance(hook, dict):
                        warnings.extend(validate_hook_structure(hook, j))

    return warnings