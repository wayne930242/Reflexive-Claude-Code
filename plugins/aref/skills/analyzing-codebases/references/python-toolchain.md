# Python Toolchain

## Required Tools

| Tool | Purpose | Install | Invocation |
|------|---------|---------|------------|
| pydeps | Dep graph | `pip install pydeps` | `pydeps --show-deps --no-output src` |
| radon | Cyclomatic + maintainability | `pip install radon` | `radon cc src -j` / `radon mi src -j` |
| lizard | Cognitive complexity | `pip install lizard` | `lizard src -X` |
| jscpd | Duplication | `npm i -g jscpd` | `jscpd --reporters json src` |
| semgrep | Semantic patterns | `pip install semgrep` | `semgrep --config auto --json src` |
| ruff | Linter | `pip install ruff` | `ruff check src --output-format json` |
| mypy | Type checker (if typed) | `pip install mypy` | `mypy src --no-error-summary` |

## Minimum Versions

- Python >=3.10
- radon >=6
- lizard >=1.17
- ruff >=0.4
- mypy >=1.8

## Output Locations

`.rcc/aref-raw/{ts}-py-<tool>.json`.

## Notes

- Detect virtualenv: check `VIRTUAL_ENV` or `poetry env info`. Run tools inside venv.
- Respect `pyproject.toml` `[tool.*]` configs if present.
- Exclude `venv`, `.venv`, `__pycache__`, `.pytest_cache`.
