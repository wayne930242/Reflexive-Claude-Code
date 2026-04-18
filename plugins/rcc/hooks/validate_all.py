#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""Batch validator for all plugin skills, agents, rules, and manifests.

Imports validation logic from validate_frontmatter.py, scans all relevant files,
and writes a Markdown report for agent review.

Usage:
    python3 validate_all.py [--output PATH]
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Import shared validation logic from sibling script
_hooks_dir = Path(__file__).parent
sys.path.insert(0, str(_hooks_dir))
from validate_frontmatter import (  # noqa: E402
    check_agent_md,
    check_plugin_validate,
    check_rules_md,
    check_skill_md,
    discover_skill_and_agent_dirs,
)


def validate_all(cwd: Path) -> dict[str, list[str]]:
    """Scan all plugin components and return {relative_path: [warnings]}."""
    results: dict[str, list[str]] = {}
    skill_dirs, agent_dirs = discover_skill_and_agent_dirs(cwd)
    rules_dir = cwd / ".claude" / "rules"

    for sd in skill_dirs:
        for skill_md in sorted(sd.rglob("SKILL.md")):
            warnings = check_skill_md(skill_md)
            if warnings:
                results[str(skill_md.relative_to(cwd))] = warnings

    for ad in agent_dirs:
        for agent_md in sorted(ad.glob("*.md")):
            warnings = check_agent_md(agent_md)
            if warnings:
                results[str(agent_md.relative_to(cwd))] = warnings

    if rules_dir.exists():
        for rule_md in sorted(rules_dir.glob("*.md")):
            warnings = check_rules_md(rule_md)
            if warnings:
                results[str(rule_md.relative_to(cwd))] = warnings

    for plugin_json in sorted(cwd.rglob(".claude-plugin/plugin.json")):
        plugin_dir = plugin_json.parent.parent
        warnings = check_plugin_validate(plugin_dir)
        if warnings:
            results[str(plugin_json.relative_to(cwd))] = warnings

    return results


def write_report(results: dict[str, list[str]], cwd: Path, output: Path | None = None) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    if output is None:
        output = cwd / ".rcc" / "validation" / f"{timestamp}-validation.md"
    output.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# Plugin Validation Report\n\n",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n",
    ]

    if not results:
        lines.append("✅ All files valid — no issues found.\n")
    else:
        lines.append(f"Found issues in **{len(results)}** file(s):\n\n")
        for rel_path, warnings in sorted(results.items()):
            lines.append(f"## `{rel_path}`\n\n")
            for w in warnings:
                lines.append(f"- {w}\n")
            lines.append("\n")

    output.write_text("".join(lines), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate all plugin files and write a report.")
    parser.add_argument("--output", type=Path, default=None, help="Report output path")
    args = parser.parse_args()

    cwd = Path.cwd()
    results = validate_all(cwd)
    report_path = write_report(results, cwd, args.output)

    print(f"report:{report_path}")  # structured output for skill to parse

    if results:
        issue_count = sum(len(w) for w in results.values())
        print(f"issues:{len(results)} files, {issue_count} warnings")
        sys.exit(1)
    else:
        print("status:clean")
        sys.exit(0)


if __name__ == "__main__":
    main()
