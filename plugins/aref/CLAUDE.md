# aref Plugin

對既有專案做 agent-friendly 重構的 plugin。獨立版號，不隨 rcc 連動。

## Version Bump

版號同步位置以根目錄 CLAUDE.md 的 Law 2 為唯一來源（aref 的 `marketplace.json` 與 README 標頭目前仍需手動同步）。

只有 aref-scoped commit（`feat(aref):`、`fix(aref):`、`feat(aref)!:`）會 bump aref；無 scope 的 `fix:` / `feat:` 只動 rcc。
