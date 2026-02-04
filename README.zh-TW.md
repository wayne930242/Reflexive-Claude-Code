# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

一個用於 Claude Code 的**技能驅動代理脈絡工程 (Agentic Context Engineering)** 工作流程。

## 核心理念

Agent 維護並重構自己的核心提示詞與 Agent 系統——而非外部文件或記憶庫。

**技能驅動代理脈絡工程**意味著：
- 每次任務開始前，Agent 會檢視技能庫中相關的能力
- 使用者透過 `reflecting` 等技能明確觸發學習點
- 透過刻意的教導，Agent 將學習成果整合到技能庫中
- 技能是抽象的、可重用的，並連結到包含範例和文件的參考目錄

## 插件

此市集提供兩個插件：

### rcc (v6.0.3)

核心 ACE 工作流程，包含反思、架構指導、模組化規則，以及技能撰寫工具。

**技能：**

| 技能 | 說明 |
|------|------|
| `agent-architect` | 架構顧問，提供元件設計的整全指導 |
| `project-discovery` | 深度專案分析，用於架構規劃 |
| `writing-skills` | 依照 Anthropic 官方模式建立有效的 SKILL.md 檔案 |
| `writing-claude-md` | 使用 `<law>` 憲法建立 CLAUDE.md |
| `writing-subagents` | 為 `.claude/agents/` 建立子代理配置 |
| `writing-rules` | 為 `.claude/rules/` 建立慣例規則檔案 |
| `writing-hooks` | 建立靜態分析與程式碼品質的 hook |
| `reflecting` | 反思對話內容，分類學習成果，整合 |
| `improving-skills` | 分析慣例與研究最佳實踐來優化技能 |
| `refactoring-skills` | 分析並整合所有技能——合併、優化、移除冗餘 |
| `hunting-skills` | 透過 claude-skills-mcp 搜尋外部技能，轉化為專案技能 |
| `refactoring-with-external-skills` | 使用外部技能模式重構現有技能 |
| `adding-laws` | 新增法則到 CLAUDE.md 憲法 |
| `initializing-projects` | 初始化新專案，包含框架、最佳實踐和代理人系統 |
| `migrating-agent-systems` | 遷移現有系統到最佳實踐架構 |

### rcc-dev (v2.0.1)

開發輔助工具，用於建立完整的 Claude Code 插件，包含 manifest、技能和市集設定。

**技能：**

| 技能 | 說明 |
|------|------|
| `writing-plugins` | 建立完整的插件套件，包含 manifest、技能和市集設定 |
| `creating-plugins` | 建立新的 Claude Code 插件骨架 |

## 元件架構

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Context                          │
├─────────────────────────────────────────────────────────────────┤
│  自動注入                          │  按需調用                   │
│  ─────────                         │  ─────────                  │
│  • CLAUDE.md（高層次）              │  • Skills（能力）           │
│  • .claude/rules/*.md（約束）       │  • Subagents（隔離脈絡）    │
│    └─ paths: 條件式觸發            │                             │
└─────────────────────────────────────────────────────────────────┘
```

| 元件 | 位置 | 觸發方式 | Token 影響 |
|------|------|----------|------------|
| **Rules** | `.claude/rules/*.md` | 自動注入 | 高 |
| **Skills** | `.claude/skills/*/SKILL.md` | Claude 決定 | 漸進式揭露 |
| **Subagents** | `.claude/agents/*.md` | Task 工具 | 隔離 |
| **CLAUDE.md** | `./CLAUDE.md` | 自動注入 | 高 |

## 核心憲法

CLAUDE.md 使用 `<law>` 區塊進行自我強化顯示：

| 法則 | 目的 |
|------|------|
| **Communication** | 簡潔、可執行的回覆 |
| **Skill Discovery** | 開始工作前檢查可用技能 |
| **Rule Consultation** | 檢查 `.claude/rules/` 的領域慣例 |
| **Parallel Processing** | 使用 Task 工具進行獨立操作 |
| **Reflexive Learning** | 發現重要事項時提醒使用者反思 |
| **Self-Reinforcing Display** | 每次回覆開頭顯示 `<law>` 區塊 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      工作階段                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. 任務開始前   │  檢視技能庫                                   │
│  2. 執行工作     │  正常工作即可                                 │
│  3. 反思         │  分類 → 規則或技能 → 整合                     │
│  4. 重構         │  整合與優化                                   │
└─────────────────────────────────────────────────────────────────┘
```

每個技能連結到一個目錄，包含：
- `SKILL.md` — 抽象指令（漸進式揭露）
- `references/` — 按需載入的詳細文件
- `scripts/` — 可執行的工具程式

## 安裝

```bash
# 從 GitHub 安裝
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install rcc@rcc
# 或
/plugin install rcc-dev@rcc

# 從本機路徑安裝
/plugin install /path/to/Reflexive-Claude-Code/plugins/rcc
```

## 專案結構

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   └── marketplace.json     # 市集定義
├── plugins/
│   ├── rcc/                 # Core ACE 插件
│   └── rcc-dev/             # 開發輔助插件
├── skills/
│   ├── agent-architect/     # ACE-core：架構顧問
│   ├── project-discovery/   # ACE-core：專案分析
│   ├── writing-skills/      # ACE-core：建立技能
│   ├── writing-claude-md/   # ACE-core：建立 CLAUDE.md
│   ├── writing-subagents/   # ACE-core：建立子代理
│   ├── writing-rules/       # ACE-core：建立規則
│   ├── writing-hooks/       # ACE-core：建立 hook
│   ├── reflecting/          # ACE-core：階段反思
│   ├── improving-skills/    # ACE-core：技能優化
│   ├── refactoring-skills/  # ACE-core：技能整合
│   ├── hunting-skills/      # ACE-core：外部技能獵取
│   ├── refactoring-with-external-skills/  # ACE-core：使用外部技能重構
│   ├── adding-laws/         # ACE-core：新增憲法法則
│   ├── initializing-projects/  # ACE-core：專案初始化
│   ├── migrating-agent-systems/  # ACE-core：系統遷移
│   ├── writing-plugins/     # RCC-dev-helper：建立插件
│   └── creating-plugins/    # RCC-dev-helper：插件建立骨架
└── README.md
```

## 啟發來源

本專案受到**代理脈絡工程 (Agentic Context Engineering, ACE)** 框架的啟發：

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

ACE 框架的模組化方法——**生成 → 反思 → 策展**——直接影響了本專案的技能驅動代理脈絡工程工作流程，由使用者明確觸發學習點，透過刻意的教導引導 Agent 的自我演化。

## 授權條款

MIT
