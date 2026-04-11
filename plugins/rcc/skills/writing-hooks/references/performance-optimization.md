# Hook Performance Optimization Reference

## PerformantSecurityHook Class Template

```python
import time
import threading
import logging
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH" 
    MEDIUM = "MEDIUM"
    LOW = "LOW"

@dataclass
class SecurityResult:
    severity: SeverityLevel
    message: str
    details: Optional[str] = None
    confidence: float = 0.0
    execution_time: float = 0.0
    check_name: str = ""

class SecurityBlockError(Exception):
    """Raised for CRITICAL security issues that must block execution"""
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(message)

class PerformantSecurityHook:
    """
    高效能安全檢查 Hook 基礎類別
    實現並行執行、超時控制、優雅降級
    """
    
    def __init__(self, 
                 timeout: int = 30,
                 max_workers: int = 4,
                 confidence_threshold: float = 0.75,
                 cache_enabled: bool = True):
        self.timeout = timeout
        self.max_workers = max_workers
        self.confidence_threshold = confidence_threshold
        self.cache_enabled = cache_enabled
        self.results_cache = {}
        
    def execute(self, context: Dict[str, Any]) -> List[SecurityResult]:
        """
        主執行方法 - 並行執行所有安全檢查
        """
        start_time = time.time()
        
        try:
            # 獲取要執行的檢查
            security_checks = self.get_security_checks(context)
            
            # 並行執行檢查
            results = self._execute_parallel_checks(security_checks, context)
            
            # 過濾低信心結果
            filtered_results = self._filter_by_confidence(results)
            
            # 應用護欄策略
            self._apply_guardrails(filtered_results)
            
            execution_time = time.time() - start_time
            logger.info(f"Security checks completed in {execution_time:.2f}s")
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Security check failed: {e}")
            return [SecurityResult(
                severity=SeverityLevel.HIGH,
                message="Security check execution failed",
                details=str(e),
                execution_time=time.time() - start_time
            )]
    
    def _execute_parallel_checks(self, 
                               checks: List[Callable], 
                               context: Dict[str, Any]) -> List[SecurityResult]:
        """
        並行執行安全檢查
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有檢查任務
            future_to_check = {
                executor.submit(self._run_single_check, check, context, self.timeout // len(checks)): 
                check.__name__ for check in checks
            }
            
            # 收集結果
            for future in as_completed(future_to_check, timeout=self.timeout):
                check_name = future_to_check[future]
                try:
                    result = future.result()
                    if result:
                        result.check_name = check_name
                        results.append(result)
                except TimeoutError:
                    results.append(SecurityResult(
                        severity=SeverityLevel.MEDIUM,
                        message=f"Security check '{check_name}' timed out",
                        check_name=check_name,
                        execution_time=self.timeout // len(checks)
                    ))
                except Exception as exc:
                    results.append(SecurityResult(
                        severity=SeverityLevel.HIGH,
                        message=f"Security check '{check_name}' failed",
                        details=str(exc),
                        check_name=check_name
                    ))
        
        return results
    
    def _run_single_check(self, 
                         check: Callable,
                         context: Dict[str, Any], 
                         timeout: int) -> Optional[SecurityResult]:
        """
        執行單一安全檢查，包含超時控制
        """
        start_time = time.time()
        check_name = check.__name__
        
        # 檢查快取
        if self.cache_enabled:
            cached_result = self._get_cached_result(check_name, context)
            if cached_result:
                return cached_result
        
        try:
            # 設定超時
            def timeout_handler():
                raise TimeoutError(f"Check '{check_name}' exceeded {timeout}s timeout")
            
            timer = threading.Timer(timeout, timeout_handler)
            timer.start()
            
            try:
                result = check(context)
                if result:
                    result.execution_time = time.time() - start_time
                    
                    # 快取結果
                    if self.cache_enabled:
                        self._cache_result(check_name, context, result)
                
                return result
            finally:
                timer.cancel()
                
        except TimeoutError:
            return SecurityResult(
                severity=SeverityLevel.MEDIUM,
                message=f"Check '{check_name}' timed out",
                execution_time=timeout
            )
        except Exception as e:
            return SecurityResult(
                severity=SeverityLevel.HIGH,
                message=f"Check '{check_name}' failed",
                details=str(e),
                execution_time=time.time() - start_time
            )
    
    def _filter_by_confidence(self, results: List[SecurityResult]) -> List[SecurityResult]:
        """
        過濾信心度低於閾值的結果
        """
        filtered = []
        for result in results:
            if result.confidence >= self.confidence_threshold or result.severity == SeverityLevel.CRITICAL:
                filtered.append(result)
            else:
                logger.debug(f"Filtered low-confidence result: {result.message} "
                           f"(confidence: {result.confidence:.2f})")
        
        return filtered
    
    def _apply_guardrails(self, results: List[SecurityResult]) -> None:
        """
        應用護欄策略
        """
        critical_issues = [r for r in results if r.severity == SeverityLevel.CRITICAL]
        high_issues = [r for r in results if r.severity == SeverityLevel.HIGH]
        medium_issues = [r for r in results if r.severity == SeverityLevel.MEDIUM]
        low_issues = [r for r in results if r.severity == SeverityLevel.LOW]
        
        # CRITICAL: 阻擋執行
        if critical_issues:
            error_messages = [f"• {issue.message}" for issue in critical_issues]
            raise SecurityBlockError(
                "Critical security issues found:\n" + "\n".join(error_messages),
                details="\n".join([issue.details or "" for issue in critical_issues])
            )
        
        # HIGH: 警告 + 5 秒延遲
        if high_issues:
            self._show_high_severity_warning(high_issues)
        
        # MEDIUM: 警告（可立即跳過）
        if medium_issues:
            self._show_medium_severity_warning(medium_issues)
        
        # LOW: 僅記錄
        for issue in low_issues:
            logger.info(f"Security notice: {issue.message}")
    
    def _show_high_severity_warning(self, issues: List[SecurityResult]) -> None:
        """
        顯示高嚴重性警告並延遲
        """
        print("\n⚠️  HIGH SECURITY CONCERNS DETECTED:")
        for issue in issues:
            print(f"• {issue.message}")
            if issue.details:
                print(f"  Details: {issue.details}")
        
        print(f"\nContinuing in 5 seconds... (Ctrl+C to abort)")
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            raise SecurityBlockError("User aborted due to security concerns")
    
    def _show_medium_severity_warning(self, issues: List[SecurityResult]) -> None:
        """
        顯示中等嚴重性警告
        """
        print("\n⚠️  Security warnings:")
        for issue in issues:
            print(f"• {issue.message}")
    
    def _get_cached_result(self, check_name: str, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        獲取快取的檢查結果
        """
        cache_key = self._get_cache_key(check_name, context)
        return self.results_cache.get(cache_key)
    
    def _cache_result(self, check_name: str, context: Dict[str, Any], result: SecurityResult) -> None:
        """
        快取檢查結果
        """
        cache_key = self._get_cache_key(check_name, context)
        self.results_cache[cache_key] = result
    
    def _get_cache_key(self, check_name: str, context: Dict[str, Any]) -> str:
        """
        生成快取鍵值
        """
        import hashlib
        
        # 基於檔案內容生成 hash
        content = str(context.get('file_content', ''))
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        
        return f"{check_name}_{content_hash}"
    
    @abstractmethod
    def get_security_checks(self, context: Dict[str, Any]) -> List[Callable]:
        """
        子類需實現：返回要執行的安全檢查函數列表
        """
        pass

# 具體實現範例
class CodeSecurityHook(PerformantSecurityHook):
    """
    程式碼安全檢查 Hook 實現
    """
    
    def get_security_checks(self, context: Dict[str, Any]) -> List[Callable]:
        """
        返回程式碼安全檢查函數
        """
        return [
            self.check_sql_injection,
            self.check_xss_vulnerabilities,
            self.check_hardcoded_secrets,
            self.check_unsafe_functions,
            self.check_dependency_vulnerabilities
        ]
    
    def check_sql_injection(self, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        SQL 注入檢查
        """
        content = context.get('file_content', '')
        
        # 簡化的 SQL 注入檢測邏輯
        sql_patterns = [
            r"execute\s*\(\s*['\"].*\+.*['\"]",
            r"query\s*\(\s*['\"].*\%.*['\"]",
            r"cursor\.execute\s*\(\s*['\"].*\+.*['\"]"
        ]
        
        import re
        for pattern in sql_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return SecurityResult(
                    severity=SeverityLevel.HIGH,
                    message="Potential SQL injection vulnerability detected",
                    details=f"Pattern matched: {pattern}",
                    confidence=0.8
                )
        
        return None
    
    def check_xss_vulnerabilities(self, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        XSS 漏洞檢查
        """
        content = context.get('file_content', '')
        
        xss_patterns = [
            r"innerHTML\s*=\s*.*\+.*",
            r"document\.write\s*\(.*\+.*\)",
            r"eval\s*\(.*user.*\)"
        ]
        
        import re
        for pattern in xss_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return SecurityResult(
                    severity=SeverityLevel.HIGH,
                    message="Potential XSS vulnerability detected",
                    details=f"Pattern matched: {pattern}",
                    confidence=0.75
                )
        
        return None
    
    def check_hardcoded_secrets(self, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        硬編碼秘密檢查
        """
        content = context.get('file_content', '')
        
        secret_patterns = [
            r"password\s*=\s*['\"][^'\"]{8,}['\"]",
            r"api_key\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]",
            r"secret_key\s*=\s*['\"][^'\"]{16,}['\"]",
            r"token\s*=\s*['\"][a-zA-Z0-9\-_]{20,}['\"]"
        ]
        
        import re
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return SecurityResult(
                    severity=SeverityLevel.CRITICAL,
                    message="Hardcoded secret detected",
                    details=f"Pattern matched: {pattern}",
                    confidence=0.9
                )
        
        return None
    
    def check_unsafe_functions(self, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        不安全函數檢查
        """
        content = context.get('file_content', '')
        
        unsafe_functions = [
            r"eval\s*\(",
            r"exec\s*\(",
            r"subprocess\.shell\s*=\s*True",
            r"os\.system\s*\("
        ]
        
        import re
        for pattern in unsafe_functions:
            if re.search(pattern, content, re.IGNORECASE):
                return SecurityResult(
                    severity=SeverityLevel.HIGH,
                    message="Unsafe function usage detected",
                    details=f"Function: {pattern}",
                    confidence=0.85
                )
        
        return None
    
    def check_dependency_vulnerabilities(self, context: Dict[str, Any]) -> Optional[SecurityResult]:
        """
        相依性漏洞檢查
        """
        # 這裡可以整合 npm audit, pip-audit 等工具
        file_path = context.get('file_path', '')
        
        if 'package.json' in file_path or 'requirements.txt' in file_path:
            # 簡化示範 - 實際應該調用 audit 工具
            return SecurityResult(
                severity=SeverityLevel.MEDIUM,
                message="Dependency security scan recommended",
                details="Run security audit on dependencies",
                confidence=0.5
            )
        
        return None

# 使用範例
def create_security_hook():
    """
    創建配置好的安全檢查 Hook
    """
    return CodeSecurityHook(
        timeout=30,
        max_workers=4,
        confidence_threshold=0.75,
        cache_enabled=True
    )

# Hook 整合範例
def pre_commit_hook(context):
    """
    Pre-commit Hook 整合範例
    """
    security_hook = create_security_hook()
    
    try:
        results = security_hook.execute(context)
        
        # 生成報告
        if results:
            print(f"\nSecurity scan found {len(results)} issues:")
            for result in results:
                severity_icon = {
                    SeverityLevel.CRITICAL: "🚫",
                    SeverityLevel.HIGH: "⚠️",
                    SeverityLevel.MEDIUM: "⚡",
                    SeverityLevel.LOW: "ℹ️"
                }[result.severity]
                
                print(f"{severity_icon} [{result.severity.value}] {result.message}")
                if result.details:
                    print(f"   {result.details}")
        
        return True
        
    except SecurityBlockError as e:
        print(f"\n🚫 COMMIT BLOCKED: {e.message}")
        if e.details:
            print(f"Details: {e.details}")
        return False
```

## Performance Monitoring Integration

```python
import time
import psutil
from contextlib import contextmanager

@contextmanager
def performance_monitor(operation_name: str):
    """
    效能監控上下文管理器
    """
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
    start_cpu = psutil.cpu_percent()
    
    yield
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss / 1024 / 1024
    end_cpu = psutil.cpu_percent()
    
    duration = end_time - start_time
    memory_delta = end_memory - start_memory
    
    logger.info(f"Performance: {operation_name}")
    logger.info(f"  Duration: {duration:.2f}s")
    logger.info(f"  Memory: {memory_delta:+.2f}MB")
    logger.info(f"  CPU: {end_cpu:.1f}%")
    
    # 警告條件
    if duration > 10:
        logger.warning(f"Slow operation: {operation_name} took {duration:.2f}s")
    if memory_delta > 100:
        logger.warning(f"High memory usage: {operation_name} used {memory_delta:.2f}MB")

# 使用範例
def optimized_security_hook(context):
    with performance_monitor("security_scan"):
        hook = create_security_hook()
        return hook.execute(context)
```

## Skip Mechanisms

```python
import os

class SecuritySkipManager:
    """
    安全檢查跳過機制管理
    """
    
    @staticmethod
    def should_skip_check(check_name: str) -> bool:
        """
        檢查是否應該跳過特定檢查
        """
        skip_env = os.getenv('CLAUDE_SECURITY_SKIP', '')
        skip_checks = [s.strip().lower() for s in skip_env.split(',')]
        
        return check_name.lower() in skip_checks
    
    @staticmethod
    def get_security_mode() -> str:
        """
        獲取安全模式設定
        """
        return os.getenv('CLAUDE_SECURITY_MODE', 'standard').lower()
    
    @staticmethod
    def get_timeout_override() -> Optional[int]:
        """
        獲取 timeout 覆寫設定
        """
        timeout_str = os.getenv('CLAUDE_SECURITY_TIMEOUT')
        if timeout_str:
            try:
                return int(timeout_str)
            except ValueError:
                logger.warning(f"Invalid CLAUDE_SECURITY_TIMEOUT: {timeout_str}")
        return None

# 整合到 Hook 中
class ConfigurableSecurityHook(PerformantSecurityHook):
    def __init__(self):
        # 根據環境變數調整設定
        mode = SecuritySkipManager.get_security_mode()
        timeout_override = SecuritySkipManager.get_timeout_override()
        
        if mode == 'fast':
            super().__init__(timeout=timeout_override or 10, max_workers=2)
        elif mode == 'thorough':
            super().__init__(timeout=timeout_override or 60, max_workers=6)
        else:  # standard
            super().__init__(timeout=timeout_override or 30, max_workers=4)
    
    def get_security_checks(self, context: Dict[str, Any]) -> List[Callable]:
        all_checks = [
            self.check_sql_injection,
            self.check_xss_vulnerabilities, 
            self.check_hardcoded_secrets,
            self.check_unsafe_functions,
            self.check_dependency_vulnerabilities
        ]
        
        # 根據跳過設定過濾
        filtered_checks = []
        for check in all_checks:
            if not SecuritySkipManager.should_skip_check(check.__name__):
                filtered_checks.append(check)
            else:
                logger.debug(f"Skipping check: {check.__name__}")
        
        return filtered_checks
```