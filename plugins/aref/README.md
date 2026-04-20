# aref

Agentic refactoring pipeline for Claude Code.
Restructures existing codebases toward AI-agent-friendly architecture: modular, single-entry, characterization-tested, complexity-bounded.

<!-- x-release-please-version package-name="aref" -->
Version: 0.1.0

## Installation

```bash
claude plugin add wayne930242/Reflexive-Claude-Code
```

## Usage

Run in a project repository:

```
/aref
```

Plugin detects the project language(s), runs analysis, proposes a phased refactor plan, scaffolds characterization tests, applies refactors phase-by-phase with checkpoints, verifies against hard rules and mutation testing, then produces `AGENTS.md` files for future AI coding agents.

## Skills

| Skill | Purpose |
|-------|---------|
| analyzing-codebases | Detect languages, run toolchain, produce refactor map |
| planning-refactors | Propose phased refactor plan from map |
| scaffolding-characterization-tests | Add golden/snapshot tests to hotspots before refactor |
| applying-refactors | Execute plan phase-by-phase on a dedicated branch |
| verifying-refactors | Validate hard rules and run mutation testing on touched modules |
| finalizing-refactors | Write AGENTS.md per subproject, suggest rcc handoff |

## Supported Languages

Deep toolchain support: TypeScript/JavaScript, Python, Rust, Go.
Other languages fall back to generic analysis (semgrep + directory tree + line counts).

## Required Tools (per language)

See each language's toolchain reference in `skills/analyzing-codebases/references/`.

## License

MIT
