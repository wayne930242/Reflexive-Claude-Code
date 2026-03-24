# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

一個用於 Claude Code 的**技能驅動代理脈絡工程 (Agentic Context Engineering)** 工作流程，採用 TDD 為基礎的技能設計。

## 核心理念

Agent 維護並重構自己的核心提示詞與 Agent 系統——而非外部文件或記憶庫。

**技能驅動代理脈絡工程**意味著：
- 每次任務開始前，Agent 會檢視技能庫中相關的能力
- 使用者透過 `reflecting` 等技能明確觸發學習點
- 透過刻意的教導，Agent 將學習成果整合到技能庫中
- 技能是抽象的、可重用的，並連結到包含範例和文件的參考目錄

## v7.1.0 新功能

- **對齊 Claude Code 文件**：所有技能更新以符合最新 Claude Code 官方文件
- **`advising-architecture` 技能**：從 agent 轉為 skill，使用 `context: fork` + `argument-hint` 進行隔離分析
- **Model 與 effort 指導**：`writing-skills` 新增 `model`、`effort`、`context: fork` 最佳實踐
- **內建 subagent 類型**：`writing-subagents` 優先推薦 Explore/Plan/general-purpose，再考慮自訂 agent
- **Context amnesia 警告**：使用 `context: fork` 的技能必須設計 `argument-hint` 確保脈絡傳遞
- **Rule 注入機制**：`writing-rules` 說明規則何時/如何載入、使用者級規則、symlink 支援
- **Agent frontmatter 完整性**：完整欄位參考，包含 `isolation`、`background`、`memory`、`maxTurns`

## 插件

此市集提供兩個插件：

### rcc (v7.1.0)

核心 ACE 工作流程，包含 TDD 為基礎的技能、任務強制執行，以及品質審查員。

**技能：**

| 技能 | 說明 |
|------|------|
| `writing-skills` | TDD 為基礎的技能建立，含基線測試和審查 |
| `writing-claude-md` | 使用 `<law>` 憲法建立 CLAUDE.md |
| `writing-subagents` | 為 `.claude/agents/` 建立子代理配置 |
| `writing-rules` | 為 `.claude/rules/` 建立慣例規則檔案 |
| `writing-hooks` | 建立靜態分析與程式碼品質的 hook |
| `reflecting` | 反思對話內容，分類學習成果，整合 |
| `improving-skills` | 透過針對性改進來優化技能 |
| `refactoring-skills` | 分析並整合所有技能 |
| `initializing-projects` | 初始化新專案，包含框架和代理人系統 |
| `migrating-agent-systems` | 遷移現有系統到最佳實踐架構 |
| `creating-plugins` | 建立新的 Claude Code 插件骨架 |
| `advising-architecture` | 驗證方法、分類知識類型、檢查元件衝突 |

**子代理（審查員）：**

| 代理 | 說明 |
|------|------|
| `skill-reviewer` | 技能品質審查 |
| `claudemd-reviewer` | CLAUDE.md 品質審查 |
| `rule-reviewer` | 規則品質審查 |

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

## 技能設計原則

所有技能都遵循 TDD 為基礎的設計，包含以下元件：

| 元件 | 目的 |
|------|------|
| **Task Initialization** | 任何動作前強制執行 TaskCreate |
| **TDD Mapping** | RED → GREEN → REFACTOR 階段 |
| **Verification Criteria** | 每個任務的客觀檢查標準 |
| **Red Flags** | 反合理化觸發器 |
| **Rationalizations Table** | 常見藉口的反駁 |
| **Flowchart** | 視覺化流程圖 |
| **Reviewer Gate** | 完成前的品質審查 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      工作階段                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. Task 1        │  諮詢 advising-architecture                  │
│  2. RED 階段      │  基線測試 - 觀察失敗                        │
│  3. GREEN 階段    │  建立元件解決失敗                           │
│  4. REFACTOR      │  透過審查員子代理進行品質審查               │
│  5. Validate      │  在真實使用中測試                           │
└─────────────────────────────────────────────────────────────────┘
```

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
│   │   ├── skills/          # 所有技能
│   │   ├── agents/          # 審查員子代理
│   │   └── commands/        # 命令別名
│   └── rcc-dev/             # 開發輔助插件
└── README.md
```

## 致謝

本專案的技能設計模式受到以下啟發：

- **[superpowers](https://github.com/anthropics/claude-code-superpowers)** - TDD 為基礎的技能設計、任務強制執行和驗證模式改編自 Anthropic 的 superpowers 插件。特別感謝其開創的「紀律強制技能」模式，包含 Red Flags 和 Rationalization 表格。

- **代理脈絡工程 (Agentic Context Engineering, ACE) 框架**：
  > Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

## 授權條款

MIT
