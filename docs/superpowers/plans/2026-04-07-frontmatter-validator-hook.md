# Frontmatter Validator Hook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a PostToolUse plugin hook that validates SKILL.md, agent, and rule file frontmatter after editing, warning on extra fields, broken links, orphaned files, invalid variables, and plugin manifest errors.

**Architecture:** Single Python script (`validate_frontmatter.py`) reads edited file path from stdin JSON, discovers valid plugin/skill/agent paths dynamically from `.claude-plugin/plugin.json` files, runs type-appropriate checks, outputs `systemMessage` JSON if warnings exist. Registered via `hooks/hooks.json` in the rcc plugin.

**Tech Stack:** Python 3.11+ stdlib only (`re`, `json`, `pathlib`, `subprocess`); pytest for tests; uv run (fallback: python3).

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `plugins/rcc/.claude-plugin/plugin.json` | Modify | Add `"hooks"` field |
| `plugins/rcc/hooks/hooks.json` | Create | PostToolUse hook registration |
| `plugins/rcc/hooks/validate_frontmatter.py` | Create | Main validator script |
| `tests/hooks/test_validate_frontmatter.py` | Create | Unit + integration tests |
| `pyproject.toml` | Modify | Add pytest to dev deps |

---

## Task 1: Plugin Integration Files

**Files:**
- Modify: `plugins/rcc/.claude-plugin/plugin.json`
- Create: `plugins/rcc/hooks/hooks.json`

- [ ] **Step 1: Add hooks field to plugin.json**

Current content (read first to confirm):
```json
{
  "name": "rcc",
  ...
}
```

Add `"hooks": "./hooks/hooks.json"` field:
```json
{
  "name": "rcc",
  "description": "Core ACE workflow with TDD-based skills, task enforcement, and quality reviewers",
  "version": "9.0.0",
  "author": {
    "name": "Wei Hung",
    "email": "wayne930242@gmail.com"
  },
  "repository": "https://github.com/wayne930242/Reflexive-Claude-Code",
  "license": "MIT",
  "hooks": "./hooks/hooks.json",
  "keywords": [
    "claude-code",
    "plugin",
    "ACE",
    "agentic-context-engineering",
    "TDD",
    "task-driven",
    "skill-authoring"
  ]
}
```

- [ ] **Step 2: Create hooks/hooks.json**

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "uv run \"${CLAUDE_PLUGIN_ROOT}/hooks/validate_frontmatter.py\" 2>/dev/null || python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/validate_frontmatter.py\"",
          "timeout": 15
        }
      ]
    }
  ]
}
```

- [ ] **Step 3: Commit**

```bash
git add plugins/rcc/.claude-plugin/plugin.json plugins/rcc/hooks/hooks.json
git commit -m "feat(hooks): register frontmatter validator hook"
```

---

## Task 2: Test Infrastructure

**Files:**
- Modify: `pyproject.toml`
- Create: `tests/__init__.py`
- Create: `tests/hooks/__init__.py`
- Create: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Add pytest to dev deps in pyproject.toml**

Change the `dev` dependency group:
```toml
[dependency-groups]
dev = [
    "pylint>=4.0.4",
    "pytest>=8.0",
]
```

- [ ] **Step 2: Create empty init files**

Create `tests/__init__.py` (empty file).
Create `tests/hooks/__init__.py` (empty file).

- [ ] **Step 3: Create test file skeleton**

Create `tests/hooks/test_validate_frontmatter.py`:
```python
"""Tests for validate_frontmatter.py hook script."""
import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent.parent / "plugins/rcc/hooks/validate_frontmatter.py"


def run_hook(file_path: str, cwd: str) -> dict:
    """Run the hook script with given file_path and cwd, return parsed stdout."""
    stdin = json.dumps({
        "tool_input": {"file_path": file_path},
        "cwd": cwd
    })
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=stdin, capture_output=True, text=True
    )
    if result.stdout.strip():
        return json.loads(result.stdout)
    return {}
```

- [ ] **Step 4: Verify pytest discovers the file**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py --collect-only
```

Expected: `no tests ran` (file collected, no test functions yet).

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml tests/
git commit -m "test(hooks): add test infrastructure for frontmatter validator"
```

---

## Task 3: Frontmatter Parser

**Files:**
- Create: `plugins/rcc/hooks/validate_frontmatter.py` (initial skeleton)
- Modify: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Write failing tests for parse_frontmatter**

Append to `tests/hooks/test_validate_frontmatter.py`:
```python
import importlib.util, types

def _load_module() -> types.ModuleType:
    """Load validate_frontmatter as a module without executing main()."""
    spec = importlib.util.spec_from_file_location("validate_frontmatter", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_parse_frontmatter_returns_fields():
    mod = _load_module()
    text = "---\nname: my-skill\ndescription: does stuff\n---\n\n# Body"
    result = mod.parse_frontmatter(text)
    assert result == {"name": "my-skill", "description": "does stuff"}

def test_parse_frontmatter_no_frontmatter_returns_none():
    mod = _load_module()
    assert mod.parse_frontmatter("# No frontmatter here") is None

def test_parse_frontmatter_empty_block_returns_empty_dict():
    mod = _load_module()
    assert mod.parse_frontmatter("---\n---\n") == {}
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: FAIL — `ModuleNotFoundError` or `AttributeError` (script doesn't exist yet).

- [ ] **Step 3: Create validate_frontmatter.py with PEP 723 header and parse_frontmatter**

Create `plugins/rcc/hooks/validate_frontmatter.py`:
```python
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


def main() -> None:
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/rcc/hooks/validate_frontmatter.py tests/hooks/test_validate_frontmatter.py
git commit -m "feat(hooks): add frontmatter parser"
```

---

## Task 4: Markdown Link Extraction + SKILL.md Checks ①②③④

**Files:**
- Modify: `plugins/rcc/hooks/validate_frontmatter.py`
- Modify: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/hooks/test_validate_frontmatter.py`:
```python
def test_extract_markdown_links_relative_only():
    mod = _load_module()
    text = "[foo](references/foo.md) [bar](https://example.com) [baz](./scripts/run.sh)"
    result = mod.extract_markdown_links(text)
    assert "references/foo.md" in result
    assert "https://example.com" not in result
    assert "./scripts/run.sh" in result

def test_check_skill_md_extra_field_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ntags: foo\n---\n# Body\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("tags" in w for w in warnings)

def test_check_skill_md_allowed_fields_no_warn(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: Use when x.\n---\n# Body\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("extra frontmatter" in w for w in warnings)

def test_check_skill_md_broken_link_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    content = "---\nname: x\ndescription: y\n---\n\n[ref](references/missing.md)\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("missing.md" in w for w in warnings)

def test_check_skill_md_valid_link_no_warn(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "real.md").write_text("# Real")
    content = "---\nname: x\ndescription: y\n---\n\n[ref](references/real.md)\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert not any("broken link" in w for w in warnings)

def test_check_skill_md_orphaned_file_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True)
    (ref_dir / "orphan.md").write_text("# Orphan")
    (skill_dir / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\n# No links\n")
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("orphan.md" in w for w in warnings)

def test_check_skill_md_hooks_only_var_warns(tmp_path):
    mod = _load_module()
    skill_dir = tmp_path / "my-skill"
    skill_dir.mkdir()
    content = "---\nname: x\ndescription: y\n---\n\nUse ${CLAUDE_PLUGIN_ROOT}/data here.\n"
    (skill_dir / "SKILL.md").write_text(content)
    warnings = mod.check_skill_md(skill_dir / "SKILL.md")
    assert any("CLAUDE_PLUGIN_ROOT" in w for w in warnings)
```

- [ ] **Step 2: Run to confirm failures**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: new tests FAIL — `AttributeError: module has no attribute 'extract_markdown_links'`.

- [ ] **Step 3: Implement extract_markdown_links and check_skill_md**

Add to `validate_frontmatter.py` (before `main()`):
```python
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
    linked = set(extract_markdown_links(text))
    for f in skill_dir.rglob("*"):
        if f == path or f.is_dir():
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        if rel not in linked:
            warnings.append(f"orphaned file: {rel}")

    # ④ hooks-only variables used in SKILL.md content
    for var in HOOKS_ONLY_VARS:
        if var in text:
            warnings.append(f"invalid variable in SKILL.md: {var} (hooks/hooks.json only)")

    return warnings
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/rcc/hooks/validate_frontmatter.py tests/hooks/test_validate_frontmatter.py
git commit -m "feat(hooks): implement SKILL.md checks ①②③④"
```

---

## Task 5: Agent and Rules Checks

**Files:**
- Modify: `plugins/rcc/hooks/validate_frontmatter.py`
- Modify: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/hooks/test_validate_frontmatter.py`:
```python
def test_check_agent_md_extra_field_warns(tmp_path):
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: inherit\ncontext: fork\ntools: []\ntags: bad\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert any("tags" in w for w in warnings)

def test_check_agent_md_allowed_fields_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-agent.md").write_text("---\nname: my-agent\ndescription: x\nmodel: inherit\ncontext: fork\ntools: []\n---\n")
    warnings = mod.check_agent_md(tmp_path / "my-agent.md")
    assert warnings == []

def test_check_rules_md_extra_field_warns(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("---\npaths: src/**\ntags: bad\n---\n# Rule\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert any("tags" in w for w in warnings)

def test_check_rules_md_paths_only_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("---\npaths: src/**\n---\n# Rule\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert warnings == []

def test_check_rules_md_no_frontmatter_no_warn(tmp_path):
    mod = _load_module()
    (tmp_path / "my-rule.md").write_text("# Rule without frontmatter\n")
    warnings = mod.check_rules_md(tmp_path / "my-rule.md")
    assert warnings == []
```

- [ ] **Step 2: Run to confirm failures**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: new tests FAIL — `AttributeError: no attribute 'check_agent_md'`.

- [ ] **Step 3: Implement check_agent_md and check_rules_md**

Add to `validate_frontmatter.py` (before `main()`):
```python
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
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/rcc/hooks/validate_frontmatter.py tests/hooks/test_validate_frontmatter.py
git commit -m "feat(hooks): implement agent and rules frontmatter checks"
```

---

## Task 6: File Discovery

**Files:**
- Modify: `plugins/rcc/hooks/validate_frontmatter.py`
- Modify: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Write failing tests**

Append to `tests/hooks/test_validate_frontmatter.py`:
```python
def test_discover_finds_plugin_skills_dir(tmp_path):
    mod = _load_module()
    # Scaffold a minimal plugin
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    (plugin_dir / "skills").mkdir()
    skill_dirs, agent_dirs = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "skills" in skill_dirs

def test_discover_respects_custom_skills_field(tmp_path):
    mod = _load_module()
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x","skills":"custom-skills"}')
    (plugin_dir / "custom-skills").mkdir()
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "custom-skills" in skill_dirs

def test_discover_includes_claude_skills(tmp_path):
    mod = _load_module()
    (tmp_path / ".claude" / "skills").mkdir(parents=True)
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert tmp_path / ".claude" / "skills" in skill_dirs

def test_discover_skips_nonexistent_dirs(tmp_path):
    mod = _load_module()
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    # skills/ does NOT exist
    skill_dirs, _ = mod.discover_skill_and_agent_dirs(tmp_path)
    assert plugin_dir / "skills" not in skill_dirs
```

- [ ] **Step 2: Run to confirm failures**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: new tests FAIL.

- [ ] **Step 3: Implement discover_skill_and_agent_dirs**

Add to `validate_frontmatter.py` (before `main()`):
```python
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
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/rcc/hooks/validate_frontmatter.py tests/hooks/test_validate_frontmatter.py
git commit -m "feat(hooks): implement plugin root discovery"
```

---

## Task 7: Main Entry Point + Plugin Validate

**Files:**
- Modify: `plugins/rcc/hooks/validate_frontmatter.py`
- Modify: `tests/hooks/test_validate_frontmatter.py`

- [ ] **Step 1: Write failing integration tests**

Append to `tests/hooks/test_validate_frontmatter.py`:
```python
def test_hook_silent_on_unrelated_file(tmp_path):
    """Files outside plugin paths produce no output."""
    (tmp_path / "random.md").write_text("---\ntags: foo\n---\n# hi\n")
    result = run_hook(str(tmp_path / "random.md"), str(tmp_path))
    assert result == {}

def test_hook_warns_on_skill_extra_field(tmp_path):
    """SKILL.md with extra frontmatter field triggers systemMessage."""
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    skill_dir = plugin_dir / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: x\ntags: bad\n---\n# Body\n")
    result = run_hook(str(skill_dir / "SKILL.md"), str(tmp_path))
    assert "systemMessage" in result
    assert "tags" in result["systemMessage"]

def test_hook_silent_on_valid_skill(tmp_path):
    """Valid SKILL.md produces no output."""
    plugin_dir = tmp_path / "my-plugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name":"x"}')
    skill_dir = plugin_dir / "skills" / "my-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: my-skill\ndescription: x\n---\n# Body\n")
    result = run_hook(str(skill_dir / "SKILL.md"), str(tmp_path))
    assert result == {}
```

- [ ] **Step 2: Run to confirm failures**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: integration tests FAIL — `main()` is a no-op.

- [ ] **Step 3: Implement check_plugin_validate and main()**

Replace the existing `main()` in `validate_frontmatter.py`:
```python
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

    sys.exit(0)
```

- [ ] **Step 4: Run all tests**

```bash
uv run pytest tests/hooks/test_validate_frontmatter.py -v
```

Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/rcc/hooks/validate_frontmatter.py tests/hooks/test_validate_frontmatter.py
git commit -m "feat(hooks): wire main entry point and plugin validate check"
```

---

## Task 8: End-to-End Test in This Project

Verify the hook works against the actual project files (this project has both plugin skills and general skills).

- [ ] **Step 1: Test against a real SKILL.md**

```bash
echo '{"tool_input":{"file_path":"plugins/rcc/skills/writing-skills/SKILL.md"},"cwd":"'$(pwd)'"}' \
  | python3 plugins/rcc/hooks/validate_frontmatter.py
```

Expected: empty output (no warnings — valid file).

- [ ] **Step 2: Test against a real agent file**

```bash
echo '{"tool_input":{"file_path":"plugins/rcc/agents/skill-reviewer.md"},"cwd":"'$(pwd)'"}' \
  | python3 plugins/rcc/hooks/validate_frontmatter.py
```

Expected: empty output.

- [ ] **Step 3: Test with an injected extra field (temp edit)**

Temporarily add `tags: test` to `plugins/rcc/agents/skill-reviewer.md` frontmatter, run:

```bash
echo '{"tool_input":{"file_path":"plugins/rcc/agents/skill-reviewer.md"},"cwd":"'$(pwd)'"}' \
  | python3 plugins/rcc/hooks/validate_frontmatter.py
```

Expected: `systemMessage` containing `extra frontmatter field: "tags"`.

Then revert the temp edit.

- [ ] **Step 4: Test unrelated file produces no output**

```bash
echo '{"tool_input":{"file_path":"README.md"},"cwd":"'$(pwd)'"}' \
  | python3 plugins/rcc/hooks/validate_frontmatter.py
```

Expected: empty output.

- [ ] **Step 5: Run full test suite**

```bash
uv run pytest tests/ -v
```

Expected: all PASS.

- [ ] **Step 6: Final commit**

```bash
git add .
git commit -m "feat(hooks): frontmatter validator hook — complete implementation"
```
