#!/usr/bin/env python3
"""Initialize a new Claude Code skill with proper structure."""

import argparse
from pathlib import Path

SKILL_TEMPLATE = '''---
name: {name}
description: TODO: Describe what this skill does. Use when [specific triggers].
---

# {title}

TODO: Add instructions here.

## Process

### 1. [First Step]

[Instructions]

### 2. [Second Step]

[Instructions]

## References

- [reference.md](references/reference.md) - Additional documentation
'''

REFERENCE_TEMPLATE = '''# Reference Documentation

Add detailed reference material here that Claude should load on-demand.
'''


def create_skill(name: str, output_path: Path) -> None:
    """Create skill directory structure."""
    skill_dir = output_path / name

    if skill_dir.exists():
        print(f"Error: {skill_dir} already exists")
        return

    # Create directories
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "references").mkdir()
    (skill_dir / "assets").mkdir()

    # Create SKILL.md
    title = name.replace("-", " ").title()
    (skill_dir / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, title=title)
    )

    # Create example reference
    (skill_dir / "references" / "reference.md").write_text(REFERENCE_TEMPLATE)

    # Create .gitkeep for empty dirs
    (skill_dir / "scripts" / ".gitkeep").touch()
    (skill_dir / "assets" / ".gitkeep").touch()

    print(f"Created skill at: {skill_dir}")
    print("\nNext steps:")
    print(f"  1. Edit {skill_dir}/SKILL.md")
    print("  2. Update the description with 'Use when...'")
    print("  3. Add instructions and references")
    print(f"  4. Run: python validate_skill.py {skill_dir}")


def main() -> None:
    """Entry point for skill initialization CLI."""
    parser = argparse.ArgumentParser(description="Initialize a new skill")
    parser.add_argument("name", help="Skill name (kebab-case)")
    parser.add_argument("--path", "-p", default=".claude/skills", help="Output directory (default: .claude/skills)")

    args = parser.parse_args()

    # Validate name
    if not args.name.replace("-", "").isalnum() or args.name != args.name.lower():
        print("Error: Name must be lowercase with hyphens only")
        return

    create_skill(args.name, Path(args.path))


if __name__ == "__main__":
    main()
