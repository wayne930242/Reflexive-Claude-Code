#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Validate frontmatter and structure of SKILL.md, agent, and rule files."""

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
AGENT_ALLOWED_FIELDS = {"name", "description", "model", "context", "tools"}
RULES_ALLOWED_FIELDS = {"paths"}
HOOKS_ONLY_VARS = {"${CLAUDE_PLUGIN_ROOT}", "${CLAUDE_PLUGIN_DATA}"}


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
    # .md reference files must appear in a markdown link (they are loaded on-demand by Claude).
    # Executable scripts (.py, .sh, .js, .mjs, .cjs, .ts, .go, etc.) only need to be mentioned
    # anywhere in the text (e.g. via ${CLAUDE_SKILL_DIR}/scripts/foo.py or plain text reference).
    linked_normalized = {str(Path(l)).replace("\\", "/") for l in extract_markdown_links(text)}
    for f in skill_dir.rglob("*"):
        if f == path or f.is_dir():
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        if f.suffix == ".md":
            if rel not in linked_normalized:
                warnings.append(f"orphaned file: {rel}")
        else:
            # Scripts etc.: mentioned anywhere in text (path or filename) is sufficient
            if rel not in text and f.name not in text:
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
    """Check agent frontmatter for extra fields."""
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    if fields is not None:
        for f in sorted(set(fields.keys()) - AGENT_ALLOWED_FIELDS):
            warnings.append(f'extra frontmatter field: "{f}"')
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

        if warnings:
            rel = path.relative_to(cwd) if path.is_relative_to(cwd) else path
            lines = "\n".join(f"  - {w}" for w in warnings)
            msg = f"⚠ validate-frontmatter [{rel}]:\n{lines}"
            print(json.dumps({"systemMessage": msg}))

    except Exception:
        pass  # never block Claude on validator errors (file may be mid-edit)

    sys.exit(0)


if __name__ == "__main__":
    main()
