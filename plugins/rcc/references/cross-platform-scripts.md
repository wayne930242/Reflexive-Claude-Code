# Cross-Platform Script Writing

Rules for writing Python scripts that work on macOS, Linux, AND Windows.
Applies to hook scripts, skill-bundled scripts, and plugin bin/ executables.

## Paths

- Use `pathlib.Path` for ALL path operations — never string concatenation with `/`
- Never hardcode `/` or `\` as separators
- Use `Path(file_path).resolve()` to normalize paths
- Never hardcode `$HOME`, `~`, `%USERPROFILE%`, or `$env:USERPROFILE` — use `Path.home()` to resolve the user's home directory portably
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

## Exec Form vs Shell Form (hook `command`)

Per the official hooks spec, a hook's `command` runs one of two ways:

- **Shell form** (no `args` key) — the `command` string is passed to a shell: `sh -c` on macOS/Linux, Git Bash on Windows if installed, otherwise **PowerShell**. The shell tokenizes the string and interprets `&&`, `||`, pipes, and quoting.
- **Exec form** (`args` key present) — `command` is resolved as an executable on `PATH` and spawned directly with `args` as the argument vector. No shell is involved on any platform, so there is no tokenization divergence to worry about.

Prefer exec form when the command doesn't need shell features (pipes, `&&`, globbing) — it carries zero shell-divergence risk:

```json
{
  "type": "command",
  "command": "python3",
  "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/lint.py"]
}
```

**Windows trap:** `.cmd`/`.bat` shims that npm installs (`npx`, `eslint`, etc. under `node_modules/.bin`) are not real executables and can't be spawned in exec form. To run one, invoke the underlying script with `node` directly (e.g. `"command": "node", "args": ["node_modules/eslint/bin/eslint.js"]`), or fall back to shell form.

The three-runner fallback below needs `&&`/`||`/`command -v` branching, so it can only run as shell form — see the Windows caveat in the next section.

## Command Paths in settings.json

**Shell assumption: bash-first.** Shell form targets Git Bash on Windows, WSL, macOS, Linux. POSIX syntax (`command -v`, `>/dev/null`, `&&`, `||`) is allowed.

**Windows caveat:** if Git Bash isn't installed, Claude Code runs shell form through **PowerShell**, not cmd.exe. The three-runner chain's POSIX syntax (`command -v`, `{ ; }` grouping) is invalid under PowerShell, so it silently fails there. If a project must support native Windows without Git Bash, either require Git for Windows (also needed for the Bash tool), drop the runner-fallback chain and pin a single interpreter behind exec form instead, or set the hook's `"shell": "bash"` field to force Git Bash explicitly (fails outright if Git Bash isn't present, rather than silently misbehaving under PowerShell).

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

### Path resolution — always use braces

`${CLAUDE_PROJECT_DIR}` and `${CLAUDE_PLUGIN_ROOT}` are Claude-Code-native placeholders: Claude Code substitutes them into `command` (and `args`) as plain strings *before* anything reaches a shell, so they resolve identically under `sh`, Git Bash, PowerShell, or exec form.

**Always use the braced form.** The unbraced `$CLAUDE_PROJECT_DIR` is bash/POSIX shell-variable syntax — it only expands under `sh`/Git Bash. Under PowerShell (the Windows-without-Git-Bash fallback), a bare `$CLAUDE_PROJECT_DIR` is not a defined variable and silently resolves to nothing, breaking the path. Write `"${CLAUDE_PROJECT_DIR}/.claude/hooks/x.py"`, never `"$CLAUDE_PROJECT_DIR"/.claude/hooks/x.py`.

Quote script paths: `"${CLAUDE_PLUGIN_ROOT}/hooks/x.py"` (handles spaces in user home).

## Line Endings

- Use `open(path, 'r', newline='')` when reading files to handle `\r\n`
- Or `.read().replace('\r\n', '\n')` to normalize

## Common Pitfalls

- `chmod +x` does nothing on Windows — Python scripts don't need it there
- `os.sep` in regex patterns — escape properly or use `pathlib`
- Temp file paths — use `tempfile.mkstemp()` not hardcoded `/tmp/`

## Debugging Across Platforms

Pipe the same JSON stdin into the hook script directly on each target OS:

```bash
echo '{"tool_name":"Write","tool_input":{"file_path":"test.py"}}' | python3 .claude/hooks/your_hook.py
echo $?
```

If the exit code is consistent on one OS but diverges on another, the bug is almost always in the script's own path handling — an unbraced placeholder, a hardcoded separator, a hardcoded `$HOME`/`/tmp` — not in the hook registration or matcher config.

## PowerShell Support

- Set `shell: powershell` in SKILL.md frontmatter for PowerShell-based skills
- User must set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`
- Ask the user which shell they use if the plugin needs cross-platform support

## Verification Checklist

- [ ] Uses `pathlib.Path` for all path operations
- [ ] No `shell=True` with string commands (use list args)
- [ ] No hardcoded `/tmp/`, `$HOME`, `%USERPROFILE%`, or path separators
- [ ] `shutil.which()` used to locate external binaries
- [ ] Line endings handled (`newline=''` or normalize)
- [ ] settings.json `command` uses `${CLAUDE_PROJECT_DIR}`/`${CLAUDE_PLUGIN_ROOT}` (braced), never unbraced `$CLAUDE_PROJECT_DIR`
