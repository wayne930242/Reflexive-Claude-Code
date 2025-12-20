# Rule Examples by Domain

> **Note**: Rules are for conventions/guidelines only. For immutable laws, use `<law>` blocks in CLAUDE.md.

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
