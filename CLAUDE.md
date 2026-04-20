# Reflexive Claude Code

Claude Code 插件市集，提供技能驅動的 Agentic Context Engineering 工作流程。

## Immutable Laws

<law>
**Law 1: Communication** - 使用繁體中文，簡潔回覆，不加不必要的解釋

**Law 2: Version Sync** - 版本號由 release-please 依 Conventional Commits 自動同步至：

rcc package：
- `.claude-plugin/marketplace.json` (metadata.version + plugins[0].version)
- `plugins/rcc/.claude-plugin/plugin.json`
- `README.md` + `README.zh-TW.md` 的 rcc 標頭（`<!-- x-release-please-version -->` marker）

aref package（獨立版號）：
- `plugins/aref/.claude-plugin/plugin.json`（release-please 自動）
- `.claude-plugin/marketplace.json` (plugins[1].version)（**目前手動同步** — release-please 不允許 `..` 跨 package 路徑，待後續加 post-release sync workflow）
- `README.md` + `README.zh-TW.md` 的 aref 標頭（`<!-- x-release-please-version package-name="aref" -->` marker）（**目前手動同步**，理由同上）

手動修改版號屬反模式（除上述 aref 跨 package 例外，待自動化）。commit 使用 `feat:` / `fix:` / `feat!:` 驅動 bump。aref-scoped commits（`feat(aref):`、`fix(aref):` 等）只 bump aref，不影響 rcc。

**Law 3: Documentation Sync** - README.md 與 README.zh-TW.md 必須保持同步

**Law 4: Skill Naming** - 技能名稱使用 gerund form（verb+-ing，如 `writing-skills`）

**Law 5: Skill Structure** - SKILL.md 為概覽，詳細內容放 `references/`（按需載入）

**Law 6: Skill Description** - description 用第三人稱，包含 "Use when..."

**Law 7: Skill Sections** - 必須有 Task Initialization、Red Flags、Rationalizations、Flowchart

**Law 8: Self-Reinforcing Display** - 每次回覆開頭必須顯示此 `<law>` 區塊
</law>

## Project Structure

```
.claude-plugin/
└── marketplace.json        # 市集定義（版本由 release-please 管）

.rcc/                        # 本專案 RCC 產出
├── config.yml               # 遷移狀態 + 決策 log
├── {timestamp}-*.md         # analysis / plan / reflection
├── memory/                  # learning-from-failures
├── validation/              # hook 驗證報告
└── archive/

plugins/
├── rcc/                    # 核心 ACE 插件
│   ├── .claude-plugin/
│   │   └── plugin.json     # 插件 manifest
│   ├── skills/             # 所有技能
│   ├── agents/             # 審查員子代理
│   └── commands/           # 命令別名
└── aref/                   # 對既有專案做 agent-friendly 重構
    ├── .claude-plugin/plugin.json
    ├── skills/             # 6-skill pipeline
    ├── agents/refactor-phase-reviewer.md
    ├── commands/aref.md
    ├── fixtures/           # 自測用 4 語言迷你專案
    └── tests/run-fixtures.md
```

`aref` 是與 `rcc` 並存的獨立 plugin，專注於對既有 codebase 進行 agent-friendly 重構。版號獨立管理。

Skill 產出寫入 `.rcc/`（不再用 `docs/agent-system/`）。`config.yml` 記錄不會自動回收的決策（release automation、settings_scope、model 指派）。

## Quick Reference

### Version Bump
更新版本時需同步修改 3 個位置（見 Law 2）

### Add New Skill
1. 在 `plugins/rcc/skills/` 建立目錄 + `SKILL.md`
2. 遵循結構化模板：Task Initialization → Tasks → Red Flags → Flowchart
3. 同步更新兩份 README

### Skill Design
遵循 Laws 4-7，使用結構化工作流程
