# Project Scanning Reference

Scan the target project to understand its stack, structure, workflow, and team scale before making recommendations.

---

## 1. Language/Framework Detection

Check file existence at project root to infer stack.

| Marker File | Language | Read For |
|---|---|---|
| `package.json` | Node.js | dependencies → React, Next.js, Express, etc. |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python | django, flask, fastapi |
| `go.mod` | Go | module path, dependencies |
| `Cargo.toml` | Rust | crate name, dependencies |
| `pom.xml` / `build.gradle` | Java | group/artifact, dependencies |
| `Gemfile` | Ruby | rails, sinatra |
| `composer.json` | PHP | laravel, symfony |

Multiple language markers present → monorepo or fullstack project.

## 2. Project Type Inference

Infer from directory structure.

| Pattern | Type |
|---|---|
| `apps/` + `packages/` or `workspaces` in package.json | Monorepo |
| `src/` + single language | Single-package |
| `bin/` or CLI entry point in manifest | CLI tool |
| `lib/` + publish config in manifest | Library |
| `Dockerfile` + `docker-compose` + multiple service dirs | Multi-service |
| `src/app/` or `pages/` or `src/routes/` | Web application |

## 3. Development Workflow Detection

### CI/CD

| Marker | System |
|---|---|
| `.github/workflows/` | GitHub Actions |
| `.gitlab-ci.yml` | GitLab CI |
| `Jenkinsfile` | Jenkins |
| `.circleci/config.yml` | CircleCI |
| `bitbucket-pipelines.yml` | Bitbucket Pipelines |

Read job/step names to understand scope (build, test, deploy, lint, security scan).

### Testing

| Marker | Framework |
|---|---|
| `jest.config.*` | Jest |
| `vitest.config.*` | Vitest |
| `pytest.ini` / `conftest.py` | pytest |
| `*_test.go` files | Go testing |
| `*.spec.ts` / `*.test.ts` | JS/TS test files |
| `spec/` directory | RSpec (Ruby) |

### Linting/Formatting

| Marker | Tool |
|---|---|
| `.eslintrc*` / `eslint.config.*` | ESLint |
| `.prettierrc*` | Prettier |
| `ruff.toml` / `ruff` in pyproject.toml | Ruff |
| `biome.json` | Biome |
| `.editorconfig` | EditorConfig |
| `.golangci.yml` | golangci-lint |

## 4. Team Scale Signals

| Signal | How to Check | Interpretation |
|---|---|---|
| `CODEOWNERS` | File exists | Code review with ownership areas |
| `CONTRIBUTING.md` | File exists | Multi-contributor project |
| Branch count | `git branch -r \| wc -l` | <5 solo, 5-20 medium, >20 large |
| Recent committers | `git log --since='3 months ago' --format='%ae' \| sort -u \| wc -l` | Active contributor count |
| PR templates | `.github/PULL_REQUEST_TEMPLATE*` | Formal review process |

---

## Output Template

Record findings in this format:

| Aspect | Finding |
|---|---|
| Language(s) | e.g., TypeScript, Python |
| Framework(s) | e.g., Next.js, FastAPI |
| Project type | e.g., Monorepo, Single-package |
| CI/CD | e.g., GitHub Actions (build, test, deploy) |
| Testing | e.g., Vitest, pytest |
| Linting | e.g., ESLint, Prettier, Ruff |
| Team scale | e.g., Medium (12 branches, 4 recent committers) |
| Notable | e.g., CODEOWNERS present, PR templates |
