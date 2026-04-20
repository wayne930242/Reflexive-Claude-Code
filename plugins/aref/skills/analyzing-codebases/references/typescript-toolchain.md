# TypeScript / JavaScript Toolchain

## Required Tools

| Tool | Purpose | Install | Invocation |
|------|---------|---------|------------|
| dependency-cruiser | Dep graph + cycles | `npm i -D dependency-cruiser` | `npx depcruise --output-type json src` |
| madge | Alt dep graph | `npm i -D madge` | `npx madge --json src` |
| jscpd | Duplication | `npm i -D jscpd` | `npx jscpd --reporters json -o .rcc/aref-raw src` |
| eslint-plugin-sonarjs | Cognitive complexity | `npm i -D eslint-plugin-sonarjs` | via eslint with `sonarjs/cognitive-complexity` rule |
| semgrep | Semantic patterns | `pip install semgrep` | `semgrep --config auto --json src` |
| tsc | Type errors | ships with TypeScript | `npx tsc --noEmit` |

## Minimum Versions

- Node.js >=20
- dependency-cruiser >=16
- jscpd >=4
- semgrep >=1.90

## Output Locations

All raw outputs go to `.rcc/aref-raw/{ts}-ts-<tool>.json`.

## Notes

- Use `dependency-cruiser` as primary; `madge` only if dependency-cruiser fails on monorepo aliases.
- Exclude `node_modules`, `dist`, `build` by default.
- For Vite/Next projects, exclude `.next`, `.turbo`, `.svelte-kit`.
