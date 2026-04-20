# Refactor Map Schema

`.rcc/{ts}-refactor-map.md` format. Markdown with explicit `##` sections so `planning-refactors` can parse.

## Required Sections

### Run Metadata

```
- run_ts: YYYYMMDD-HHMMSS
- scope: <path(s)>
- languages: [ts, py, ...]
- monorepo: true|false
- subprojects: [list of paths]
```

### Tool Status

Table: tool name | language | status (ran|skipped|failed) | raw output path

### Hotspots (Top 20)

Ordered list. Each entry:

```
- rank: N
  path: <file>
  score: <number>
  churn_last_6mo: <commits>
  cognitive_complexity: <n>
  cyclomatic: <n>
  lines: <n>
  notes: <why it's a hotspot>
```

### Cyclic Dependencies

List each cycle as `A → B → C → A`. If zero, state "None detected".

### Duplication

Top duplicate clusters by token count (jscpd output).

### AGENTS.md Status

- root: present|absent|partial
- subprojects: per-subproject status
- gaps: list sections missing per expected template

### Limitations

Any degraded analysis (missing tool, generic fallback). Explicit list so planning knows what it doesn't know.

## Parse Rules

Planning-refactors MUST:
- Read sections in the exact order above.
- Treat any missing section as a FAIL and ask user to rerun analyzing-codebases.
- Respect the "Limitations" section — do not propose work blind.
