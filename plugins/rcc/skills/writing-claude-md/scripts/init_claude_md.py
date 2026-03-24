#!/usr/bin/env python3
"""Initialize a CLAUDE.md with project-specific instructions for Claude Code."""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

CLAUDE_MD_TEMPLATE = """# {project_name}

{description}

## Code Style

- [Add project-specific style rules that differ from defaults]
- [Example: MUST use ES modules (import/export), NOT CommonJS (require)]

## Workflow

- Build: `{build_cmd}`
- Test: `{test_cmd}`
- [Add project-specific workflow instructions]

## Architecture

- `{src_path}` — Source code
- `{test_path}` — Test files
- [Add key directories and their purpose]

## Gotchas

- [Add non-obvious behavior, environment quirks]
- [Example: Dev server must restart after changing auth config]
"""

MINIMAL_TEMPLATE = """# {project_name}

{description}

## Workflow

- Build: `{build_cmd}`
- Test: `{test_cmd}`
"""


def backup_existing(file_path: Path) -> Path | None:
    """Backup existing file if it exists."""
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = (
        file_path.parent / f"{file_path.stem}.backup_{timestamp}{file_path.suffix}"
    )
    shutil.copy2(file_path, backup_path)
    return backup_path


def detect_project_type(project_dir: Path) -> dict:
    """Detect project type and return default values."""
    defaults = {
        "build_cmd": "make build",
        "test_cmd": "make test",
        "src_path": "src/",
        "test_path": "tests/",
    }

    # Node.js project
    if (project_dir / "package.json").exists():
        defaults["build_cmd"] = "npm run build"
        defaults["test_cmd"] = "npm test"

    # Python project
    elif (project_dir / "pyproject.toml").exists() or (
        project_dir / "setup.py"
    ).exists():
        defaults["build_cmd"] = "python -m build"
        defaults["test_cmd"] = "pytest"

    # Rust project
    elif (project_dir / "Cargo.toml").exists():
        defaults["build_cmd"] = "cargo build"
        defaults["test_cmd"] = "cargo test"

    # Go project
    elif (project_dir / "go.mod").exists():
        defaults["build_cmd"] = "go build ./..."
        defaults["test_cmd"] = "go test ./..."

    return defaults


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize CLAUDE.md with project-specific instructions"
    )
    parser.add_argument(
        "--path",
        "-p",
        default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--name",
        "-n",
        help="Project name (default: directory name)",
    )
    parser.add_argument(
        "--description",
        "-d",
        default="One-line description.",
        help="Project description",
    )
    parser.add_argument(
        "--minimal",
        "-m",
        action="store_true",
        help="Use minimal template",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite without backup prompt",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=["root", "claude-dir"],
        default="root",
        help="Output location: 'root' for ./CLAUDE.md, 'claude-dir' for .claude/CLAUDE.md",
    )

    args = parser.parse_args()

    project_dir = Path(args.path).resolve()
    project_name = args.name or project_dir.name
    defaults = detect_project_type(project_dir)

    # Determine output path
    if args.output == "claude-dir":
        claude_dir = project_dir / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)
        output_path = claude_dir / "CLAUDE.md"
    else:
        output_path = project_dir / "CLAUDE.md"

    # Backup existing file
    if output_path.exists():
        backup_path = backup_existing(output_path)
        if backup_path:
            print(f"Backed up existing file to: {backup_path}")

    # Generate content
    template = MINIMAL_TEMPLATE if args.minimal else CLAUDE_MD_TEMPLATE
    content = template.format(
        project_name=project_name,
        description=args.description,
        **defaults,
    )

    # Write file
    output_path.write_text(content)
    print(f"Created: {output_path}")

    print("\nNext steps:")
    print("  1. Replace placeholder instructions with project-specific ones")
    print("  2. Remove any sections not needed")
    print("  3. Keep it under 200 lines — move details to rules or skills")


if __name__ == "__main__":
    main()
