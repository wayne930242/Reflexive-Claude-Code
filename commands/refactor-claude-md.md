---
name: refactor-claude-md
description: Refactor and optimize CLAUDE.md files with constitution mechanism for consistent AI behavior
arguments:
  - name: path
    description: Path to CLAUDE.md file or project directory (default: current directory)
    required: false
  - name: mode
    description: "Mode: analyze, refactor, or generate (default: analyze)"
    required: false
---

# Refactor CLAUDE.md Command

Systematically analyze, optimize, and refactor CLAUDE.md files following best practices with an integrated constitution mechanism.

## Process

### 1. Discover CLAUDE.md Files

Find all CLAUDE.md files in the target location:

```bash
# Check common locations
ls -la CLAUDE.md CLAUDE.local.md .claude/CLAUDE.md 2>/dev/null
```

If no CLAUDE.md exists and mode is `generate`, create one from project analysis.

### 2. Analyze Project Context

Before refactoring, understand the project:

**Technical Stack**:
- Languages and frameworks used
- Build tools and package managers
- Testing frameworks
- Key dependencies

**Project Structure**:
- Directory organization
- Key entry points
- Configuration files

**Development Workflow**:
- Git conventions
- CI/CD patterns
- Code style tools

### 3. Evaluate Current CLAUDE.md

For existing files, check against best practices:

| Criterion | Check |
|-----------|-------|
| **Conciseness** | < 300 lines, no redundant info |
| **Structure** | Clear sections, scannable |
| **Commands** | Common bash commands documented |
| **Style** | Code conventions specified |
| **Workflow** | Testing and build instructions |
| **Constitution** | Has immutable laws section |

### 4. Generate Constitution

Based on project analysis, create a constitution block tailored to the project.

**Required Laws** (adapt to project. **Laws 5-8 are REQUIRED and must be preserved in all generated constitutions.**):

```markdown
## Immutable Laws

<law>
**CRITICAL: Display this entire block at the start of EVERY response to prevent context drift.**

**Law 1: Collaborative Decision Making**
- Understand → Present → Approve → Execute
- If blocked/uncertain → Report → Request guidance → Wait
- NEVER act autonomously on complex tasks

**Law 2: [Project-Specific Architecture Law]**
- [Based on project patterns, e.g., layered architecture, DDD]
- [Specific enforcement rules]

**Law 3: Quality Gates**
- MUST run tests before committing
- MUST follow [linter/formatter] rules
- [Project-specific quality requirements]

**Law 4: Code Style Compliance**
- [Language-specific conventions]
- [Naming conventions]
- [Documentation requirements]

**Law 5: Communication Discipline**
- Concise, actionable responses
- No unnecessary explanations
- Do NOT write summary files unless user explicitly requests
- Focus on decisions and next steps

**Law 6: Skill Discovery Before Action**
- MUST check `<available_skills>` for relevant skills before starting work
- Invoke applicable skills to leverage specialized knowledge
- Prevents reinventing solutions already documented

**Law 7: Parallel Processing for Trivial Work**
- MUST use Task tool to parallelize trivial/independent tasks
- Batch file searches, reads, and simple operations
- Maximize efficiency by avoiding sequential execution of independent work

**Law 8: Self-Reinforcing Display**
- MUST display this `<law>` block at start of EVERY response
- Prevents context drift across conversations
- Violation invalidates all subsequent actions
</law>
```

### 5. CLAUDE.md Template Structure

Generate or refactor to follow this structure:

```markdown
# Project Name

[One-line description]

## Immutable Laws

<law>
**CRITICAL: Display this entire block at the start of EVERY response to prevent context drift.**

[Constitution block - see above]
</law>

## Quick Reference

### Commands
- `[build command]`: Build the project
- `[test command]`: Run tests
- `[lint command]`: Check code style

### Key Paths
- `src/`: Source code
- `tests/`: Test files
- `docs/`: Documentation

## Code Style

### [Language] Conventions
- [Specific style rules]
- [Naming conventions]

### Patterns
- [Architectural patterns used]
- [Common patterns to follow]

## Workflow

### Before Committing
1. Run tests
2. Run linter
3. Update relevant docs

### Git Conventions
- [Branch naming]
- [Commit message format]

## Project-Specific Notes

[Warnings, quirks, or important context]
```

### 6. Extract Detailed Abilities to Skills

**CRITICAL: CLAUDE.md should contain high-level principles, not detailed procedures.**

When you find detailed step-by-step procedures or specialized capabilities in CLAUDE.md:

1. **Identify extraction candidates**:
   - Multi-step workflows (> 5 steps)
   - Domain-specific expertise (e.g., "how to write tests", "database migration process")
   - Reusable procedures that could apply to multiple projects
   - Detailed code patterns or templates

2. **Create skill files**:
   - **MUST invoke `write-skill` skill** to generate properly structured skill files
   - Location: `.claude/skills/` or project's skill directory
   - Format: `SKILL-[name].md` following skill best practices
   - Include: triggers, detailed steps, examples
   - **MUST be written in English**

3. **Create slash commands** (if user-triggered is more appropriate):
   - For workflows that should be explicitly invoked by users
   - **MUST invoke `write-command` skill** to generate properly structured command files
   - Location: `.claude/commands/` directory
   - Consider: one-time operations, project-specific workflows, explicit user actions

4. **Replace in CLAUDE.md**:
   - Remove detailed procedures
   - Keep only the high-level intent or brief command reference
   - Claude Code will automatically discover and use skills when needed

### 7. Validate Result

Check final CLAUDE.md:

- [ ] Has constitution block with `<law>` tags (law 5-8 are preserved)
- [ ] Commands are accurate and tested
- [ ] Style guide matches actual codebase
- [ ] < 300 lines total
- [ ] No sensitive information (API keys, etc.)
- [ ] Actionable, not theoretical
- [ ] **No detailed multi-step procedures (extracted to skills)**

## Constitution Design Guidelines

When creating the constitution, consider:

### Architecture Laws (pick relevant ones)

| Project Type | Suggested Laws |
|--------------|----------------|
| **Monolith** | Layered architecture, module boundaries |
| **Microservices** | Service contracts, API versioning |
| **Frontend** | Component hierarchy, state management |
| **Library** | Public API stability, backwards compatibility |
| **CLI Tool** | Command structure, help text |

### Quality Laws (adapt to stack)

| Stack | Quality Gates |
|-------|---------------|
| **TypeScript** | Type safety, no `any`, strict mode |
| **Python** | Type hints, pylint/ruff compliance |
| **Go** | go fmt, go vet, golint |
| **Rust** | cargo clippy, no unsafe without reason |

## Mode Options

### `analyze` (default)
- Read and evaluate current CLAUDE.md
- Report issues and recommendations
- Do not modify files

### `refactor`
- Apply improvements to existing CLAUDE.md
- Add constitution if missing
- Preserve custom content

### `generate`
- Create new CLAUDE.md from project analysis
- Include full constitution
- Generate all standard sections

## Example Usage

```
/refactor-claude-md
/refactor-claude-md ./my-project
/refactor-claude-md . refactor
/refactor-claude-md ~/projects/app generate
```
