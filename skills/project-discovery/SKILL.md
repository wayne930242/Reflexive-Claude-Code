---
name: project-discovery
description: Deep project analysis for architecture planning. Use when starting migration or designing new agent components for an unfamiliar codebase.
---

# Project Discovery

Systematically explore a project to produce a discovery report for `agent-architect`.

## Process

### 1. Structure Scan

Explore the project root and key directories:

```
□ Root files: package.json, pyproject.toml, Cargo.toml, go.mod, etc.
□ Source directories: src/, lib/, app/, components/
□ Config files: tsconfig.json, .eslintrc, prettier, etc.
□ CI/CD: .github/workflows/, .gitlab-ci.yml, Jenkinsfile
□ Existing Claude setup: .claude/, CLAUDE.md
```

### 2. Tech Stack Identification

Determine:

| Aspect | Examples |
|--------|----------|
| Language(s) | TypeScript, Python, Rust, Go |
| Framework | React, Next.js, FastAPI, Express |
| Build tools | Vite, Webpack, esbuild, tsc |
| Package manager | npm, pnpm, yarn, pip, cargo |
| Test framework | Jest, Vitest, pytest, go test |

### 3. Workflow Discovery

Identify existing automation and manual workflows:

**Automated:**
- Build scripts in package.json / Makefile
- CI/CD pipelines
- Pre-commit hooks (husky, lint-staged)
- Existing Claude hooks

**Manual (candidates for automation):**
- Common developer commands
- Deployment procedures
- Release processes

### 4. Pattern Recognition

Look for:
- Code conventions (formatting, naming)
- Architecture patterns (DDD, clean arch, MVC)
- Testing patterns (unit, integration, e2e)
- Documentation style

## Output: Discovery Report

Produce a structured report:

```markdown
# Discovery Report: [Project Name]

## Overview
- **Type**: [Web app / CLI / Library / API / Monorepo]
- **Language**: [Primary language(s)]
- **Framework**: [Main framework(s)]

## Tech Stack
| Category | Technology |
|----------|------------|
| Runtime | ... |
| Framework | ... |
| Build | ... |
| Test | ... |
| Lint/Format | ... |

## Existing Automation
- [List current CI/CD, hooks, scripts]

## Recommended Components

### Skills
- [ ] `skill-name` - [reason]

### Commands
- [ ] `/command-name` - [reason]

### Hooks
- [ ] `hook-name` on [event] - [reason]

### Rules
- [ ] `rule-name` - [convention to extract]

## Notes
[Any special considerations, legacy code, migration risks]
```

## Handoff

After producing the report:
1. Present findings to user for validation
2. Pass approved recommendations to `agent-architect`
3. Let `agent-architect` classify and delegate each component

## Exploration Tips

- Use `Glob` for file patterns: `**/*.config.*`, `**/test/**`
- Use `Grep` for conventions: `import`, `export default`, `async function`
- Check README.md for documented workflows
- Look at recent git commits for active development areas
