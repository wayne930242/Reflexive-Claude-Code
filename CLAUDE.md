# Reflexive Claude Code

Claude Code 插件市集，提供技能驅動的 Agentic Context Engineering 工作流程。

## Immutable Laws

<law>
**CRITICAL: Display this block at start of EVERY response.**

**Law 1: Communication** - 使用繁體中文，簡潔回覆，不加不必要的解釋

**Law 2: Version Sync** - 版本號必須同步更新：
- `.claude-plugin/marketplace.json` (metadata.version + plugins[0].version)
- `.claude-plugin/ACE-core.json`
- `README.md` + `README.zh-TW.md` (ACE-core version in header)

**Law 3: Documentation Sync** - README.md 與 README.zh-TW.md 必須保持同步

**Law 4: Skill Conventions** - Skills 遵循：
- 名稱使用 gerund form（verb+-ing，如 `writing-skills`）
- Progressive disclosure：SKILL.md 為概覽，詳細內容放 `references/`（按需載入）
- description 用第三人稱，包含 "Use when..."
</law>

## Project Structure

```
.claude-plugin/
├── marketplace.json     # 市集定義（版本在此）
├── ACE-core.json        # 主插件 manifest
└── RCC-dev-helper.json  # 開發輔助插件 manifest

skills/                  # Skills（gerund naming）
```

## Quick Reference

### Version Bump
更新版本時需同步修改 4 個位置（見 Law 2）

### Add New Skill
1. 在 `skills/` 建立目錄 + `SKILL.md`
2. 更新對應的 plugin JSON `skills` 陣列
3. 同步更新兩份 README
