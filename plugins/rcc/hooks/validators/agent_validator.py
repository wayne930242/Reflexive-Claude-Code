"""Agent frontmatter validation functions."""

import json
import re
from pathlib import Path
from .constants import (
    AGENT_ALLOWED_FIELDS, VALID_MODELS, VALID_EFFORT_LEVELS,
    VALID_PERMISSION_MODES, VALID_MEMORY_SCOPES, VALID_ISOLATION_MODES,
    VALID_COLORS, CLAUDE_CODE_TOOLS
)
from .utils import parse_frontmatter


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

        # Validate permissionMode field
        if "permissionMode" in fields:
            perm_value = fields["permissionMode"].strip().strip('"')
            if perm_value and perm_value not in VALID_PERMISSION_MODES:
                warnings.append(f'invalid permissionMode "{perm_value}" (valid: {", ".join(sorted(VALID_PERMISSION_MODES))})')

        # Validate memory field
        if "memory" in fields:
            memory_value = fields["memory"].strip().strip('"')
            if memory_value and memory_value not in VALID_MEMORY_SCOPES:
                warnings.append(f'invalid memory "{memory_value}" (valid: {", ".join(sorted(VALID_MEMORY_SCOPES))})')

        # Validate isolation field
        if "isolation" in fields:
            isolation_value = fields["isolation"].strip().strip('"')
            if isolation_value and isolation_value not in VALID_ISOLATION_MODES:
                warnings.append(f'invalid isolation "{isolation_value}" (valid: {", ".join(sorted(VALID_ISOLATION_MODES))})')

        # Validate tools field (basic check for JSON array format)
        if "tools" in fields:
            tools_value = fields["tools"].strip()
            if tools_value and not tools_value.startswith('['):
                warnings.append('tools field should be a JSON array like ["Read", "Write"]')
            elif tools_value:
                try:
                    tools_list = json.loads(tools_value)
                    if isinstance(tools_list, list):
                        for tool in tools_list:
                            if isinstance(tool, str):
                                # Basic validation: check for Claude Code tool names or MCP pattern
                                if (tool not in CLAUDE_CODE_TOOLS and
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