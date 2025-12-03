#!/usr/bin/env python3
"""Initialize a new Claude Code slash command with proper structure."""

import argparse
from pathlib import Path

COMMAND_TEMPLATE = '''---
name: {name}
description: TODO: Brief description of what this command does
arguments:
  - name: arg1
    description: First argument description
    required: true
  - name: arg2
    description: Optional argument description
    required: false
---

# {title}

TODO: Describe what this command does.

## Process

### 1. [First Step]

[Instructions]

### 2. [Second Step]

[Instructions]

## Example Usage

```
/{name} value1 value2
```
'''

COMMAND_TEMPLATE_NO_ARGS = '''---
name: {name}
description: TODO: Brief description of what this command does
---

# {title}

TODO: Describe what this command does.

## Process

### 1. [First Step]

[Instructions]

### 2. [Second Step]

[Instructions]

## Example Usage

```
/{name}
```
'''


def create_command(name: str, output_path: Path, with_args: bool = True) -> None:
    """Create a new slash command file."""
    command_file = output_path / f"{name}.md"

    if command_file.exists():
        print(f"Error: {command_file} already exists")
        return

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Create command file
    title = name.replace("-", " ").title()
    template = COMMAND_TEMPLATE if with_args else COMMAND_TEMPLATE_NO_ARGS
    command_file.write_text(template.format(name=name, title=title))

    print(f"Created command at: {command_file}")
    print("\nNext steps:")
    print(f"  1. Edit {command_file}")
    print("  2. Update the description")
    if with_args:
        print("  3. Define your arguments (or remove if not needed)")
    print("  4. Add step-by-step instructions")
    print(f"  5. Test with: /{name}")


def main() -> None:
    """Entry point for command initialization CLI."""
    parser = argparse.ArgumentParser(description="Initialize a new slash command")
    parser.add_argument("name", help="Command name (kebab-case)")
    parser.add_argument("--path", "-p", default=".claude/commands", help="Output directory (default: .claude/commands)")
    parser.add_argument("--no-args", action="store_true", help="Create command without argument template")

    args = parser.parse_args()

    # Validate name
    if not args.name.replace("-", "").isalnum() or args.name != args.name.lower():
        print("Error: Name must be lowercase with hyphens only")
        return

    create_command(args.name, Path(args.path), with_args=not args.no_args)


if __name__ == "__main__":
    main()
