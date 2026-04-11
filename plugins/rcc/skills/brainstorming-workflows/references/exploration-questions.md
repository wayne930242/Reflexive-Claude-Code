# Targeted Exploration Questions

探索用戶工作流的問題庫，按三個探索領域組織。
每次問一題，根據回答調整後續問題，總共 5-8 題。

## 1. Pipeline Mode Exploration

**目標：** 判斷工作流是 chain-pipe 還是 owner-pipe，以及工作範圍。

### 問題

依序嘗試，根據回答跳過已釐清的問題：

1. 「這個工作流平常怎麼啟動的？固定入口還是看情況？」
   - 固定入口 → owner-pipe
   - 看情況 → chain-pipe
2. 「中間如果斷掉，你會怎麼接回來？從頭重跑還是接著做？」
   - 從頭重跑 → 無狀態，簡單 pipe
   - 接著做 → 需要 state persistence
3. 「每一步大概動多少檔案？改的範圍多大？」
   - 大範圍 → 需要 script-managed state
   - 小範圍 → 簡單 skill 即可
4. 「這個流程有幾個步驟？每步是誰負責的？」
   - 步驟數 + 負責人模式
5. 「有沒有哪些步驟的順序其實可以換？」
   - 可換序 → 鬆耦合，chain-pipe
   - 不可換 → 緊耦合，owner-pipe

### 判讀規則

| 回答特徵 | 指向元件類型 |
|----------|-------------|
| 固定入口 + 2-3 步 | owner-pipe |
| 變動入口 + 3+ 步 | chain-pipe |
| 每步大範圍改動 | 需要 script-managed state |
| 步驟可重排 | 鬆耦合，chain-pipe |

## 2. Pain Point Discovery

**目標：** 找出目前 agent 系統失效或缺失的地方。

### 問題

優先問失敗經驗，再問期望：

1. 「上次 agent 讓你覺得不好用是什麼時候？發生了什麼？」
   - 揭示缺失的 skill 或斷鏈
2. 「有沒有什麼情況你覺得應該自動處理但現在沒有？」
   - 揭示缺失的 hook 或 rule
3. 「哪些錯誤你已經被提醒過兩次以上？」
   - 需要 rule 或 hook 來預防
4. 「有沒有什麼指令你每次都要重複說？」
   - 應該寫成 CLAUDE.md 中的 rule
5. 「agent 有沒有做過讓你要花時間修正的事？」
   - 需要 guardrail（rule 或 hook）

### 判讀規則

| 回答特徵 | 指向元件類型 |
|----------|-------------|
| 重複糾正同一行為 | rule |
| 缺少自動化 | hook |
| 複雜多步驟失敗 | skill |
| 行為錯誤 | rule 或 CLAUDE.md 更新 |

## 3. Small Task / Routine Work Identification

**目標：** 找出可由 agent 處理的重複性小任務。

### 問題

1. 「有沒有你每天都在做、但覺得很無聊的事？」
   - 自動化候選
2. 「搜尋程式碼的時候，有沒有固定的模式或常找的東西？」
   - 帶特定搜尋模式的 agent
3. 「有沒有什麼格式化、檢查、或清理工作可以自動化？」
   - hook 候選
4. 「有沒有定期要做的報告或摘要？」
   - agent 或 skill 候選
5. 「有沒有什麼工作你覺得 agent 做比你快？」
   - delegation 候選

### 判讀規則

| 回答特徵 | 指向元件類型 |
|----------|-------------|
| 格式/lint 檢查 | PostToolUse hook |
| 固定搜尋模式 | 帶特定 tool config 的 agent |
| 週期性任務 | scheduled agent 或 skill |
| 簡單規則 | CLAUDE.md 或 rule file |

## General Guidelines

- 每次只問一題
- 跳過分析報告中已回答的問題
- 根據回答調整後續問題，不要機械地照表問
- 總共最多 5-8 題
- 盡量用選擇題
- 先問失敗經驗，再問願望
