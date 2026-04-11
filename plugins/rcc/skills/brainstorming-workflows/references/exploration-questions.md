# Targeted Exploration Questions

探索用戶工作流的問題庫，按三個探索領域組織。
每次問一題，根據回答調整後續問題，總共 5-8 題。

## 1. Pipeline Mode Exploration

**目標：** 判斷工作流的連接方式與狀態管理需求。

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| 「這個工作流平常怎麼啟動的？固定入口還是看情況？」 | 流程啟動模式 | owner-pipe（固定入口）vs chain-pipe（變動入口） |
| 「中間如果斷掉，你會怎麼接回來？從頭重跑還是接著做？」 | 狀態持久化需求 | 無狀態 pipe vs state persistence |
| 「每一步大概動多少檔案？跨幾個模組？」 | 工作範圍大小 | 簡單 skill（小範圍）vs script-managed state（大範圍） |
| 「這些步驟一定要按順序嗎？還是有些可以平行？」 | pipeline 拓撲結構 | 順序 pipeline vs 平行分派 |
| 「誰負責決定下一步做什麼？」 | 控制權歸屬 | owner-pipe（人決定）vs chain-pipe（自動接力） |
| 「這個流程有幾個步驟？每步是誰負責的？」 | 步驟數與責任分配 | 步驟多 → chain-pipe；步驟少 → owner-pipe |

**選問策略：** 先問啟動模式，再根據回答決定是否需要問狀態和範圍。
如果前兩題已能判斷 pipeline mode，跳過其餘。

## 2. Pain Point Discovery

**目標：** 找出目前 agent 系統失效或讓用戶不滿的地方。

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| 「上次 agent 讓你覺得不好用是什麼時候？發生了什麼？」 | 缺失的能力或斷鏈 | 缺失的 skill 或 rule |
| 「有沒有什麼情況你覺得應該自動處理但現在沒有？」 | 自動化缺口 | 缺失的 hook 或 skill |
| 「哪些錯誤你已經被提醒過兩次以上？」 | 重複違規 | rule 或 hook enforcement |
| 「有沒有 Claude 回答的方式讓你覺得不對？」 | 行為偏差 | rule 或 CLAUDE.md adjustment |
| 「什麼時候你會覺得 Claude 太囉嗦或太簡短？」 | 溝通風格問題 | communication rule |
| 「有沒有什麼指令你每次都要重複說？」 | 指令遺忘 | CLAUDE.md 或 rule file |
| 「agent 有沒有做過讓你要花時間修正的事？」 | 行為失控 | guardrail（rule 或 hook） |

**選問策略：** 先問失敗經驗（前兩題），再根據回答決定是否深入溝通風格或行為問題。
如果用戶沒有負面經驗，快速帶過。

## 3. Routine Task & Small Work Identification

**目標：** 找出可自動化的重複性任務。

| Question | What It Reveals | Typical Component |
|----------|-----------------|-------------------|
| 「有沒有你每天都在做、但覺得很無聊的事？」 | 自動化候選 | agent 或 skill |
| 「搜尋程式碼的時候，有沒有固定的模式或常找的東西？」 | 固定搜尋模式 | 帶特定搜尋 pattern 的 agent |
| 「有沒有什麼格式化或檢查工作可以自動化？」 | 格式/品質檢查 | PostToolUse hook |
| 「每次開新 PR 或新 branch 的時候，有固定的步驟嗎？」 | 流程儀式 | skill 或 hook |
| 「有沒有常用的指令組合你希望一鍵完成？」 | 指令組合 | command alias 或 skill |
| 「有沒有定期要做的報告或摘要？」 | 週期性任務 | scheduled agent 或 skill |
| 「有沒有什麼工作你覺得 agent 做比你快？」 | delegation 候選 | agent 或 skill |

**選問策略：** 先問無聊的事，再根據角色補問特定類型。
開發者多問搜尋和格式化；PM 多問報告和流程。

## General Guidelines

- 每次只問一題
- 跳過分析報告中已回答的問題
- 根據回答調整後續問題，不要機械地照表問
- 總共最多 5-8 題（三個領域合計）
- 盡量用選擇題
- 先問失敗經驗，再問願望
