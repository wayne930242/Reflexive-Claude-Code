#!/usr/bin/env python3
"""
Claude Code Plugin Health Check

Validates a plugin directory against official Claude Code best practices.
Integrates with `claude plugin validate` when available, then runs extended checks.

Usage:
    python validate_plugin.py <plugin-directory>
    uv run validate_plugin.py <plugin-directory>

Exit codes:
    0 = pass
    1 = fail (errors found)
"""
# /// script
# requires-python = ">=3.10"
# ///

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ERRORS: list[str] = []
WARNINGS: list[str] = []
INFOS: list[str] = []


def error(msg: str) -> None:
    ERRORS.append(msg)
    print(f"  \u274c {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  \u26a0\ufe0f  {msg}")


def info(msg: str) -> None:
    INFOS.append(msg)
    print(f"  \u2139\ufe0f  {msg}")


def ok(msg: str) -> None:
    print(f"  \u2705 {msg}")


# ============================================================
# 0. Official CLI validation
# ============================================================
def run_official_validate(plugin_dir: Path) -> None:
    """Run `claude plugin validate` if the CLI is available."""
    print("\n--- Official CLI Validation ---")

    claude_bin = shutil.which("claude")
    if not claude_bin:
        info("claude CLI not found in PATH, skipping official validation")
        return

    try:
        result = subprocess.run(
            [claude_bin, "plugin", "validate", str(plugin_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            ok("claude plugin validate passed")
        else:
            error(f"claude plugin validate failed:\n{result.stderr or result.stdout}")

        # Print output for visibility
        output = (result.stdout or "").strip()
        if output:
            for line in output.split("\n"):
                print(f"    {line}")

    except subprocess.TimeoutExpired:
        warn("claude plugin validate timed out (30s)")
    except FileNotFoundError:
        info("claude CLI not executable, skipping official validation")
    except Exception as e:
        warn(f"claude plugin validate error: {e}")


# ============================================================
# 1. Manifest validation
# ============================================================
def validate_manifest(plugin_dir: Path) -> dict:
    """Validate .claude-plugin/plugin.json."""
    print("\n--- Manifest ---")
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"

    if not manifest_path.exists():
        error("Missing .claude-plugin/plugin.json")
        return {}

    ok("plugin.json exists")

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        error(f"plugin.json is not valid JSON: {e}")
        return {}

    ok("Valid JSON syntax")

    # Required: name
    name = data.get("name", "")
    if not name:
        error("Missing required field: name")
    elif not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        error(f"Invalid name '{name}': must be lowercase kebab-case")
    else:
        ok(f"name: {name}")

    reserved = {"helper", "utils", "anthropic", "claude"}
    if name.lower() in reserved:
        warn(f"Name '{name}' uses reserved word")

    # Recommended: description, version
    for field in ("description", "version"):
        val = data.get(field)
        if not val:
            warn(f"Missing recommended field: {field}")
        else:
            ok(f"{field}: {val}")

    # Version format
    version = data.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+", version):
        warn(f"Version '{version}' does not follow semver (MAJOR.MINOR.PATCH)")

    # Optional fields
    for field in ("author", "license", "keywords"):
        if not data.get(field):
            info(f"Optional field missing: {field}")

    return data


# ============================================================
# 2. Directory structure
# ============================================================
def validate_structure(plugin_dir: Path) -> None:
    """Validate plugin directory structure."""
    print("\n--- Directory Structure ---")

    # Anti-pattern: components inside .claude-plugin/
    claude_plugin_dir = plugin_dir / ".claude-plugin"
    for dirname in ("commands", "agents", "skills", "hooks"):
        bad_path = claude_plugin_dir / dirname
        if bad_path.exists():
            error(f"{dirname}/ found inside .claude-plugin/ \u2014 must be at plugin root")

    # Component directories at root
    component_count = 0
    for dirname in ("skills", "commands", "agents"):
        comp_dir = plugin_dir / dirname
        if comp_dir.is_dir():
            items = [p for p in comp_dir.iterdir() if p.is_dir() or p.suffix == ".md"]
            count = len(items)
            ok(f"{dirname}/ exists ({count} items)")
            component_count += count

    if component_count == 0:
        warn("No component directories found (skills/, commands/, agents/)")

    # README
    if (plugin_dir / "README.md").exists():
        ok("README.md exists")
    else:
        warn("Missing README.md")


# ============================================================
# 3. Skills validation
# ============================================================
def validate_skills(plugin_dir: Path) -> None:
    """Validate all skills in the plugin."""
    print("\n--- Skills ---")
    skills_dir = plugin_dir / "skills"

    if not skills_dir.is_dir():
        info("No skills/ directory")
        return

    skill_dirs = [p for p in skills_dir.iterdir() if p.is_dir()]
    if not skill_dirs:
        info("No skills found")
        return

    descriptions: list[tuple[str, str]] = []

    for sd in sorted(skill_dirs):
        sname = sd.name
        skill_md = sd / "SKILL.md"

        if not skill_md.exists():
            error(f"Skill '{sname}' missing SKILL.md")
            continue

        # Gerund naming
        if not re.search(r"(ing$|ing-)", sname):
            warn(f"Skill '{sname}' does not use gerund form (verb+-ing)")

        content = skill_md.read_text(encoding="utf-8")

        # Frontmatter check
        if not content.startswith("---"):
            error(f"Skill '{sname}': missing YAML frontmatter")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            error(f"Skill '{sname}': invalid frontmatter format")
            continue

        # Parse frontmatter
        fm = {}
        for line in parts[1].strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                fm[key.strip()] = val.strip().strip('"').strip("'")

        desc = fm.get("description", "")
        if desc:
            descriptions.append((sname, desc))
            if "use when" not in desc.lower():
                warn(f"Skill '{sname}': description missing 'Use when' triggers")
        else:
            warn(f"Skill '{sname}': missing description in frontmatter")

        # Line count
        lines = len(content.split("\n"))
        if lines > 300:
            warn(f"Skill '{sname}': {lines} lines (recommend < 300, use references/)")

        # Mandatory sections
        body = parts[2] if len(parts) > 2 else ""
        body_lower = body.lower()
        for section in ("task initialization", "red flags", "rationalizations", "flowchart"):
            if section not in body_lower:
                warn(f"Skill '{sname}': missing '{section}' section")

        ok(f"Skill '{sname}': valid ({lines} lines)")

    # Cross-skill: trigger overlap detection
    if len(descriptions) > 1:
        _check_trigger_overlap(descriptions)


def _check_trigger_overlap(descriptions: list[tuple[str, str]]) -> None:
    """Check for overlapping triggers between skills."""
    for i, (name_a, desc_a) in enumerate(descriptions):
        for name_b, desc_b in descriptions[i + 1 :]:
            # Simple heuristic: check if trigger phrases overlap significantly
            words_a = set(desc_a.lower().split()) - {"use", "when", "the", "a", "an", "or", "and", "to", "is", "for", "in", "of"}
            words_b = set(desc_b.lower().split()) - {"use", "when", "the", "a", "an", "or", "and", "to", "is", "for", "in", "of"}
            overlap = words_a & words_b
            ratio = len(overlap) / min(len(words_a), len(words_b)) if words_a and words_b else 0
            if ratio > 0.7:
                warn(f"Possible trigger overlap between '{name_a}' and '{name_b}'")


# ============================================================
# 4. Commands validation
# ============================================================
def validate_commands(plugin_dir: Path) -> None:
    """Validate command files."""
    print("\n--- Commands ---")
    cmds_dir = plugin_dir / "commands"

    if not cmds_dir.is_dir():
        info("No commands/ directory")
        return

    cmd_files = list(cmds_dir.glob("*.md"))
    if not cmd_files:
        info("No commands found")
        return

    for cf in sorted(cmd_files):
        cname = cf.stem
        content = cf.read_text(encoding="utf-8")

        if not content.startswith("---"):
            warn(f"Command '{cname}': missing YAML frontmatter")
        else:
            ok(f"Command '{cname}': valid")

        # Check for orphan commands (references non-existent skill)
        if "invoke" in content.lower() or "skill" in content.lower():
            # Try to find referenced skill name
            for line in content.split("\n"):
                match = re.search(r"rcc:(\S+)", line)
                if match:
                    skill_name = match.group(1)
                    skill_path = plugin_dir / "skills" / skill_name / "SKILL.md"
                    if not skill_path.exists():
                        warn(f"Command '{cname}' references skill '{skill_name}' which was not found locally")


# ============================================================
# 5. Agents validation
# ============================================================
def validate_agents(plugin_dir: Path) -> None:
    """Validate agent files."""
    print("\n--- Agents ---")
    agents_dir = plugin_dir / "agents"

    if not agents_dir.is_dir():
        info("No agents/ directory")
        return

    agent_files = list(agents_dir.glob("*.md"))
    if not agent_files:
        info("No agents found")
        return

    for af in sorted(agent_files):
        aname = af.stem
        content = af.read_text(encoding="utf-8")

        if "context:" not in content:
            warn(f"Agent '{aname}': missing context isolation (recommend context: fork)")

        if "tools:" not in content:
            warn(f"Agent '{aname}': missing tools specification")

        ok(f"Agent '{aname}': valid")


# ============================================================
# 6. Path safety
# ============================================================
def validate_paths(plugin_dir: Path) -> None:
    """Check for absolute paths in configuration files."""
    print("\n--- Path Safety ---")

    config_files = list((plugin_dir / ".claude-plugin").glob("*.json"))
    found_abs = False

    for cf in config_files:
        content = cf.read_text(encoding="utf-8")
        # Find absolute paths (not URLs)
        for i, line in enumerate(content.split("\n"), 1):
            # Skip comment lines and URLs
            stripped = line.strip()
            if stripped.startswith("//") or "http://" in line or "https://" in line:
                continue
            # Check for absolute paths like /Users/, /home/, C:\, etc.
            if re.search(r'["\']/(Users|home|opt|usr|var|tmp)/', line) or re.search(r'["\'][A-Z]:\\', line):
                warn(f"Absolute path in {cf.name}:{i}: {stripped}")
                found_abs = True

    if not found_abs:
        ok("No absolute paths in config")


# ============================================================
# 7. Version sync
# ============================================================
def validate_version_sync(plugin_dir: Path, manifest_data: dict) -> None:
    """Check version sync with marketplace.json."""
    print("\n--- Version Sync ---")

    plugin_name = manifest_data.get("name", "")
    plugin_ver = manifest_data.get("version", "")

    if not plugin_ver:
        info("No version in plugin.json, skipping sync check")
        return

    # Search for marketplace.json in parent directories
    marketplace_path = None
    check_dir = plugin_dir
    for _ in range(4):
        check_dir = check_dir.parent
        candidate = check_dir / ".claude-plugin" / "marketplace.json"
        if candidate.exists():
            marketplace_path = candidate
            break

    if not marketplace_path:
        info("No marketplace.json found for version sync check")
        return

    try:
        market_data = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        warn("marketplace.json exists but is not readable/valid")
        return

    # Check plugin entry version
    for p in market_data.get("plugins", []):
        if p.get("name") == plugin_name:
            market_ver = p.get("version", "")
            if market_ver and market_ver != plugin_ver:
                error(f"Version mismatch: plugin.json ({plugin_ver}) != marketplace ({market_ver})")
            elif market_ver:
                ok(f"Version sync: plugin.json ({plugin_ver}) = marketplace ({market_ver})")
            break

    # Check metadata version
    meta_ver = market_data.get("metadata", {}).get("version", "")
    if meta_ver and meta_ver != plugin_ver:
        info(f"Marketplace metadata version ({meta_ver}) differs from plugin ({plugin_ver})")


# ============================================================
# Main
# ============================================================
def validate_plugin(plugin_dir: Path) -> bool:
    """Run all validations on a plugin directory."""
    print(f"\n{'=' * 50}")
    print(f"Plugin Health Check: {plugin_dir.name}")
    print(f"Path: {plugin_dir}")
    print(f"{'=' * 50}")

    if not plugin_dir.is_dir():
        error(f"Not a directory: {plugin_dir}")
        return False

    # 0. Official CLI validation
    run_official_validate(plugin_dir)

    # 1. Manifest
    manifest_data = validate_manifest(plugin_dir)

    # 2. Structure
    validate_structure(plugin_dir)

    # 3. Skills
    validate_skills(plugin_dir)

    # 4. Commands
    validate_commands(plugin_dir)

    # 5. Agents
    validate_agents(plugin_dir)

    # 6. Path safety
    validate_paths(plugin_dir)

    # 7. Version sync
    if manifest_data:
        validate_version_sync(plugin_dir, manifest_data)

    # Summary
    print(f"\n{'=' * 50}")
    print("Summary")
    print(f"{'=' * 50}")
    print(f"  Errors:   {len(ERRORS)}")
    print(f"  Warnings: {len(WARNINGS)}")
    print(f"  Info:     {len(INFOS)}")
    print()

    if ERRORS:
        print(f"\u274c Health check FAILED with {len(ERRORS)} error(s)")
        return False
    elif WARNINGS:
        print(f"\u26a0\ufe0f  Health check PASSED with {len(WARNINGS)} warning(s)")
        return True
    else:
        print("\u2705 Health check PASSED")
        return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Claude Code Plugin Health Check",
        epilog="Validates plugin structure against official best practices.",
    )
    parser.add_argument("path", help="Path to plugin directory")

    args = parser.parse_args()
    plugin_path = Path(args.path).resolve()

    success = validate_plugin(plugin_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
