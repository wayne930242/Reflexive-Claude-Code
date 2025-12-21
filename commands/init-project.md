---
name: init-project
description: Initialize a new project with framework, best practices, and agent system from scratch
arguments:
  - name: path
    description: Path to project directory (default: current directory)
    required: false
---

# Project Initialization

Bootstrap a new project with modern best practices and agent system.

## Process

### 1. Requirements Gathering

First ask **Project Type**, then ask relevant questions based on type.

#### Question Groups

| # | Question | Description |
|---|----------|-------------|
| 1 | Language & Runtime | TypeScript, Python, Go, Rust, etc. (with version) |
| 2 | Framework | Next.js, FastAPI, Gin, Astro, etc. |
| 3 | UI Library | React, Vue, Svelte, native |
| 4 | Styling | Tailwind, CSS Modules, Styled Components |
| 5 | State Management | Redux, Zustand, Pinia, Context API |
| 6 | Data Fetching | React Query, SWR, Apollo, tRPC |
| 7 | Backend Service | Vercel Edge, Cloudflare Workers, AWS Lambda |
| 8 | ORM / Database | Prisma, Drizzle, SQLAlchemy, TypeORM |
| 9 | Validation | Zod, Yup, Pydantic |
| 10 | API Style | REST, GraphQL, gRPC, tRPC |
| 11 | Auth Strategy | JWT, session, OAuth providers |
| 12 | Package Manager | npm, pnpm, yarn, bun, uv |
| 13 | Testing | Jest, Vitest, Pytest, Go test |
| 14 | Linting & Formatting | ESLint, Prettier, Biome, Ruff |
| 15 | CI/CD | GitHub Actions, GitLab CI |
| 16 | Deployment Target | Vercel, AWS, Docker, self-hosted |
| 17 | Methodology | DDD, TDD, clean architecture, hexagonal |
| 18 | Monorepo Tools | Turborepo, Nx, pnpm workspaces |
| 19 | Notebook Environment | Jupyter, Google Colab, VS Code notebooks |
| 20 | Static Site Generator | Astro, Hugo, 11ty, Jekyll |

#### Project Type → Questions

| Project Type | Questions |
|--------------|-----------|
| **Frontend SPA** | 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16 |
| **Frontend + Light Backend** | 1, 2, 3, 4, 5, 6, 7, 9, 12, 13, 14, 15, 16 |
| **Full-stack App** | 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 |
| **API Service (with DB)** | 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 |
| **Lightweight Service** | 1, 2, 9, 10, 12, 13, 14, 15, 16 |
| **Research / Notebook** | 1, 12, 14, 19 |
| **Static Blog / Docs** | 1, 2, 4, 12, 14, 15, 16, 20 |
| **CLI Tool / Library** | 1, 9, 12, 13, 14, 15 |
| **Monorepo** | 1, 12, 14, 15, 18 + (ask sub-project types) |

Ask questions iteratively. Skip if already answered or not applicable.

### 2. Research Best Practices

Use web search to find:

- Latest stable version of chosen framework
- Official CLI tool and initialization commands
- Current best practices and recommended project structure
- Breaking changes or migration notes if relevant

### 3. Write Blueprint

Create `/docs/blueprint.md` with:

```markdown
# Project Blueprint

## Stack
- Language: [version]
- Framework: [version]
- Package manager: [choice]

## Project Structure
[Recommended directory layout]

## Initialization Command
[Official CLI command to bootstrap, e.g., `npx create-next-app@latest`]

## Key Dependencies
[Core packages with versions]

## Conventions
[Code style, patterns, architecture decisions]
```

**Ask user to confirm the blueprint before proceeding.**

### 4. Bootstrap Project

After user confirmation:

1. Run the official CLI tool to create project (prefer official scaffolding over manual setup)
2. Install additional dependencies if needed
3. Apply any post-init configurations

### 5. Setup Agent System

Invoke `/migration` command to:

- Create CLAUDE.md with project-specific constitution
- Setup skills, commands, subagents as needed
- Configure hooks for static checks (linting, formatting, type checking)
- Create rules based on discovered conventions

### 6. Final Confirmation

Ask user if they want to proceed with bootstrapping according to the blueprint.

## Example Usage

```
/init-project
/init-project ./my-new-app
```
