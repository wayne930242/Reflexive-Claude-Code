#!/usr/bin/env python3
"""Initialize base constitution rules for a Claude Code project."""

import argparse
from pathlib import Path

CONSTITUTION_CONTENT = """---
# No paths = global, auto-injected
---

# Core Laws

## Communication
- Concise, actionable responses
- No unnecessary explanations
- No summary files unless explicitly requested

## Skill Discovery
- MUST check available skills before starting work
- Invoke applicable skills for specialized knowledge

## Parallel Processing
- MUST use Task tool for independent operations
- Batch file searches and reads with agents

## Reflexive Learning
- Important discoveries → remind user: `/reflect`
- Strong user requests for constraints → use `write-rules` skill
"""


def init_constitution(output_dir: str = ".claude/rules") -> None:
    """Create the base constitution file."""
    rules_path = Path(output_dir)
    rules_path.mkdir(parents=True, exist_ok=True)

    constitution_file = rules_path / "00-constitution.md"

    if constitution_file.exists():
        print(f"Constitution already exists: {constitution_file}")
        print("Use --force to overwrite")
        return

    constitution_file.write_text(CONSTITUTION_CONTENT.strip() + "\n")
    print(f"Created: {constitution_file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize base constitution rules")
    parser.add_argument(
        "-p",
        "--path",
        default=".claude/rules",
        help="Output directory (default: .claude/rules)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing constitution"
    )

    args = parser.parse_args()

    rules_path = Path(args.path)
    rules_path.mkdir(parents=True, exist_ok=True)

    constitution_file = rules_path / "00-constitution.md"

    if constitution_file.exists() and not args.force:
        print(f"Constitution already exists: {constitution_file}")
        print("Use --force to overwrite")
        return

    constitution_file.write_text(CONSTITUTION_CONTENT.strip() + "\n")
    print(f"Created: {constitution_file}")


if __name__ == "__main__":
    main()
