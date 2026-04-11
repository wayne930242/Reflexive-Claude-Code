# Reflexive Claude Code

[English](README.md) | [繁體中文](README.zh-TW.md)

Claude Code 插件市集，提供**技能驅動的代理脈絡工程 (Agentic Context Engineering, ACE)** — 以結構化工作流程建立、分析、維護 agent 系統。

## 功能簡介

Reflexive Claude Code 讓 Claude Code 擁有一套完整的 agent 系統管理工具：CLAUDE.md、rules、skills、subagents、hooks。每個元件都遵循結構化創建流程並搭配自動品質審查。

**核心能力：**

- **從零建立 agent 系統** — 偵測專案成熟度、探索工作流、規劃架構，再依相依順序建立所有元件
- **分析既有系統** — 11 類弱點檢查清單，涵蓋路由、context 管理、安全性、rules 健康度、跨工具遷移
- **即時驗證** — PostToolUse hook 在每次編輯 skill、agent、rule 檔案時檢查 frontmatter、壞連結、孤立檔案
- **品質閘門** — 5 個專用 reviewer agent（skill、CLAUDE.md、rule、hook、subagent）在每次建立或修改後執行
- **先進安全架構** — AI 特化安全模式、八層防禦體系、30 秒效能約束、智能反思驅動學習機制

## 安裝

```bash
/plugin marketplace add wayne930242/Reflexive-Claude-Code
/plugin install rcc@rcc
```

## 運作方式

### Agent System Pipeline

完整 pipeline 有 6 個階段，各由專門的 skill 負責：

```
migrate → analyze → brainstorm → plan → apply → review → refactor
```

| 階段 | Skill | 功能 |
|------|-------|------|
| **遷移** | `migrating-agent-systems` | 偵測成熟度（None/Seed/Partial/Established），提出 rules 重構建議，路由至正確鏈 |
| **分析** | `analyzing-agent-systems` | 掃描所有元件，執行 11 類弱點清單，產出 Rules Health Summary |
| **探索** | `brainstorming-workflows` | 複雜度階梯（L1-L6）探索工作流，對應 Anthropic 模式 |
| **規劃** | `planning-agent-systems` | 先畫架構流程圖，再依相依性排序元件計畫 |
| **執行** | `applying-agent-systems` | 依序呼叫 writing-* skills：CLAUDE.md → rules → hooks → skills → agents |
| **審查** | `reviewing-agent-systems` | 執行全部 5 個 reviewer agent，產出結構化報告 |

### 品質檢查

**11 類弱點分析**（透過 `analyzing-agent-systems`）：

| # | 類別 | 主要檢查項 |
|---|------|-----------|
| 1 | 路由 / 觸發 | 模糊描述、重疊觸發、缺失 handoff |
| 2 | Context 管理 | CLAUDE.md 過大、急切載入、context 污染 |
| 3 | 工作流連續性 | 斷裂鏈、缺少驗證閘門 |
| 4 | 冗餘 / 衝突 | 重複規則、矛盾指令 |
| 5 | 安全 | 未保護敏感檔案、過度權限 |
| 6 | 可觀測性 | 缺少結構化輸出、不透明路由 |
| 7 | 架構 / 擴展 | 扁平拓撲、過度編排 |
| 8 | Constitution 穩定性 | CLAUDE.md 含程序、模糊指令 |
| 9 | 專案脈絡完整度 | 缺少部署文件、語言覆蓋率缺口 |
| 10 | 跨工具遷移 | 未匯入 `.cursorrules`、copilot instructions |
| 11 | Rules 健康度 | 行數 > 50、缺少 `paths:`、dead glob、session-start > 300 行 |

**Rules Health Summary**（分析時產出）：

| 指標 | 閾值 |
|------|------|
| CLAUDE.md 行數 | > 200 = 警告 |
| Session-start 總計（CLAUDE.md + global rules） | > 300 = 警告 |
| 單一 rule 行數 | > 50 = 警告 |
| 有 `paths:` 但匹配 0 個檔案 | dead glob |
| rules 含程序性內容 | 應抽成 skill |

**即時驗證 hook**（`validate_frontmatter.py`）：
- 每次 Edit/Write skill、agent 或 rule 檔案時觸發
- 依官方規格檢查無效 frontmatter 欄位
- 偵測 skill 目錄中的壞連結和孤立檔案
- 輸出 `additionalContext` 讓 Claude 立即自我修正

### 元件撰寫 Skills

每個 `writing-*` skill 遵循結構化流程並搭配 reviewer 閘門：

| Skill | 建立 | Reviewer |
|-------|------|----------|
| `writing-claude-md` | `CLAUDE.md` | `claudemd-reviewer` |
| `writing-rules` | `.claude/rules/*.md` | `rule-reviewer` |
| `writing-hooks` | `.claude/hooks/*` | `hook-reviewer` |
| `writing-skills` | `.claude/skills/*/SKILL.md` | `skill-reviewer` |
| `writing-subagents` | `.claude/agents/*.md` | `subagent-reviewer` |

### Plugin Pipeline

獨立的 pipeline 用於建立和維護 Claude Code 插件：

```
migrate-plugin → validate → refactor
                 ↑
        （或）從零建立 / 從腳本專案轉換
```

| 成熟度 | 偵測 | 路由 |
|--------|------|------|
| **None** | 沒有 `.claude-plugin/` | → `creating-plugins`（從零開始） |
| **Pre-plugin** | 腳本專案，無 plugin 結構 | → 提出轉換建議 → `creating-plugins`（帶 proposal） |
| **Minimal** | 有 manifest，缺元件 | → `validating-plugins` → `refactoring-plugins` |
| **Complete** | 完整插件 | → `validating-plugins` → `refactoring-plugins` |

### Skill 資產

每個 skill 可打包三種輔助資產：

| 目錄 | 角色 | 範例 |
|------|------|------|
| `references/` | 按需載入的文件 | 清單、模式目錄 |
| `scripts/` | 可執行的自動化腳本 | Scaffolder、驗證器 |
| `templates/` | 可重用的檔案骨架 | 報告格式、設定檔 |

規劃器決定每個 skill 需要哪些資產；審查器檢查是否存在；重構器直接建立缺少的資產。

### 模型建議

| 使用場景 | 模型 |
|---------|------|
| 實作、程式碼產生 | `sonnet` |
| 規劃、架構設計 | `opus` |
| 唯讀分析、審查 | `sonnet` |
| 簡單查詢、探索 | `haiku` |

## 完整 Skill 列表

### rcc (v10.0.0)

| Skill | 用途 |
|-------|------|
| `migrating-agent-systems` | 成熟度分級路由 + rules 重構建議 |
| `migrating-plugins` | 偵測插件成熟度（None/Pre-plugin/Minimal/Complete），腳本轉插件 |
| `analyzing-agent-systems` | 專案掃描 + 11 類弱點偵測 + 可執行的重構建議 |
| `brainstorming-workflows` | 針對性探索 pipeline 模式、痛點、例行任務 |
| `planning-agent-systems` | 架構優先規劃 + 相依排序 |
| `applying-agent-systems` | 透過 writing-* 鏈執行元件計畫 |
| `reviewing-agent-systems` | 執行全部 5 個 reviewer agent |
| `refactoring-agent-systems` | 依 review 報告修正問題 |
| `writing-skills` | 結構化技能建立 |
| `writing-claude-md` | 標準格式 CLAUDE.md |
| `writing-subagents` | 含 model/isolation 指南的 subagent 設定 |
| `writing-rules` | 含決策樹和內容驗證的 rules |
| `writing-hooks` | 靜態分析和品質閘門的 hooks |
| `reflecting` | 擷取學習成果，路由至 skills 或 rules |
| `improving-skills` | 優化單一 skill |
| `refactoring-skills` | 跨 skill 整合與去重 |
| `advising-architecture` | 分類知識類型、驗證方法 |
| `initializing-projects` | 從零建立專案 + agent 系統 |
| `creating-plugins` | 建立新 Claude Code 插件骨架 |
| `refactoring-plugins` | 依官方最佳實踐檢查插件健康度 |
| `validating-plugins` | 批次掃描所有插件檔案錯誤 |

## 專案結構

```
Reflexive-Claude-Code/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── rcc/
│       ├── skills/          # 21 個 skills
│       ├── agents/          # 5 個 reviewer subagents
│       └── hooks/           # Frontmatter 驗證 hook
└── README.md
```

## 致謝

- **[superpowers](https://github.com/anthropics/claude-code-superpowers)** — TDD 技能設計與紀律強制模式改編自 Anthropic 的 superpowers 插件。
- **代理脈絡工程 (Agentic Context Engineering, ACE)**：
  > Zhang, Q., et al. (2025). *Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models*. arXiv:2510.04618.

## 授權條款

MIT
