# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

一個用於 Claude Code 的**技能驅動代理脈絡工程 (Agentic Context Engineering)** 工作流程。

## 核心理念

Agent 維護並重構自己的核心提示詞與 Agent 系統——而非外部文件或記憶庫。

**技能驅動代理脈絡工程**意味著：
- 每次任務開始前，Agent 會檢視技能庫中相關的能力
- 使用者透過 `/reflect` 等指令明確觸發學習點
- 透過刻意的教導，Agent 將學習成果整合到技能庫中
- 技能是抽象的、可重用的，並連結到包含範例和文件的參考目錄

## 插件

此市集提供兩個插件：

### ACE-core (v4.1.0)

核心 ACE 工作流程，包含反思、架構指導、模組化規則，以及撰寫工具。

**技能：**

| 技能 | 說明 | 觸發條件 |
|------|------|----------|
| `agent-architect` | 架構顧問，提供元件設計的整全指導 | "檢視架構..."、"幫我重構..." |
| `write-claude-md` | 使用 `<law>` 憲法建立 CLAUDE.md | "幫我寫 CLAUDE.md..."、"建立專案設定..." |
| `write-subagent` | 為 `.claude/agents/` 建立子代理配置 | "建立子代理..."、"設定程式碼審查代理..." |
| `write-skill` | 依照 Anthropic 官方模式建立有效的 SKILL.md 檔案 | "幫我寫一個技能..."、"建立一個新技能..." |
| `write-command` | 建立具有正確 YAML frontmatter 和參數處理的斜線指令 | "幫我寫一個指令..."、"建立一個斜線指令..." |
| `write-rules` | 為 `.claude/rules/` 建立慣例規則檔案 | "新增程式碼慣例..."、"建立規則..." |
| `write-hook` | 建立靜態分析與程式碼品質的 hook | "新增 linting hook..."、"設定型別檢查..." |

**指令：**

| 指令 | 說明 | 用法 |
|------|------|------|
| `/init-project` | 初始化新專案，包含框架、最佳實踐和代理人系統 | `/init-project [path]` |
| `/reflect` | 反思對話內容，分類學習成果，整合 | `/reflect [focus]` |
| `/refactor-skills` | 分析並整合所有技能——合併、優化、移除冗餘 | `/refactor-skills` |
| `/migration` | 遷移現有系統到最佳實踐架構 | `/migration [path]` |
| `/improve-skill` | 分析慣例與研究最佳實踐來優化技能 | `/improve-skill <skill-path>` |

### RCC-dev-helper (v1.0.0)

開發輔助工具，用於建立完整的 Claude Code 插件，包含 manifest、指令、技能和市集設定。

**技能：**

| 技能 | 說明 | 觸發條件 |
|------|------|----------|
| `write-plugin` | 建立完整的插件套件，包含 manifest、指令、技能和市集設定 | "建立一個插件..."、"把這個打包成插件..." |

**指令：**

| 指令 | 說明 | 用法 |
|------|------|------|
| `/create-plugin` | 建立新的 Claude Code 插件骨架 | `/create-plugin <name> [type]` |

## 元件架構

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Context                          │
├─────────────────────────────────────────────────────────────────┤
│  自動注入                          │  按需調用                   │
│  ─────────                         │  ─────────                  │
│  • CLAUDE.md（高層次）              │  • Skills（能力）           │
│  • .claude/rules/*.md（約束）       │  • Commands（使用者觸發）   │
│    └─ paths: 條件式觸發            │  • Subagents（隔離脈絡）    │
└─────────────────────────────────────────────────────────────────┘
```

| 元件 | 位置 | 觸發方式 | Token 影響 |
|------|------|----------|------------|
| **Rules** | `.claude/rules/*.md` | 自動注入 | 高（< 50 行） |
| **Skills** | `.claude/skills/*/SKILL.md` | Claude 決定 | 中（< 200 行） |
| **Commands** | `.claude/commands/*.md` | 使用者 `/command` | 低 |
| **Subagents** | `.claude/agents/*.md` | Task 工具 | 隔離 |
| **CLAUDE.md** | `.claude/CLAUDE.md` | 自動注入 | 高（< 300 行） |

## 核心憲法

CLAUDE.md 使用 `<law>` 區塊進行自我強化顯示：

| 法則 | 目的 |
|------|------|
| **Communication** | 簡潔、可執行的回覆 |
| **Skill Discovery** | 開始工作前檢查可用技能 |
| **Rule Consultation** | 檢查 `.claude/rules/` 的領域慣例 |
| **Parallel Processing** | 使用 Task 工具進行獨立操作 |
| **Reflexive Learning** | 發現重要事項時提醒使用者 `/reflect` |
| **Self-Reinforcing Display** | 每次回覆開頭顯示 `<law>` 區塊 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      工作階段                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. 任務開始前   │  檢視技能庫                                   │
│  2. 執行工作     │  正常工作即可                                 │
│  3. /reflect     │  分類 → 規則或技能 → 整合                     │
│  4. /refactor-*  │  整合與優化                                   │
└─────────────────────────────────────────────────────────────────┘
```

每個技能連結到一個目錄，包含：
- `SKILL.md` — 抽象指令（< 200 行）
- `references/` — 按需載入的詳細文件
- `scripts/` — 可執行的工具程式

## 安裝

```bash
# 從 GitHub 安裝
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install ACE-core@weihung-marketplace
# 或
/plugin install RCC-dev-helper@weihung-marketplace

# 從本機路徑安裝
/plugin install /path/to/Reflexive-Claude-Code
```

## 專案結構

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   ├── marketplace.json     # 市集定義
│   ├── ACE-core.json        # ACE-core 插件 manifest
│   └── RCC-dev-helper.json  # RCC-dev-helper 插件 manifest
├── commands/
│   ├── init-project.md      # ACE-core：專案初始化
│   ├── reflect.md           # ACE-core：階段反思
│   ├── refactor-skills.md   # ACE-core：技能整合
│   ├── migration.md         # ACE-core：系統遷移
│   ├── improve-skill.md     # ACE-core：技能優化
│   └── create-plugin.md     # RCC-dev-helper：插件建立
├── skills/
│   ├── agent-architect/     # ACE-core：架構顧問
│   ├── write-claude-md/     # ACE-core：建立 CLAUDE.md
│   ├── write-subagent/      # ACE-core：建立子代理
│   ├── write-skill/         # ACE-core：建立技能
│   ├── write-command/       # ACE-core：建立指令
│   ├── write-rules/         # ACE-core：建立規則
│   ├── write-hook/          # ACE-core：建立 hook
│   └── write-plugin/        # RCC-dev-helper：建立插件
└── README.md
```

## 啟發來源

本專案受到**代理脈絡工程 (Agentic Context Engineering, ACE)** 框架的啟發：

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

ACE 框架的模組化方法——**生成 → 反思 → 策展**——直接影響了本專案的技能驅動代理脈絡工程工作流程，由使用者明確觸發學習點，透過刻意的教導引導 Agent 的自我演化。

## 授權條款

MIT
