# aref Plugin — Design

- 日期：2026-04-20
- 狀態：設計核可待實作
- 作者：Wei Hung
- 相依：`plugins/rcc/`（既有），`.claude-plugin/marketplace.json`

## 1. Problem 與 Goals

對任意既有專案做結構性重構，產出結果讓 AI coding agent（Claude Code / Cursor / Codex 等）能安全導覽、理解、修改。目標兼顧三件事：

- 機械化可驗證的結構品質（模組化、入口單一化、共用層、cyclic-free、複雜度控制）
- 靜態品質閘門（linter、type checker）存在且綠
- 動手重構前建立安全網（characterization tests），事後以 mutation testing 驗測試有 assertion

產出獨立於 `rcc`，重構結束時依條件建議下一步 `/rcc migrate` 或 `/rcc reflect` handoff。

### 非目標

- 不負責商業邏輯重寫（僅結構）
- 不跑 feature 開發
- 不整合 CI／遠端觸發（v1 範圍外）
- 不強制單一 coverage %

## 2. Plugin 架構

### 名稱與位置

- 套件名：`aref`（agentic refactor 縮寫）
- 路徑：`plugins/aref/`，與現有 `plugins/rcc/` 並列
- Marketplace：更新 `.claude-plugin/marketplace.json` 的 `plugins` 陣列加入第二個條目，獨立版號

### 目錄結構

```
plugins/aref/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── analyzing-codebases/
│   ├── planning-refactors/
│   ├── scaffolding-characterization-tests/
│   ├── applying-refactors/
│   ├── verifying-refactors/
│   └── finalizing-refactors/
├── agents/
│   └── refactor-phase-reviewer.md
├── commands/
│   └── aref.md
├── fixtures/                       # 自測用迷你 broken 專案
│   ├── typescript/
│   ├── python/
│   ├── rust/
│   └── go/
├── tests/
│   └── run-fixtures.md
└── README.md
```

### 版號管理

- `aref` 版號獨立於 `rcc`。
- `release-please-config.json` 新增 `plugins/aref` 套件條目；`.release-please-manifest.json` 加對應 key。
- `marketplace.json` 的 `plugins[0]` 是 rcc，`plugins[1]` 是 aref，各自 `version` 欄位由 release-please 更新。
- 本專案 README 的 aref 區塊同 rcc 方式加 `<!-- x-release-please-version -->` marker。

### 與 rcc 關係

- 完全獨立可並存。使用者可只裝 rcc、只裝 aref、或兩者都裝。
- `finalizing-refactors` 依 §6 條件建議呼叫 rcc，但不強制。

## 3. Workflow

### 進入點

`/aref` 命令觸發 `analyzing-codebases`；後續 skill 透過 handoff 鏈式推進（每 skill 的 `Routing` 區塊指向下一 skill）。

### Pipeline 6 階段

```
/aref
  ↓
[1] analyzing-codebases
    → 偵測語言與 monorepo 狀態
    → 跑對應 toolchain（見 §5）
    → 產 .rcc/{ts}-refactor-map.md（hotspot 排名、dep graph、複雜度、AGENTS.md gap）
    → ⏸ checkpoint
  ↓
[2] planning-refactors
    → 依 map 提 phased plan（parallel-change / branch-by-abstraction / strangler 擇一）
    → 每 phase 標定：目標模組、預計 LOC、對應 characterization test 需求、pattern 分類
    → 產 .rcc/{ts}-refactor-plan.md
    → ⏸ checkpoint
  ↓
[3] scaffolding-characterization-tests
    → 為 plan 涉及的 hotspot 模組補 golden / snapshot test
    → 既有測試足夠 → 跳過該模組
    → 無法建（高 IO 依賴、外部 service）→ 標記 high-risk
    → 驗證：新增 test 全綠
    → ⏸ checkpoint（若有新增 test）
  ↓
[4] applying-refactors
    → 驗 git status 乾淨
    → 建 branch refactor/{ts}-{scope}
    → 逐 phase：編輯 → 跑 test → commit
    → ⏸ checkpoint between phases
    → 每 phase 呼叫 refactor-phase-reviewer 子代理驗 diff
  ↓
[5] verifying-refactors
    → 硬規則驗（cyclic=0、file/fn line caps、cognitive 15、cyclomatic 10）
    → mutation testing on touched modules
    → 產 .rcc/{ts}-verification-report.md
    → ⏸ checkpoint
  ↓
[6] finalizing-refactors
    → 產/更新 AGENTS.md（per subproject）
    → 封存 .rcc/ 檔案到 .rcc/archive/{ts}-aref-run/
    → 偵測 .claude/ 或 plugins/
      · 不存在 → 建議 /rcc migrate
      · 存在 → 建議 /rcc reflect
    → 輸出 merge 或 PR 指引
```

### Checkpoint 機制

- 每 ⏸ 點 skill 必須停下等使用者確認，不得靜默推進。
- 使用者可回下列四種動作：
  - `繼續`：推進下一 phase / 階段
  - `調整計畫`：回 `planning-refactors` 改 plan（僅 `applying-refactors` 前可用）
  - `rollback current phase`：撤回當前 phase 的編輯（`applying-refactors` 期間可用，詳見 §6）
  - `abort entire run`：整個 run 中止；branch 保留、已 commit 不動

### 失敗處理

- Phase test 紅 → 停在該 phase，輸出錯訊，使用者決定修還是 rollback（`git reset --hard <phase-start-sha>`）。
- Characterization test 無法建 → 標記 high-risk，要使用者明確 acknowledge 才能進 `applying-refactors`。
- Mutation survivors >20% → 列在 verification report，不擋 finalizing。
- Oversized phase（>400 LOC）→ planning 階段即拆小；不可拆時需使用者明確批准。

## 4. Data Flow 與 Artifacts

### .rcc/ 檔案布局

```
.rcc/
├── config.yml                               # 既有（rcc 擁有，aref 新增 aref: 區塊）
├── {ts}-refactor-map.md                     # analyzing 產
├── {ts}-refactor-plan.md                    # planning 產
├── {ts}-characterization-notes.md           # scaffolding 產
├── {ts}-phase-{N}-review.md                 # reviewer 每 phase 報告
├── {ts}-verification-report.md              # verifying 產
└── archive/
    └── {ts}-aref-run/                       # finalizing 移入
        ├── refactor-map.md
        ├── refactor-plan.md
        ├── characterization-notes.md
        ├── phase-*-review.md
        └── verification-report.md
```

- `{ts}` 格式 `YYYYMMDD-HHMMSS`，對齊 rcc 既有慣例。
- `archive/` 保留歷史 run；下次 `/aref` 重新以新 `{ts}` 起算。

### config.yml 新增 aref 區塊

```yaml
aref:
  last_run: 20260420-143022
  detected_languages: [typescript, python]
  tools:
    typescript: [dependency-cruiser, madge, jscpd, eslint, tsc, vitest, stryker]
    python: [radon, pydeps, lizard, ruff, mypy, pytest, mutmut]
  decisions:
    - ts: 20260420-143022
      decision: chose parallel-change over strangler for auth module
      reason: scope too narrow for strangler
```

### AGENTS.md 寫入策略

- 目標路徑：repo root + 每個 subproject（偵測自有 manifest 的目錄）
- 策略：
  - 不存在 → 新建
  - 已存在 → 讀既有、增補缺 section、保留使用者自訂內容、diff 預覽請使用者確認
- 骨架 section（plugin 自動填）：
  - Overview（取 README 頭段）
  - Build / Test（取 manifest scripts 或 Makefile）
  - Code Style（取 linter config）
  - Test Conventions（取 test 目錄結構）
  - Architecture（refactor-map dep graph 摘要）
  - Security（placeholder，留 user 自填）

### 不觸動區

- `.rcc/memory/`（rcc 專屬）
- `docs/plans/`（rcc brainstorming 專用）
- `.env` 與密鑰檔
- CI config（`.github/`、`.gitlab-ci.yml` 等）
- Git config

## 5. Language Tool Matrix

依 Q3-B 主流棧優先。每階段每語言一組預設工具。

| 階段             | TypeScript / JS                                    | Python                  | Rust                          | Go                       | 其他降級              |
|------------------|----------------------------------------------------|-------------------------|-------------------------------|--------------------------|-----------------------|
| Dep graph        | dependency-cruiser                                 | pydeps                  | cargo-modules                 | go-callvis               | 目錄樹                |
| File/fn complexity | complexity-report / eslint-plugin-sonarjs        | radon + lizard          | clippy lints                  | gocyclo                  | 行數 + 嵌套（通用）   |
| Cognitive        | eslint-plugin-sonarjs (cognitive-complexity)       | cognitive-complexity    | clippy::cognitive_complexity  | gocognit                 | 退回 cyclomatic       |
| Duplication      | jscpd                                              | jscpd                   | jscpd                         | jscpd                    | jscpd                 |
| Semantic pattern | ast-grep / semgrep                                 | semgrep                 | ast-grep                      | semgrep                  | semgrep               |
| Linter           | eslint                                             | ruff                    | clippy                        | staticcheck + go vet     | 跳過                  |
| Type checker     | tsc --noEmit                                       | mypy / pyright          | cargo check                   | go build                 | N/A                   |
| Test runner      | vitest / jest（偵測）                              | pytest                  | cargo test                    | go test                  | 偵測 Makefile / CI    |
| Mutation         | stryker                                            | mutmut                  | cargo-mutants                 | go-mutesting             | 跳過（退 assertion 計） |

### 工具安裝策略

- Plugin 不強裝工具。`analyzing-codebases` 偵測缺工具 → 印安裝命令 + 讓使用者選「裝後繼續」或「跳過該類分析」。
- 每語言 recipe 放 `plugins/aref/skills/analyzing-codebases/references/{lang}-toolchain.md`。

### 偵測邏輯

1. Root 掃 `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` → 語言集合
2. 多語 monorepo → 每 subproject 獨立 recipe
3. 無上述 manifest → 降級通用模式（semgrep + jscpd + 目錄分析 + 行數計）

### 版本策略

Plugin 不釘工具版本。README 記最低相容版號（e.g. `dependency-cruiser >=16`），使用者自行維護。

## 6. Safety / Risk Controls

### 分支隔離

- `applying-refactors` 前驗 `git status` 乾淨。dirty tree → 停，印「先 commit 或 stash」。
- 建 branch：`refactor/YYYYMMDD-HHMMSS-{scope}`，scope 由 plan 指定。
- 不觸 main / master / production 等 base branch。

### Commit 紀律

- 每 parallel-change phase 一個 commit，訊息格式：
  ```
  refactor(aref): phase N/M — {phase title}

  {phase description from plan}
  Phase: {expand|migrate|contract}
  Verification: {tests pass | mutation score X/Y}
  ```
- Phase 正常推進過程禁用 `--amend`、`rebase -i`、`reset --hard`（僅 rollback 路徑例外，見本節 Rollback 路徑）。
- Commit 前必跑對應語言 test runner；紅 → 阻擋 commit。

### Phase size ceiling

- 預估 phase diff >400 LOC → planning 階段即拆小。
- 不可拆時（單檔 extract class 類）標記 `oversized`，要使用者明確批准。
- `refactor-phase-reviewer` 實測 diff LOC，超限發警告。

### Characterization test 防網

- 無測試的 hotspot 模組 → 必過 `scaffolding-characterization-tests`，否則 `applying-refactors` 拒啟動。
- 高 IO / 外部依賴無法建測 → 標 high-risk，使用者 acknowledge 才能進 applying。

### Mutation testing scope

- 只跑 touched modules（全專案跑代價過高）。
- Mutation survivors >20% → verifying 報 `weak-tests`，不擋 finalizing。

### 全階段禁止動作

- 不改 git config。
- 不 force push。
- 不跳 hooks（`--no-verify`）。
- 不刪檔案（除非 plan 列出且使用者批准）。
- 不改 CI config / `.env` 類檔。
- 不跑 publish 類命令（`npm publish` / `cargo publish` / `pip upload`）。

### Rollback 路徑

- 任一 checkpoint 可選 `rollback current phase` 或 `abort entire run`。
- Rollback：`git reset --hard <phase-start-sha>`（commit 未推時）或建議手動 revert。
- Abort：branch 保留，commit 不動。

### Dry-run

- `/aref --dry-run` 只跑 analyzing + planning，不進 scaffolding / applying。輸出 plan + 預估 diff。

## 7. Scope 與 Monorepo

### 每次執行 scope 決策

- 預設 operate on CWD。
- Monorepo 偵測：root 有 `pnpm-workspace.yaml` / `lerna.json` / `nx.json` / `turbo.json` / Cargo workspace / Go multi-module / Python workspace。
- Monorepo → `analyzing-codebases` 列所有 subproject，問使用者選「全 repo」/「特定 subproject」/「root only」。
- 單語言單 project → 直接掃整 repo。

### Subproject 隔離

- 每 subproject 獨立 refactor-map + plan（不混）。
- 多 subproject → 依序跑，branch 策略由使用者選：
  - 每 subproject 一 branch
  - 單一 branch 多 scope
- Cross-subproject refactor（例如抽共用型別到新 package）在 plan 標 `cross-subproject`，使用者明確 acknowledge 才執行。

### AGENTS.md per-subproject

- 每 subproject root 寫自己的 AGENTS.md。
- Repo root AGENTS.md 摘要全 repo + 指向各 subproject AGENTS.md。

## 8. Plugin 自身驗證

### Skill 結構 lint

- 每 skill 用 rcc 的 `skill-reviewer` agent 審（frontmatter、gerund 命名、四段齊全：Task Init / Red Flags / Rationalizations / Flowchart）。

### Fixture 專案

- `plugins/aref/fixtures/{typescript, python, rust, go}/` 各放一個迷你 broken 專案。
- 每 fixture 含：god file、cyclic dep、缺測試模組。

### E2E 手測腳本

- `plugins/aref/tests/run-fixtures.md` 列每 fixture 跑 `/aref` 後應產的 artifact 清單 + 預期 AGENTS.md 內容。

### Agent reviewer 單測

- 用假 diff 驗 `refactor-phase-reviewer` 在 400 LOC trip、紅 test trip 條件下是否正確擋下。

### Plugin install 測

- 本地 `claude plugin add ./plugins/aref`，驗 6 skill 可 discover、`/aref` 命令存在、4 個 fixture 各自 analyzing 成功產出 map。

### Release automation 驗

- 初次 release 前跑 `release-please` dry-run 確認 aref 版號 bump 路徑正確，不影響 rcc 版號。

## 9. 不進 v1（YAGNI）

- 自動產生 architecture diagram（Mermaid / PlantUML）
- IDE 整合預覽 diff
- 遠端 CI 觸發
- 非 4 主流語言深度 recipe（Java、C#、Ruby、PHP 等）
- `/aref --continue` 斷點續跑（v1 用 dry-run + 手動重跑替代）

## 10. Open Questions

- refactor-map.md 與 refactor-plan.md 是否該有機械可讀的 YAML header（為 `applying-refactors` 機械讀取）？初版採 Markdown + 明確節點（e.g. `## Phase 1`），如難解析再補 frontmatter。
- Fixtures 是否納入 release 包？會增 install size。傾向放 `fixtures/` 但 README 註明「開發用途，可手動刪」。
- `/aref --dry-run` 以 flag 還是獨立 slash command（e.g. `/aref-plan`）？選 flag 以集中入口。

## 11. Success Criteria

V1 release 前必須達成：

1. 6 skill + 1 reviewer 全數通過 `skill-reviewer` 審查。
2. 4 個語言 fixture 各能跑完 `/aref` 全 pipeline，產出完整 artifact 集。
3. 所有 checkpoint 機制經手測觸發過（繼續 / 回頭 / 中止 / rollback 各一次）。
4. Release automation 能 bump aref 版號不影響 rcc 版號。
5. Plugin install 測通過（遠端 `claude plugin add` 從 marketplace）。
6. README（中英版）含安裝、使用範例、工具相容版號表。
