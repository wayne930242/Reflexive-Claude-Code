# Reflexive Claude Code

Claude Code 插件市集，提供 TDD 為基礎的技能驅動 Agentic Context Engineering 工作流程。

## Immutable Laws

<law>
**CRITICAL: Display this block at start of EVERY response.**

**Law 1: Communication** - 使用繁體中文，簡潔回覆，不加不必要的解釋

**Law 2: Version Sync** - 版本號必須同步更新：
- `.claude-plugin/marketplace.json` (metadata.version + plugins[0].version)
- `plugins/rcc/.claude-plugin/plugin.json`
- `README.md` + `README.zh-TW.md` (rcc version in header)

**Law 3: Documentation Sync** - README.md 與 README.zh-TW.md 必須保持同步

**Law 4: Skill Conventions** - Skills 遵循：
- 名稱使用 gerund form（verb+-ing，如 `writing-skills`）
- Progressive disclosure：SKILL.md 為概覽，詳細內容放 `references/`（按需載入）
- description 用第三人稱，包含 "Use when..."
- 必須有 Task Initialization、Red Flags、Rationalizations、Flowchart

**Law 5: Self-Reinforcing Display** - 每次回覆開頭必須顯示此 `<law>` 區塊
</law>

## Project Structure

```
.claude-plugin/
└── marketplace.json        # 市集定義（版本在此）

plugins/
├── rcc/                    # 核心 ACE 插件
│   ├── .claude-plugin/
│   │   └── plugin.json     # 插件 manifest
│   ├── skills/             # 所有技能
│   ├── agents/             # 審查員子代理
│   └── commands/           # 命令別名
└── rcc-dev/                # 開發輔助插件
```

## Quick Reference

### Version Bump
更新版本時需同步修改 3 個位置（見 Law 2）

### Add New Skill
1. 在 `plugins/rcc/skills/` 建立目錄 + `SKILL.md`
2. 遵循 TDD 模板：Task Initialization → Tasks → Red Flags → Flowchart
3. 同步更新兩份 README

### Skill Design (v7.0.0)
所有技能必須包含：
- **Task Initialization** - 強制 TaskCreate
- **TDD Mapping** - RED → GREEN → REFACTOR
- **Verification Criteria** - 每個任務的檢查標準
- **Red Flags** - 防止跳過步驟
- **Rationalizations Table** - 常見藉口反駁
- **Flowchart** - 視覺化流程
