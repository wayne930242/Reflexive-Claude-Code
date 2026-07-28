# Path Patterns for Rules

> **Reminder**: `paths:` is a real load gate. A rule with `paths:` enters context only when Claude reads a matching file; a rule without `paths:` loads at launch in every session. Scope aggressively.

## Basic Patterns

| Pattern | Description | Example Match |
|---------|-------------|---------------|
| `*` | Any file in current dir | `*.ts` matches `index.ts` |
| `**` | Any directory depth | `**/*.ts` matches `src/utils/helper.ts` |
| `?` | Single character | `file?.ts` matches `file1.ts` |

## Directory Patterns

```yaml
# All files in specific directory
paths:
  - "src/api/**"

# Only direct children
paths:
  - "src/api/*"

# Specific subdirectory structure
paths:
  - "src/**/utils/**"
```

## Extension Patterns

```yaml
# Single extension
paths:
  - "**/*.ts"

# Multiple extensions (brace expansion)
paths:
  - "**/*.{ts,tsx}"

# Exclude test files (use separate rule instead)
paths:
  - "src/**/*.ts"
# Then create another rule for tests with paths: ["**/*.test.ts"]
```

## Multiple Path Patterns

```yaml
# Multiple paths
paths:
  - "src/**/*.ts"
  - "lib/**/*.ts"

# Brace expansion for directories
paths:
  - "{src,lib,packages}/**/*.ts"
```

## Common Configurations

### Frontend Project

```yaml
# Components
paths:
  - "src/components/**/*.{tsx,jsx}"

# Styles
paths:
  - "src/**/*.{css,scss,less}"

# State management
paths:
  - "src/store/**/*.ts"
```

### Backend Project

```yaml
# API routes
paths:
  - "src/api/**/*.ts"
  - "src/routes/**/*.ts"

# Database
paths:
  - "src/db/**/*.ts"
  - "src/models/**/*.ts"

# Middleware
paths:
  - "src/middleware/**/*.ts"
```

### Monorepo

```yaml
# Specific package
paths:
  - "packages/core/**/*.ts"

# All packages
paths:
  - "packages/**/src/**/*.ts"

# Shared code
paths:
  - "{packages,libs}/shared/**/*.ts"
```

## Testing Rules

```yaml
# All test files
paths:
  - "**/*.test.ts"
  - "**/*.spec.ts"

# Specific test directory
paths:
  - "tests/**/*.ts"
  - "__tests__/**/*.ts"

# E2E tests only
paths:
  - "e2e/**/*.ts"
  - "cypress/**/*.ts"
```

## Priority Notes

- More specific paths take precedence
- Rules without `paths:` are global (lowest specificity) and always resident
- Use descriptive names: `api-conventions.md`, `testing-guidelines.md`

## Glob Gotchas

- **Brace budget**: a rule's whole `paths:` list shares one budget of 1,000 expanded patterns and 4 MiB. Each brace group multiplies the count (`{a,b}/{c,d}/*.{ts,tsx}` = 8). Patterns that exceed the budget are used unexpanded, so their literal braces match nothing.
- **Bracket syntax**: `[` starts a bracket expression. A pattern like `photos [2024/**` is invalid and matches nothing; escape it as `photos \[2024/**`.
