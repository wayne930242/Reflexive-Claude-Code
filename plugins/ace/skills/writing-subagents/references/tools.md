# Available Tools for Subagents

## File Operations

| Tool | Purpose | Read-Only |
|------|---------|-----------|
| `Read` | Read file contents | Yes |
| `Edit` | Modify existing files | No |
| `Write` | Create new files | No |
| `Glob` | Find files by pattern | Yes |

## Search Operations

| Tool | Purpose | Read-Only |
|------|---------|-----------|
| `Grep` | Search file contents | Yes |

## System Operations

| Tool | Purpose | Read-Only |
|------|---------|-----------|
| `Bash` | Execute shell commands | Depends |

## Web Operations

| Tool | Purpose | Read-Only |
|------|---------|-----------|
| `WebFetch` | Fetch web content | Yes |
| `WebSearch` | Search the web | Yes |

## MCP Tools

If MCP servers are configured, their tools are also available.
Common examples:
- `mcp__context7__*` - Documentation lookup
- `mcp__playwright__*` - Browser automation
- `mcp__ide__*` - IDE integration

## Tool Combinations by Use Case

### Read-Only Analysis

```yaml
tools: Read, Grep, Glob
```

Best for: Code review, exploration, security audit

### Code Modification

```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
```

Best for: Refactoring, implementation, fixes

### Testing

```yaml
tools: Read, Bash, Grep, Glob
```

Best for: Test execution, debugging

### Documentation

```yaml
tools: Read, Edit, Write, Glob
```

Best for: Doc generation, updates

### Research

```yaml
tools: Read, Grep, Glob, WebFetch, WebSearch
```

Best for: Learning, external documentation

## Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Normal permission prompts |
| `acceptEdits` | Auto-accept file edits |
| `bypassPermissions` | Skip all prompts (dangerous) |
| `plan` | Read-only, planning mode |
| `ignore` | Ignore this field |

## Best Practices

1. **Principle of Least Privilege**: Only grant necessary tools
2. **Read-Only Default**: Start with read-only tools, add write access if needed
3. **Bash Caution**: Bash can do anything - consider limiting for untrusted tasks
4. **MCP Awareness**: Know what MCP tools expose before granting access
