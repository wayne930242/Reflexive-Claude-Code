# Generic Fallback (unknown language)

Used when no supported manifest is detected. Provides minimum viable analysis.

## Tools

| Tool | Purpose | Install | Invocation |
|------|---------|---------|------------|
| jscpd | Duplication | `npm i -g jscpd` | `jscpd --reporters json -o <out-dir> .` |
| semgrep | Semantic patterns (auto config includes many langs) | `pip install semgrep` | `semgrep --config auto --json .` |
| `find` + `wc -l` | Line counts | POSIX | `find . -type f -print \| xargs wc -l \| sort -rn \| head -50` |
| `tree` | Directory shape | `brew install tree` or `apt install tree` | `tree -L 3 -I 'node_modules\|venv\|.git'` |

## Procedure

1. `tree -L 3 -I node_modules\|venv\|.git` → directory shape
2. `find . -type f \( -name '*.md' -o -name 'LICENSE' \) -prune -o -type f -print | xargs wc -l | sort -rn | head -50` → largest files
3. `jscpd --reporters json .` → duplication
4. `semgrep --config auto --json .` → patterns
5. `git log --format=format: --name-only --since="6 months ago" | grep -v '^$' | sort | uniq -c | sort -rn | head -20` → churn

## Limitations

- No dep graph (unknown import syntax).
- No cognitive complexity.
- Hotspot = churn × file size as weak proxy.

Record limitations in the refactor map so planning-refactors knows to prompt the user for missing context.
