# rcc Plugin

Claude Code 核心 ACE（Agentic Context Engineering）插件。

## Version Bump Locations

commit 含 `feat:` / `fix:` / `feat!:` 時，以下位置必須同步為新版號：

1. `.claude-plugin/plugin.json` → `version`
2. `../../.claude-plugin/marketplace.json` → `metadata.version` + `plugins[0].version`
3. `../../README.md` + `../../README.zh-TW.md` → rcc 標頭版號（`<!-- x-release-please-version -->` marker 範圍內）

Conventional Commits → 版號 mapping：

- `fix:` → patch（1.2.3 → 1.2.4）
- `feat:` → minor（1.2.3 → 1.3.0）
- `feat!:` / `BREAKING CHANGE:` → major（1.2.3 → 2.0.0）

release-please 通常自動處理。CI 失敗時手動補齊所有位置。

## Commit Scope

- rcc commit 無 scope：`feat: ...`、`fix: ...`
- aref commit 加 scope：`feat(aref): ...`（不影響 rcc 版號）
