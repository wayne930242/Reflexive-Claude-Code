# Go Toolchain

## Required Tools

| Tool | Purpose | Install | Invocation |
|------|---------|---------|------------|
| go-callvis | Call graph | `go install github.com/ofabry/go-callvis@latest` | `go-callvis -format dot ./... > <output>.dot` (no JSON output; use `dot` and parse text or convert via graphviz) |
| gocyclo | Cyclomatic | `go install github.com/fzipp/gocyclo/cmd/gocyclo@latest` | `gocyclo -over 0 .` (text output: `<complexity> <package> <function> <file:line:col>`) |
| gocognit | Cognitive complexity | `go install github.com/uudashr/gocognit/cmd/gocognit@latest` | `gocognit -json .` |
| staticcheck | Linter | `go install honnef.co/go/tools/cmd/staticcheck@latest` | `staticcheck -f json ./...` |
| jscpd | Duplication | `npm i -g jscpd` | `jscpd --reporters json .` |
| semgrep | Semantic patterns | `pip install semgrep` | `semgrep --config auto --json .` |

## Minimum Versions

- Go >=1.22

## Output Locations

`.rcc/aref-raw/{ts}-go-<tool>.<ext>` per tool's native format:
- `gocognit`, `staticcheck`, `semgrep`, `jscpd` → `.json`
- `gocyclo` → `.txt`
- `go-callvis` → `.dot`

## Notes

- Multi-module: iterate each `go.mod` directory.
- Exclude `vendor/`, `testdata/`.
