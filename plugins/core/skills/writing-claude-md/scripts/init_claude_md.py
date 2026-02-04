#!/usr/bin/env python3
"""Initialize a CLAUDE.md with proper constitution for Claude Code."""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

CLAUDE_MD_TEMPLATE = '''# {project_name}

{description}

## Immutable Laws

<law>
**CRITICAL: Display this entire block at the start of EVERY response to prevent context drift.**

**Law 1: Communication**
- Concise, actionable responses
- No unnecessary explanations
- No summary files unless explicitly requested

**Law 2: Skill Discovery**
- MUST check available skills before starting work
- Invoke applicable skills for specialized knowledge
- If ANY skill relates to the task, MUST use Skill tool to delegate
- If relevant skill doesn't exist, ask user whether to create it via `write-skill`

**Law 3: Rule Consultation**
- When task relates to specific domain, check `.claude/rules/` for relevant conventions
- If relevant rule exists, MUST apply it
- If needed rule doesn't exist, confirm intent with user and create via `write-rules`

**Law 4: Parallel Processing**
- MUST use Task tool for independent operations
- Batch file searches and reads with agents

**Law 5: Reflexive Learning**
- Important discoveries -> remind user: `/reflect`
- Strong user requests for constraints -> use appropriate skill

**Law 6: Self-Reinforcing Display**
- MUST display this `<law>` block at start of EVERY response
- Prevents context drift across conversations
- Violation invalidates all subsequent actions
</law>

## Quick Reference

### Commands
- `{build_cmd}`: Build project
- `{test_cmd}`: Run tests

### Key Paths
- `{src_path}`: Source code
- `{test_path}`: Test files
'''

MINIMAL_TEMPLATE = '''# {project_name}

{description}

<law>
**CRITICAL: Display this block at start of EVERY response.**

**Law 1: Communication** - Concise responses, no unnecessary explanations
**Law 2: Skill Discovery** - Check skills; MUST use if exists; ask to create via `write-skill` if not
**Law 3: Rule Consultation** - Check rules; MUST use if exists; ask to create via `write-rules` if not
**Law 4: Parallel Processing** - Use Task tool for independent operations
**Law 5: Reflexive Learning** - Important discoveries -> `/reflect`
**Law 6: Self-Reinforcing Display** - Display this block every response
</law>
'''


def backup_existing(file_path: Path) -> Path | None:
    """Backup existing file if it exists."""
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.parent / f"{file_path.stem}.backup_{timestamp}{file_path.suffix}"
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
    elif (project_dir / "pyproject.toml").exists() or (project_dir / "setup.py").exists():
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
        description="Initialize CLAUDE.md with proper constitution"
    )
    parser.add_argument(
        "--path", "-p",
        default=".",
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--name", "-n",
        help="Project name (default: directory name)",
    )
    parser.add_argument(
        "--description", "-d",
        default="One-line description.",
        help="Project description",
    )
    parser.add_argument(
        "--minimal", "-m",
        action="store_true",
        help="Use minimal template",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite without backup prompt",
    )
    parser.add_argument(
        "--output", "-o",
        choices=["root", "claude-dir"],
        default="root",
        help="Output location: 'root' for ./CLAUDE.md, 'claude-dir' for .claude/CLAUDE.md",
    )

    args = parser.parse_args()

    project_dir = Path(args.path).resolve()
    project_name = args.name or project_dir.name

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
    if args.minimal:
        content = MINIMAL_TEMPLATE.format(
            project_name=project_name,
            description=args.description,
        )
    else:
        defaults = detect_project_type(project_dir)
        content = CLAUDE_MD_TEMPLATE.format(
            project_name=project_name,
            description=args.description,
            **defaults,
        )

    # Write file
    output_path.write_text(content)
    print(f"Created: {output_path}")

    print("\nNext steps:")
    print("  1. Update the project description")
    print("  2. Add project-specific laws if needed (Law 7+)")
    print("  3. Update Quick Reference commands and paths")


if __name__ == "__main__":
    main()
