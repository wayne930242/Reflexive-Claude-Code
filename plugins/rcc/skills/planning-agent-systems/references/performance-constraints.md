# Performance Constraints Reference

## Hook Performance Requirements

### Time Limits (Hard Constraints)
- **總執行時間**: ≤ 30 秒 (MUST) - 超過即強制終止
- **網路請求時間**: ≤ 10 秒 (timeout 設定)
- **檔案掃描時間**: ≤ 5 秒 (本地操作)
- **資料庫查詢時間**: ≤ 3 秒 (如適用)

### Performance Budget Allocation
```
總預算 30 秒分配：
├── 初始化 (2秒)
├── 並行檢查 (20秒)
│   ├── 靜態分析 (15秒)
│   ├── 網路驗證 (10秒，並行)
│   └── 檔案掃描 (5秒，並行)
├── 結果整合 (3秒)
├── 報告生成 (3秒)
└── 清理緩存 (2秒)
```

## Implementation Strategies

### 1. Parallel Execution
```python
# 使用 ThreadPoolExecutor 並行處理
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

def execute_checks_parallel(checks, timeout=25):
    results = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_check = {
            executor.submit(check.run, timeout//len(checks)): check.name 
            for check in checks
        }
        
        for future in as_completed(future_to_check, timeout=timeout):
            check_name = future_to_check[future]
            try:
                results[check_name] = future.result()
            except Exception as exc:
                results[check_name] = {"error": str(exc), "status": "timeout"}
    
    return results
```

### 2. Progressive Enablement
```
快速模式 (5秒)：基本語法檢查 + 安全層級 1
標準模式 (15秒)：靜態分析 + 安全層級 1-2  
完整模式 (30秒)：全面掃描 + 安全層級 1-4
```

### 3. Scope Limiting
- **僅掃描變更檔案**: 使用 git diff 限制掃描範圍
- **增量檢查**: 基於檔案 hash 快取結果
- **路徑過濾**: 排除 node_modules, .git, dist 等目錄

### 4. Result Caching
```python
import hashlib
import json
from pathlib import Path

class SecurityCheckCache:
    def __init__(self, cache_dir=".claude/cache/security"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_file_hash(self, filepath):
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def get_cached_result(self, filepath, check_type):
        file_hash = self.get_file_hash(filepath)
        cache_file = self.cache_dir / f"{check_type}_{file_hash}.json"
        
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)
        return None
    
    def cache_result(self, filepath, check_type, result):
        file_hash = self.get_file_hash(filepath)
        cache_file = self.cache_dir / f"{check_type}_{file_hash}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(result, f)
```

## Guardrail vs Blocker Strategy

### Decision Matrix
| 嚴重性 | 行為 | 使用者選項 | 延遲時間 |
|--------|------|------------|----------|
| CRITICAL | BLOCK | 無法跳過，必須修復 | N/A |
| HIGH | WARN + DELAY | 5秒後可跳過 | 5秒 |
| MEDIUM | WARN | 立即可跳過 | 0秒 |
| LOW | LOG | 靜默處理，僅記錄 | 0秒 |

### Implementation
```python
class GuardrailStrategy:
    @staticmethod
    def apply_guardrail(severity, message, details=None):
        if severity == "CRITICAL":
            raise SecurityBlockError(message, details)
        elif severity == "HIGH":
            return HighSeverityWarning(message, details, skip_delay=5)
        elif severity == "MEDIUM":
            return MediumSeverityWarning(message, details)
        elif severity == "LOW":
            logger.info(f"Security notice: {message}")
            return None

class HighSeverityWarning:
    def __init__(self, message, details, skip_delay=5):
        self.message = message
        self.details = details
        self.skip_delay = skip_delay
        
    def prompt_user(self):
        print(f"⚠️  HIGH SECURITY CONCERN: {self.message}")
        if self.details:
            print(f"Details: {self.details}")
        print(f"Continuing in {self.skip_delay} seconds... (Ctrl+C to abort)")
        time.sleep(self.skip_delay)
```

## Development Experience Optimization

### Skip Mechanisms
```bash
# 環境變數跳過機制
export CLAUDE_SECURITY_MODE="fast"      # 僅基本檢查
export CLAUDE_SECURITY_SKIP="low,medium" # 跳過特定嚴重性
export CLAUDE_SECURITY_TIMEOUT="15"     # 自訂 timeout
```

### Progress Indicators
```python
from tqdm import tqdm
import threading

class ProgressIndicator:
    def __init__(self, total_checks):
        self.progress = tqdm(total=total_checks, desc="Security checks")
        self.lock = threading.Lock()
    
    def update(self, description=""):
        with self.lock:
            self.progress.set_description(f"Security checks: {description}")
            self.progress.update(1)
    
    def close(self):
        self.progress.close()

# 使用範例
progress = ProgressIndicator(len(security_checks))
for check in security_checks:
    progress.update(f"Running {check.name}")
    result = check.run()
    # 處理結果
progress.close()
```

### Performance Monitoring
```python
import time
import psutil
from contextlib import contextmanager

@contextmanager
def performance_monitor(check_name):
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    
    yield
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
    
    duration = end_time - start_time
    memory_delta = end_memory - start_memory
    
    if duration > 5:  # 警告超過 5 秒的檢查
        logger.warning(f"{check_name} took {duration:.2f}s (slow)")
    if memory_delta > 50:  # 警告超過 50MB 記憶體使用
        logger.warning(f"{check_name} used {memory_delta:.2f}MB memory")

# 使用範例
with performance_monitor("static_analysis"):
    run_static_analysis()
```

## Quality Metrics

### Performance Targets
- **平均執行時間**: ≤ 15 秒
- **成功率**: ≥ 95% (無 timeout 失敗)
- **記憶體使用**: ≤ 200MB peak
- **並行效率**: ≥ 60% CPU 利用率

### Monitoring Commands
```bash
# 效能監控
claude security --monitor --duration=1h
claude security --profile --output=performance.json
claude security --benchmark --iterations=10
```