# Agent System 技能分解設計

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 將 `migrating-agent-systems` 拆分為 5 個專責技能，並改造 3 個調用方技能消除重複

**Architecture:** 鏈式調用架構，每個技能產出文件作為下一個的輸入。分析先行，brainstorm 可跳過已知問題。所有 `.claude/` 寫入必須由主對話執行，subagent 僅限唯讀分析。

**Tech Stack:** Claude Code skills (SKILL.md + references/)

---

## 背景

### 問題

`migrating-agent-systems` 是一個 monolithic 技能，包含 7 個 tasks 涵蓋從探索到驗證的全流程。這導致：
- 無法單獨使用分析或重構功能
- `refactoring-skills` 重複實作分析邏輯
- 沒有工作流探索（假設使用者是開發者）
- 無弱點檢測機制

### 約束

| 約束 | 說明 |
|---|---|
| `.claude/` 寫入限制 | Subagent 無法自主寫入 `.claude/` 目錄，需使用者核准 prompt |
| Subagent 角色 | 僅用於唯讀分析（reviewer、探索），不可用於撰寫 |
| CLAUDE.md 格式 | 使用官方建議的純 markdown 格式，不使用 `<law>` 標籤 |
| 鏈式調用 | 每步結束自動提示銜接下一步 |
| 產出物路徑 | `docs/agent-system/{timestamp}-{type}.md` |

---

## 完整流程

```
[使用者觸發]
    │
    ├─ "setup agent" / "migrate agent system"
    │   → migrating-agent-systems (路由器)
    │       ├─ 偵測到 .claude/ 存在 → analyzing-agent-systems
    │       └─ 全新專案 → brainstorming-workflows
    │
    ├─ "initialize project" / "new project"
    │   → initializing-projects
    │       └─ Task 6 → brainstorming-workflows
    │
    └─ "refactor skills" / "cleanup skills"
        → refactoring-skills
            └─ Task 2 → analyzing-agent-systems
```

### 鏈式流程

```
analyzing-agent-systems ──報告弱點──→ 使用者確認
        │
brainstorming-workflows ──帶入弱點，問是否修補──→ 探索工作流 ──→ 工作流摘要
        │
planning-agent-systems ──根據分析+摘要規劃元件──→ 元件計畫
        │
applying-agent-systems ──調用 writing-* 技能建立元件──→ 元件就緒
        │
refactoring-agent-systems ──review + 清理──→ 完成
```

---

## 新技能設計

### 技能 0: `analyzing-agent-systems`

**職責：** 掃描並分析現有 agent system 元件，檢測弱點，產出分析報告

**觸發：** "分析 agent system"、"檢查設定"，或由 `migrating-agent-systems`、`refactoring-skills` 調用

**Tasks：**

1. **掃描元件** — 找出所有 agent system 元件
   - `CLAUDE.md`（constitution）
   - `.claude/rules/`（conventions）
   - `.claude/settings.json`（hooks）
   - `.claude/skills/` 或 plugin skills
   - `.claude/agents/` 或 subagents

2. **弱點分析** — 8 類弱點檢測

   | 類別 | 檢查項目 |
   |---|---|
   | 路由/觸發 | description 模糊、觸發條件重疊、無 fallback 策略、route 飽和（>20 skills） |
   | 上下文管理 | reviewer 沒有 `context: fork` 隔離、CLAUDE.md 過載（>200行）、reference 未按需載入 |
   | 工作流連貫性 | 技能鏈斷裂點、缺少驗證閘門、無錯誤恢復路徑、ReAct 步驟過多 |
   | 重複/衝突 | 技能功能重疊、rule 與 CLAUDE.md 矛盾、跨層重複邏輯 |
   | 安全性 | 缺少敏感檔案保護 hook、subagent 權限未限縮（用 subagent 寫 .claude/） |
   | 可觀測性 | 無結構化日誌、路由決策不透明 |
   | 架構擴展 | 錯誤放大風險、協調開銷過大、flat topology |
   | 憲法穩定性 | CLAUDE.md 長對話侵蝕、指令與任務衝突、無版本控制 |

3. **產出分析報告** — 寫入 `docs/agent-system/{timestamp}-analysis.md`
   - 元件清單 + 狀態（符合/需修改/缺失）
   - 弱點列表（嚴重度：critical/warning/info）
   - 建議改善方向

4. **報告給使用者** — 呈現弱點摘要，等使用者確認

**銜接：** 使用者確認後 → 「要繼續進行工作流探索嗎？」→ 調用 `brainstorming-workflows`，傳入分析報告路徑

**References：**
- `references/weakness-checklist.md` — 8 類弱點的完整檢查清單與範例

---

### 技能 1: `brainstorming-workflows`

**職責：** 模板引導使用者選擇角色，探索工作流程，產出工作流摘要

**觸發：** 由 `analyzing-agent-systems` 銜接調用，或使用者說 "explore workflows"、"setup agent"（全新專案）

**Tasks：**

1. **帶入分析結果（如有）** — 讀取分析報告，先問使用者：
   - 「分析發現以下弱點，是否要在這次一併修補？」
   - 使用者確認要修補的項目 → 記錄到工作流摘要

2. **角色選擇** — 提供角色模板：

   | 角色 | 典型工作流 |
   |---|---|
   | **軟體開發者** | 寫程式、跑測試、code review、CI/CD、部署 |
   | **專案管理者** | 追蹤任務、寫報告、排程、溝通協調 |
   | **內容創作者** | 寫文件、翻譯、發布、社群管理 |
   | **資料分析師** | 資料處理、視覺化、報告產出、自動化分析 |
   | **營運/DevOps** | 監控、部署、事件回應、基礎設施管理 |
   | **自定義** | 使用者自行描述 |

   使用者選擇最接近的角色後，針對性深入。

3. **工作流探索** — 根據角色，一次問一個問題：
   - 「你日常最常做的 3 件事是什麼？」
   - 「哪些任務你希望自動化？」
   - 「有沒有經常重複但容易出錯的流程？」
   - 「你需要遵守的團隊規範有哪些？」
   - 如果分析已覆蓋某些問題 → 跳過對應問題

4. **產出工作流摘要** — 寫入 `docs/agent-system/{timestamp}-workflows.md`
   - 使用者角色
   - 核心工作流列表
   - 需自動化的任務
   - 需修補的弱點（從分析帶入）
   - 需遵守的規範

**銜接：** 「工作流摘要完成。要繼續規劃 agent system 元件嗎？」→ 調用 `planning-agent-systems`

---

### 技能 2: `planning-agent-systems`

**職責：** 根據分析報告 + 工作流摘要，規劃要建立/修改的元件

**觸發：** 由 `brainstorming-workflows` 銜接調用

**Tasks：**

1. **讀取輸入** — 讀取分析報告（如有）和工作流摘要

2. **元件規劃** — 對每種元件決定動作：

   | 元件 | 來源依據 | 決策 |
   |---|---|---|
   | CLAUDE.md | 工作流摘要中的規範 + 分析中的憲法弱點 | 建立/修改/保留 |
   | Rules | 工作流中的慣例 + 分析中的路徑匹配 | 建立哪些 rule、scope |
   | Hooks | 工作流中需自動化的品質檢查 | 建立哪些 hook、事件 |
   | Skills | 工作流中重複的任務 | 建立哪些 skill |
   | Agents | 需要隔離的分析任務 | 建立哪些 subagent（唯讀） |

3. **技能複用分析** — 檢查現有 rcc 技能是否可複用：
   - 已有 `writing-claude-md` → 不重建 CLAUDE.md 撰寫邏輯
   - 已有 `writing-rules` → 不重建 rule 撰寫邏輯
   - 已有 `writing-hooks` → 不重建 hook 撰寫邏輯
   - 已有 `writing-skills` → 不重建 skill 撰寫邏輯

4. **產出元件計畫** — 寫入 `docs/agent-system/{timestamp}-plan.md`
   - 每個元件的：動作（建立/修改/刪除）、內容摘要、使用的 writing-* 技能
   - 執行順序（CLAUDE.md → rules → hooks → skills → agents）
   - 預期的弱點修補效果

5. **使用者確認** — 呈現計畫，等使用者核准

**銜接：** 使用者確認後 → 「計畫已確認。要開始建立元件嗎？」→ 調用 `applying-agent-systems`

---

### 技能 3: `applying-agent-systems`

**職責：** 根據計畫逐一調用 writing-* 技能建立元件

**觸發：** 由 `planning-agent-systems` 銜接調用

**Tasks：**

1. **讀取元件計畫**

2. **依序執行** — 按計畫順序，對每個元件：
   - 調用對應的 writing-* 技能（主對話直接執行，不委派 subagent）
   - 驗證元件建立成功
   - 標記完成

   | 元件 | 調用技能 |
   |---|---|
   | CLAUDE.md | `writing-claude-md` |
   | Rules | `writing-rules`（每條 rule 各調用一次） |
   | Hooks | `writing-hooks`（每個 hook 各調用一次） |
   | Skills | `writing-skills`（每個 skill 各調用一次） |
   | Agents | `writing-subagents`（每個 agent 各調用一次） |

3. **驗證系統** — 所有元件建立後：
   - CLAUDE.md 存在且 < 200 行
   - Rules 有正確的 paths 設定
   - Hooks 可正常執行（exit code 0/2）
   - Skills 符合結構規範

**銜接：** 「所有元件已建立。要進行 review 和重構嗎？」→ 調用 `refactoring-agent-systems`

**CRITICAL：** 所有寫入操作必須由主對話執行。不可使用 subagent 調用 writing-* 技能。

---

### 技能 4: `refactoring-agent-systems`

**職責：** Review 完成的 agent system，清理重複/衝突/弱點

**觸發：** 由 `applying-agent-systems` 銜接調用，或使用者說 "review agent system"、"cleanup agent system"

**Tasks：**

1. **調用 `analyzing-agent-systems`** — 重新掃描分析，取得最新狀態

2. **比對改善** — 對比 applying 前後的分析報告：
   - 哪些弱點已修補？
   - 哪些弱點仍存在？
   - 是否引入新問題？

3. **執行重構** — 針對殘留問題：
   - 重複邏輯 → 合併或抽取為 rule
   - 衝突指令 → 統一或移除
   - 過度設計 → 簡化（YAGNI）
   - 弱觸發 → 改善 description

4. **最終驗證** — 再跑一次 `analyzing-agent-systems`，確認無 critical 弱點

5. **產出重構報告** — 寫入 `docs/agent-system/{timestamp}-refactoring-report.md`

**CRITICAL：** 重構中的寫入操作同樣必須由主對話執行。Subagent 僅用於分析。

---

## 調用方改造

### `migrating-agent-systems` → 瘦身為路由器

**改造前：** 7 個 tasks，自己做全部
**改造後：** 2 個 tasks

1. **偵測現有系統** — 檢查 `.claude/` 是否存在
2. **路由** —
   - 有現有系統 → 調用 `analyzing-agent-systems`（鏈式自動往下走）
   - 全新專案 → 調用 `brainstorming-workflows`（鏈式自動往下走）

保留現有觸發詞："setup agent", "migrate agent system", "configure claude code"

### `initializing-projects` → Task 6 改調用鏈

**改造前：** Task 6 調用 `migrating-agent-systems`
**改造後：** Task 6 改為：
- 全新專案（必然），直接調用 `brainstorming-workflows`
- 鏈式自動往下走到 `applying-agent-systems`

### `refactoring-skills` → Task 2 委託分析

**改造前：** Task 1-2 自己做 discover + analyze
**改造後：**
- Task 1 保留 discover（找 skills）
- Task 2 改為調用 `analyzing-agent-systems` 取得分析報告
- Task 3-6 保留（execute refactoring、extract conventions、validate、report）
- 分析報告中的弱點信息輔助 Task 3 的重構決策

---

## 檔案異動總覽

### 新增（5 個技能目錄）

```
plugins/rcc/skills/
├── analyzing-agent-systems/
│   ├── SKILL.md
│   └── references/
│       └── weakness-checklist.md
├── brainstorming-workflows/
│   ├── SKILL.md
│   └── references/
│       └── role-templates.md
├── planning-agent-systems/
│   └── SKILL.md
├── applying-agent-systems/
│   └── SKILL.md
└── refactoring-agent-systems/
    └── SKILL.md
```

### 修改（3 個現有技能）

```
plugins/rcc/skills/
├── migrating-agent-systems/SKILL.md  ← 瘦身為路由器
├── initializing-projects/SKILL.md    ← Task 6 改調用鏈
└── refactoring-skills/SKILL.md       ← Task 2 委託分析
```

### 其他

- `README.md` + `README.zh-TW.md` — 更新技能清單
- `.claude-plugin/marketplace.json` + `plugins/rcc/.claude-plugin/plugin.json` — 版本號更新
