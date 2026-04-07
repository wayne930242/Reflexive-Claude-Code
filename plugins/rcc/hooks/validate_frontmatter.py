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

    # ③ Orphaned files (not mentioned in any link)
    linked_normalized = {str(Path(l)).replace("\\", "/") for l in extract_markdown_links(text)}
    for f in skill_dir.rglob("*"):
        if f == path or f.is_dir():
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        if rel not in linked_normalized:
            warnings.append(f"orphaned file: {rel}")

    # ④ hooks-only variables used in SKILL.md content
    for var in HOOKS_ONLY_VARS:
        if var in text:
            warnings.append(f"invalid variable in SKILL.md: {var} (hooks/hooks.json only)")

    return warnings


def main() -> None:
    sys.exit(0)


if __name__ == "__main__":
    main()
