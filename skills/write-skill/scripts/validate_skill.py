#!/usr/bin/env python3
"""Validate a Claude Code skill structure and content."""

import argparse
import re
import sys
from pathlib import Path

ERRORS = []
WARNINGS = []


def error(msg: str) -> None:
    ERRORS.append(f"❌ {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(f"⚠️  {msg}")


def ok(msg: str) -> None:
    print(f"✅ {msg}")


def validate_structure(skill_dir: Path) -> None:
    """Validate skill directory structure."""
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        error(f"Not a directory: {skill_dir}")
        return

    if not skill_md.exists():
        error("SKILL.md not found")
        return

    ok(f"SKILL.md exists")


def validate_frontmatter(content: str) -> dict:
    """Validate YAML frontmatter."""
    if not content.startswith("---"):
        error("Missing YAML frontmatter (must start with ---)")
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        error("Invalid frontmatter format (missing closing ---)")
        return {}

    frontmatter = parts[1].strip()

    # Parse simple YAML
    data = {}
    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

    # Check required fields
    if "name" not in data:
        error("Missing required field: name")
    else:
        name = data["name"]
        if not re.match(r'^[a-z0-9-]+$', name):
            error(f"Invalid name '{name}': must be lowercase with hyphens")
        else:
            ok(f"name: {name}")

    if "description" not in data:
        error("Missing required field: description")
    else:
        desc = data["description"]
        if "use when" not in desc.lower():
            warn("Description should include 'Use when...' triggers")
        if len(desc) < 20:
            warn("Description seems too short")
        else:
            ok(f"description: {desc[:50]}...")

    return data


def validate_body(content: str) -> None:
    """Validate SKILL.md body."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return

    body = parts[2].strip()
    lines = body.split("\n")

    # Check length
    if len(lines) > 500:
        warn(f"Body has {len(lines)} lines (recommend < 500)")
    else:
        ok(f"Body length: {len(lines)} lines")

    # Check for common issues
    body_lower = body.lower()
    if "when to use this skill" in body_lower:
        warn("'When to use' should be in description, not body")

    # Check if skill actually contains these files (not just mentions them)
    skill_dir_from_content = Path(skill_dir) if 'skill_dir' in dir() else None


def validate_skill(skill_dir: Path) -> bool:
    """Run all validations."""
    print(f"\nValidating: {skill_dir}\n")

    validate_structure(skill_dir)
    if ERRORS:
        return False

    content = (skill_dir / "SKILL.md").read_text()
    validate_frontmatter(content)
    validate_body(content)

    # Print results
    print()
    for w in WARNINGS:
        print(w)
    for e in ERRORS:
        print(e)

    if ERRORS:
        print(f"\n❌ Validation failed with {len(ERRORS)} error(s)")
        return False
    elif WARNINGS:
        print(f"\n⚠️  Passed with {len(WARNINGS)} warning(s)")
        return True
    else:
        print(f"\n✅ Validation passed")
        return True


def main():
    parser = argparse.ArgumentParser(description="Validate a skill")
    parser.add_argument("path", help="Path to skill directory")

    args = parser.parse_args()
    success = validate_skill(Path(args.path))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
