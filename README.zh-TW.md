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

## 技能

根據上下文自動啟用的能力。

| 技能 | 說明 | 觸發條件 |
|------|------|----------|
| `write-skill` | 依照 Anthropic 官方模式建立有效的 SKILL.md 檔案 | "幫我寫一個技能..."、"建立一個新技能..." |
| `write-command` | 建立具有正確 YAML frontmatter 和參數處理的斜線指令 | "幫我寫一個指令..."、"建立一個斜線指令..." |
| `write-plugin` | 建立完整的插件套件，包含 manifest、指令、技能和市集設定 | "建立一個插件..."、"把這個打包成插件..." |

## 指令

| 指令 | 說明 | 用法 |
|------|------|------|
| `/reflect` | 反思對話內容，萃取學習成果，整合到技能庫 | `/reflect [focus]` |
| `/refactor-skills` | 分析並整合所有技能——合併、優化、移除冗餘 | `/refactor-skills` |
| `/refactor-claude-md` | 以憲法機制重構 CLAUDE.md | `/refactor-claude-md [path] [mode]` |
| `/create-plugin` | 建立新的 Claude Code 插件骨架 | `/create-plugin <name> [type]` |

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                      工作階段                            │
├─────────────────────────────────────────────────────────┤
│  1. 任務開始前   │  檢視技能庫                           │
│  2. 執行工作     │  正常工作即可                         │
│  3. /reflect     │  萃取學習成果 → 技能                  │
│  4. /refactor-skills│  整合與優化                        │
└─────────────────────────────────────────────────────────┘
```

每個技能連結到一個目錄，包含：
- `SKILL.md` — 抽象指令
- `references/` — 詳細文件、程式碼範例
- `scripts/` — 可執行的工具程式

## 安裝

```bash
# 從 GitHub 安裝
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install Reflexive-Claude-Code@wayne930242

# 從本機路徑安裝
/plugin install /path/to/Reflexive-Claude-Code
```

## 專案結構

```
Reflexive-Claude-Code/
├── commands/
│   ├── reflect.md           # 核心：階段反思
│   ├── refactor-skills.md   # 核心：技能整合
│   ├── refactor-claude-md.md
│   └── create-plugin.md
├── skills/
│   ├── write-skill/         # 元技能：建立技能
│   ├── write-command/
│   └── write-plugin/
└── .claude-plugin/
```

## 啟發來源

本專案受到**代理脈絡工程 (Agentic Context Engineering, ACE)** 框架的啟發：

> Zhang, Q., Hu, C., Upasani, S., Ma, B., Hong, F., Kamanuru, V., Rainton, J., Wu, C., Ji, M., Li, H., Thakker, U., Zou, J., & Olukotun, K. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618. https://arxiv.org/abs/2510.04618

ACE 框架的模組化方法——**生成 → 反思 → 策展**——直接影響了本專案的技能驅動代理脈絡工程工作流程，由使用者明確觸發學習點，透過刻意的教導引導 Agent 的自我演化。

## 授權條款

MIT
