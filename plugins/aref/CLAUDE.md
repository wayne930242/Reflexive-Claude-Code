# aref Plugin

對既有專案做 agent-friendly 重構的 plugin。獨立版號，不隨 rcc 連動。

## Version Bump Locations

commit 含 `feat(aref):` / `fix(aref):` / `feat(aref)!:` 時，同步更新：

1. `.claude-plugin/plugin.json` → `version`（release-please 自動）
2. `../../.claude-plugin/marketplace.json` → `plugins[1].version`（**手動** — release-please 不跨 package 路徑）
3. `../../README.md` + `../../README.zh-TW.md` → aref 標頭版號（**手動** — markers 已移除避免 rcc release 誤覆寫）

Conventional Commits → 版號 mapping：

- `fix(aref):` → patch
- `feat(aref):` → minor
- `feat(aref)!:` / `BREAKING CHANGE:` → major

**注意**：無 scope 的 `fix:` / `feat:` 只動 rcc，不動 aref。
