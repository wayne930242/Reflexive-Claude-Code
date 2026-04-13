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

- Use `"python3"` or `"python"` — Windows may only have `python`
- Safe pattern: `"command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/check.py\" || python \"$CLAUDE_PROJECT_DIR/.claude/hooks/check.py\""`
- `$CLAUDE_PROJECT_DIR` works on all platforms (Claude Code resolves it)

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
