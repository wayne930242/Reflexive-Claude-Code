# 反思輕量化 + 架構精簡 改版計畫

**日期：** 2026-06-26
**範圍：** 反思機制重寫（建議制兩段式）+ 架構精簡（移除對 AI 價值低的指引）
**決策來源：** 使用者選定「建議制兩段式」「反思 + 架構精簡一起」「四項全部精簡」

## 目標

1. 反思從「全量納入 + 自動落地」改為「建議候選 + 使用者挑選 + 輕量落地」。
2. 移除對 AI 價值低或重複的指引：skill flowchart、`memory-manager.py`、重複的反思 skill、Law 7 強制四大 section。

## 現況盤點

| 項目 | 現況 | 問題 |
|------|------|------|
| `reflecting` | 314 行 / 6 tasks | 強制 TaskCreate 6 項、≥3 events、router Glob trace、7 欄 learning、reviewer 逐項審、自動路由 planning 建 component |
| `learning-from-failures` | 237 行 / 5 tasks + 511 行 Python | 與 reflecting 的 error/safety_bypass 分析重疊；用 Python script 自管 memory，與 reflecting「靠內建 memory」宣稱矛盾 |
| flowchart | 23 個 skill 有 graphviz `digraph` | 文字步驟已涵蓋，dot 圖對 AI 冗餘 |
| TaskCreate 樣板 | 24 個 skill 全有 `Task Initialization (MANDATORY)` | 短流程不需開頭強制建 N task |
| Law 7 | CLAUDE.md 強制每 skill 四大 section | 製造上述樣板膨脹 |

## 依賴點（trace 結果）

- `learning-from-failures` 被引用：`planning-agent-systems`（`memory-manager.py get-warnings`，line 89/104）、`README.md`、`README.zh-TW.md`、`plugins/rcc/README.md`。
- `reflecting` 被引用：`commands/reflect.md`、`planning-agent-systems`、`writing-rules/references/examples.md`、`brainstorming-workflows/references/routing-patterns.md`、`migrating-agent-systems/references/config-schema.md`、兩份 README。

## 執行階段

### Phase 1 — 政策層（CLAUDE.md Law 7）

- 改寫 Law 7：從「必須有四大 section」→「依需要」。明確：flowchart 非必需；TaskCreate 樣板僅多步驟流程需要。
- 驗證：Law 7 不再含強制四大 section 措辭。

### Phase 2 — 反思核心重寫

- 重寫 `reflecting/SKILL.md` 為建議制兩段式：
  - **Stage 1 輕量掃描**：列「值得反思的候選點」清單（簡述 + 為何值得 + 類型）；不強制數量；`safety_bypass` 仍醒目標記（安全不輕量化掉）。
  - **Stage 2 深入**：使用者挑選後，僅對選中項萃取 learning + 建議落地位置（rule/law/skill/hook/doc）。
  - 移除：6-task MANDATORY 樣板、router Glob trace、reviewer 逐項審強制、自動路由 planning、結尾 flowchart。
  - 併入 `learning-from-failures` 的失敗學習（debug session 雙目標：bug 本身 + 模型推理錯誤）。
  - hand off `planning-agent-systems` 改為 opt-in（保留 ACE pipeline 能力但不強制）。
  - 目標：< 120 行。
- 重寫 `references/report-template.md` → 輕量「建議清單」格式。
- 刪除 `learning-from-failures/` 整個目錄（SKILL.md + `scripts/memory-manager.py` 511 行 + `references/memory-patterns.md` 406 行）。

### Phase 3 — 下游修正

- `planning-agent-systems`：移除 `memory-manager.py get-warnings` 呼叫（line 89 區段）+「learning warnings addressed」改寫（line 104）。
- `commands/reflect.md`：描述對齊建議制。
- references 引用檢查：`writing-rules/examples.md`、`brainstorming-workflows/routing-patterns.md`、`migrating-agent-systems/config-schema.md`。
- 驗證：`grep memory-manager plugins/` 無殘留；引用 reflecting 處與新流程一致。

### Phase 4 — flowchart 批次移除

- 移除其餘 22 個 skill 的 `## Flowchart` + `digraph` 段落（reflecting 已於 Phase 2 處理）。
- 驗證：`grep -rl digraph plugins/rcc/skills/*/SKILL.md` = 0。

### Phase 5 — TaskCreate 樣板鬆綁（務實範圍）

我的建議：**不**一次硬改全部 24 個 skill。理由：一次動 24 檔 diff 巨大難審、違反 surgical 原則，且部分多步驟 skill 的 task 追蹤有實際價值。

- 政策先行（Phase 1 已鬆綁 Law 7）。
- 反思 skill 示範新樣式（Phase 2 已套用）。
- 其餘 skill 的 TaskCreate 樣板：移除純儀式性者、保留有價值的多步驟追蹤；逐一判斷，可隨各自後續重構漸進套用。

### Phase 6 — 文件同步 + 收尾

- `README.md` + `README.zh-TW.md` 同步（Law 3）：反思機制描述、移除 `learning-from-failures`、skill 表更新。
- `plugins/rcc/README.md` 同步。
- `.rcc/config.yml` `decisions_log` 記錄此次決策。
- commit（策略待定：移除 skill 屬 breaking，候選 `feat!:`；執行到該步再確認）。

## 額外觀察（待你決定，預設不動）

- **Law 8**（每次回覆開頭顯示 `<law>` block）同屬「形式主義、對 AI 任務價值低」候選，但不在你勾選範圍內，本次保留。若要一併精簡再告知。

## 驗證總表

| Phase | 驗證 |
|-------|------|
| 1 | Law 7 無強制四大 section |
| 2 | reflecting < 120 行、無 TaskCreate/flowchart、含兩段建議制；`learning-from-failures/` 不存在 |
| 3 | `grep memory-manager plugins/` = 空 |
| 4 | `grep digraph plugins/rcc/skills/*/SKILL.md` = 0 |
| 6 | 兩份 README 同步、config 決策已記 |
