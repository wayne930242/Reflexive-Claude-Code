# Cross-Platform Script Writing

Rules for writing Python scripts that work on macOS, Linux, AND Windows.
Applies to hook scripts, skill-bundled scripts, and plugin bin/ executables.

## Paths

- Use `pathlib.Path` for ALL path operations — never string concatenation with `/`
- Never hardcode `/` or `\` as separators
- Use `Path(file_path).resolve()` to normalize paths
- Shebangs (`#!/usr/bin/env python3`) are ignored on Windows — harmless, keep them

## Shell Commands

- Wrap external commands with `shutil.which()` to locate binaries
- Use `subprocess.run()` with list args, not shell strings:
  ```python
  # Good
  subprocess.run(["npx", "eslint", str(path)])
  # Bad
  subprocess.run(f"npx eslint {path}", shell=True)
  ```
- If `shell=True` is unavoidable, detect platform: `subprocess.run(cmd, shell=True)` uses `cmd.exe` on Windows, not bash

## Command Paths in settings.json

**Shell assumption: bash-first.** Targets Git Bash on Windows, WSL, macOS, Linux. POSIX syntax (`command -v`, `>/dev/null`, `&&`, `||`) is allowed. cmd.exe is NOT a target.

### Three-runner fallback (standard template)

```bash
{ command -v uv >/dev/null 2>&1 && uv run "<SCRIPT>"; } \
  || { python3 --version >/dev/null 2>&1 && python3 "<SCRIPT>"; } \
  || { command -v python >/dev/null 2>&1 && python "<SCRIPT>"; } \
  || echo '<json fallback warning>'
```

Priority: **uv → python3 → python → warning**. Reasons:
- `uv` is fastest, handles inline deps (PEP 723), avoids env pollution
- `python3` second for POSIX-clean systems
- `python` third for Windows where `python3` is often missing

**Why braces `{ ... }` are mandatory:** Bash chains `A && B || C && D` are left-associative with **equal precedence**, so a successful `A && B` does NOT short-circuit the trailing `&& D` — it evaluates as `(((A && B) || C) && D)`. Without grouping, even when `uv run` succeeds, bash still drops into `python3` and `python` branches afterward. Grouping each runner with `{ ...; }` makes each branch an atomic exit-code unit so `||` short-circuits correctly.

### Windows `python3` Microsoft Store stub trap

On Windows, `command -v python3` may match a Microsoft Store *redirect stub* — the binary exists but executing it pops up an installer prompt and fails. **Always probe with `python3 --version` (actual execution), not `command -v python3`.** This is why the standard template above uses `--version` for python3 specifically.

### Path resolution

- `${CLAUDE_PROJECT_DIR}` and `${CLAUDE_PLUGIN_ROOT}` work on all platforms — Claude Code resolves them before shell expansion.
- Quote script paths: `"${CLAUDE_PLUGIN_ROOT}/hooks/x.py"` (handles spaces in user home).

## Line Endings

- Use `open(path, 'r', newline='')` when reading files to handle `\r\n`
- Or `.read().replace('\r\n', '\n')` to normalize

## Common Pitfalls

- `chmod +x` does nothing on Windows — Python scripts don't need it there
- `os.sep` in regex patterns — escape properly or use `pathlib`
- Temp file paths — use `tempfile.mkstemp()` not hardcoded `/tmp/`

## PowerShell Support

- Set `shell: powershell` in SKILL.md frontmatter for PowerShell-based skills
- User must set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`
- Ask the user which shell they use if the plugin needs cross-platform support

## Verification Checklist

- [ ] Uses `pathlib.Path` for all path operations
- [ ] No `shell=True` with string commands (use list args)
- [ ] No hardcoded `/tmp/` or path separators
- [ ] `shutil.which()` used to locate external binaries
- [ ] Line endings handled (`newline=''` or normalize)
