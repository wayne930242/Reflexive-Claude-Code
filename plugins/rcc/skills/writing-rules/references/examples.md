# Rule Examples by Domain

> **Note**: Rules are for path-scoped conventions. For broad project instructions, use CLAUDE.md directly.

## Code Style Conventions

### TypeScript (Global)

```yaml
# .claude/rules/typescript.md
---
paths: **/*.{ts,tsx}
---

# TypeScript Rules

- Use strict mode
- No `any` type without justification
- Prefer `interface` over `type` for objects
- Use named exports
```

### Python (Global)

```yaml
# .claude/rules/python.md
---
paths: **/*.py
---

# Python Rules

- Follow PEP 8
- Type hints required for public functions
- Docstrings for modules and classes
- Use pathlib over os.path
```

---

## Domain-Specific Rules

### API Endpoints

```yaml
# .claude/rules/api/validation.md
---
paths: src/api/**/*.ts, src/routes/**/*.ts
---

# API Rules

- All endpoints MUST validate input
- Use standard error response format
- Include OpenAPI documentation
- Rate limiting required for public endpoints
```

### Database Operations

```yaml
# .claude/rules/database/safety.md
---
paths: src/db/**/*.ts, src/models/**/*.ts
---

# Database Rules

- All queries MUST use parameterized statements
- Transactions required for multi-step operations
- No raw SQL in application code
- Migrations MUST be reversible
```

### React Components

```yaml
# .claude/rules/frontend/components.md
---
paths: src/components/**/*.tsx
---

# Component Rules

- One component per file
- Props interface required
- No inline styles
- Accessibility attributes required
```

---

## Testing Rules

### Test Coverage

```yaml
# .claude/rules/testing/coverage.md
---
paths: **/*.test.ts, **/*.spec.ts
---

# Testing Rules

- Coverage MUST be > 80%
- No skipped tests in main branch
- Test names MUST describe behavior
- One assertion focus per test
```

### E2E Tests

```yaml
# .claude/rules/testing/e2e.md
---
paths: e2e/**/*.ts, cypress/**/*.ts
---

# E2E Rules

- Tests MUST be independent
- Use data-testid for selectors
- Clean up test data after run
- No hardcoded timeouts
```

---

## Security Rules

### Authentication

```yaml
# .claude/rules/security/auth.md
---
paths: src/auth/**/*.ts, src/middleware/auth*.ts
---

# Auth Rules

- Never log credentials
- Tokens MUST expire
- Use secure cookie flags
- Rate limit auth endpoints
```

### Secrets

```yaml
# .claude/rules/security/secrets.md
---
# Global
---

# Secret Rules

- Never commit .env files
- No hardcoded secrets
- Use environment variables
- Rotate secrets regularly
```

---

## Workflow Rules

### Git Conventions

```yaml
# .claude/rules/git.md
---
# Global
---

# Git Rules

- Conventional commit messages
- No force push to main/master
- PRs require review
- Squash merge preferred
```

---

## Safety Bypass Prevention (Recommended Defaults)

These are baseline safety rules every agent system should have. They prevent destructive/irreversible actions from happening without explicit user confirmation. Pair with `reflecting` skill's `safety_bypass` detection for full loop (prevent → detect → learn).

### Git Safety (Global)

```yaml
# .claude/rules/git-safety.md
---
# Global — always active
---

# Git Safety

- `git push --force` / `--force-with-lease` to any remote branch: require explicit user confirmation. State exact command and target; wait for approval.
- Never `git push --force` to main/master under any circumstance.
- Never use `--no-verify`, `--no-gpg-sign`, `-c commit.gpgsign=false` unless user explicitly requests.
- Never `git reset --hard`, `git checkout .`, `git restore .`, `git clean -f`, `git branch -D` without user confirmation.
- Before staging untracked files, verify `.gitignore` excludes local tooling dirs. Stage specific files by name; never `git add .` or `git add -A`.
- Investigate unfamiliar files/branches before deleting — they may be user in-progress work.
```

### Deployment Safety (Global)

```yaml
# .claude/rules/deploy-safety.md
---
# Global
---

# Deploy Safety

- Never `rsync --delete` without verifying exclusion of runtime files (.env, state files, tokens).
- Run project test suite before any deploy. No untested deploys.
- Ansible: always `--check` (dry-run) on production targets first.
- Verify target directory exists and is non-empty before destructive sync.
```

### Destructive Command Confirmation (Global)

```yaml
# .claude/rules/destructive-ops.md
---
# Global
---

# Destructive Operations

- `rm -rf`, `DROP TABLE`, dropping databases, overwriting uncommitted changes: require explicit confirmation naming exact target.
- Do not delete or edit tests to make them pass. Fix implementation instead. If tests are wrong, surface the discrepancy.
- Do not use destructive actions as shortcuts around obstacles. Investigate root cause first.
- Hooks/validators failing is a signal — do not bypass with `--no-verify`. Fix the underlying issue.
```

**When to scope these rules:** Most safety rules should be **global** (always active). Path-scoping defeats the purpose — destructive commands need catching regardless of which file the agent is editing. Scope only if a specific subsystem has different risk profile (e.g. migration scripts with reversibility requirements).

**Law vs rule:** If a safety constraint is absolute and project-specific (e.g. "never force push to this monorepo's main"), consider promoting to a CLAUDE.md Law for self-reinforcement.
