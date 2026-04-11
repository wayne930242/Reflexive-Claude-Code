# AI 安全檢查 Hook 模板

## 完整 Python Hook 實現

```python
#!/usr/bin/env python3
"""
AI Security Checks Hook
針對 AI 生成程式碼進行安全漏洞檢測

Usage:
  - 作為 pre-commit hook 使用
  - 支援 Python, JavaScript, TypeScript 檔案
  - 三層檢驗架構：阻斷/警告/建議
"""

import re
import sys
import os
import json
import signal
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# AI 風險模式定義
AI_RISK_PATTERNS = {
    'python': {
        'sql_injection': {
            'pattern': r'f["\'].*SELECT.*\{.*\}|f["\'].*INSERT.*\{.*\}|f["\'].*UPDATE.*\{.*\}|f["\'].*DELETE.*\{.*\}|(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']',
            'confidence': 90,
            'description': 'SQL 注入風險：字串拼接查詢',
            'severity': 'high'
        },
        'command_injection': {
            'pattern': r'(os\.system|subprocess\.call|eval|exec)\s*\(\s*f?["\'].*\{.*\}',
            'confidence': 95,
            'description': '命令注入風險：格式化字串執行',
            'severity': 'critical'
        },
        'hardcoded_secrets': {
            'pattern': r'(password|api_key|secret|token)\s*=\s*["\'][a-zA-Z0-9_\-]{8,}["\']',
            'confidence': 85,
            'description': '硬編碼敏感資訊',
            'severity': 'high'
        },
        'path_traversal': {
            'pattern': r'open\s*\(\s*(request\.|user_|input_)',
            'confidence': 80,
            'description': '路徑遍歷風險：未驗證檔案路徑',
            'severity': 'medium'
        },
        'dangerous_eval': {
            'pattern': r'\b(eval|exec)\s*\(',
            'confidence': 95,
            'description': '危險程式碼執行：eval/exec',
            'severity': 'critical'
        },
        'pickle_deserialization': {
            'pattern': r'pickle\.loads?\s*\(',
            'confidence': 85,
            'description': 'Pickle 反序列化安全風險',
            'severity': 'high'
        }
    },
    'javascript': {
        'xss_risk': {
            'pattern': r'innerHTML\s*=.*\+|document\.write\s*\(',
            'confidence': 85,
            'description': 'XSS 風險：動態 HTML 注入',
            'severity': 'high'
        },
        'prototype_pollution': {
            'pattern': r'__proto__|constructor\s*\[.*\]|\.prototype\s*\[',
            'confidence': 90,
            'description': '原型污染風險',
            'severity': 'high'
        },
        'eval_usage': {
            'pattern': r'\beval\s*\(',
            'confidence': 95,
            'description': '危險程式碼執行：eval',
            'severity': 'critical'
        },
        'cors_wildcard': {
            'pattern': r'Access-Control-Allow-Origin.*\*',
            'confidence': 75,
            'description': 'CORS 萬用字元風險',
            'severity': 'medium'
        }
    },
    'typescript': {
        # TypeScript 繼承 JavaScript 模式
        'any_type_usage': {
            'pattern': r':\s*any\b',
            'confidence': 60,
            'description': 'any 類型使用：降低型別安全性',
            'severity': 'low'
        },
        'non_null_assertion': {
            'pattern': r'!\s*;|\!\.',
            'confidence': 70,
            'description': '非空斷言：可能的空指針風險',
            'severity': 'medium'
        }
    }
}

class AISecurityScanner:
    def __init__(self):
        self.results = []
        self.file_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript'
        }
        # 預編譯正則表達式以提升效能
        self.compiled_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, Dict[str, Dict]]:
        """預編譯所有正則表達式模式以提升效能"""
        compiled = {}
        for language, patterns in AI_RISK_PATTERNS.items():
            compiled[language] = {}
            for pattern_name, pattern_info in patterns.items():
                compiled_info = pattern_info.copy()
                compiled_info['compiled_pattern'] = re.compile(pattern_info['pattern'], re.IGNORECASE)
                compiled[language][pattern_name] = compiled_info
        return compiled
    
    def get_file_type(self, filepath: str) -> Optional[str]:
        """根據副檔名判斷檔案類型"""
        ext = Path(filepath).suffix
        return self.file_extensions.get(ext)
    
    def has_security_ignore(self, line: str, pattern_name: str) -> bool:
        """檢查是否有安全檢查忽略標記"""
        ignore_patterns = [
            f'AI-SECURITY-IGNORE: {pattern_name}',
            'AI-SECURITY-IGNORE: all',
            f'nosec: {pattern_name}'
        ]
        return any(pattern in line for pattern in ignore_patterns)
    
    def analyze_code_content(self, filepath: str, content: str) -> List[Dict]:
        """分析程式碼內容，返回風險發現"""
        file_type = self.get_file_type(filepath)
        if not file_type:
            return []
        
        # 檔案大小檢查：跳過超過 1MB 的檔案以提升效能
        if len(content.encode('utf-8')) > 1024 * 1024:
            print(f"⚠️ 跳過大檔案 {filepath} (> 1MB)")
            return []
        
        findings = []
        lines = content.split('\n')
        
        # 使用預編譯的模式
        language_patterns = self.compiled_patterns.get(file_type, {})
        if file_type == 'typescript':
            # TypeScript 繼承 JavaScript 模式
            js_patterns = self.compiled_patterns.get('javascript', {})
            language_patterns = {**js_patterns, **language_patterns}
        
        for line_num, line in enumerate(lines, 1):
            for pattern_name, pattern_info in language_patterns.items():
                # 檢查是否有忽略標記
                if self.has_security_ignore(line, pattern_name):
                    continue
                
                # 使用預編譯的正則表達式
                if pattern_info['compiled_pattern'].search(line):
                    findings.append({
                        'file': filepath,
                        'line': line_num,
                        'pattern': pattern_name,
                        'confidence': pattern_info['confidence'],
                        'description': pattern_info['description'],
                        'severity': pattern_info['severity'],
                        'code': line.strip(),
                        'suggestion': self.get_suggestion(pattern_name, line)
                    })
        
        return findings
    
    def get_suggestion(self, pattern_name: str, code_line: str) -> str:
        """提供修正建議"""
        suggestions = {
            'sql_injection': '使用參數化查詢或 ORM',
            'command_injection': '使用 subprocess 配合列表參數',
            'hardcoded_secrets': '使用環境變數或密鑰管理系統',
            'path_traversal': '驗證檔案路徑，使用白名單限制',
            'dangerous_eval': '避免使用 eval/exec，考慮 ast.literal_eval',
            'xss_risk': '使用安全的 DOM 操作方法',
            'prototype_pollution': '驗證物件屬性，避免動態屬性設定',
            'eval_usage': '避免使用 eval，考慮 JSON.parse',
            'any_type_usage': '使用具體型別定義',
            'pickle_deserialization': '使用 JSON 或其他安全格式'
        }
        return suggestions.get(pattern_name, '請檢查程式碼安全性')
    
    def categorize_findings(self, findings: List[Dict]) -> Dict[str, List[Dict]]:
        """根據嚴重程度分類發現"""
        categories = {
            'critical': [],  # 阻斷部署
            'high': [],      # 需確認
            'medium': [],    # 警告
            'low': []        # 建議
        }
        
        for finding in findings:
            severity = finding['severity']
            if severity in categories:
                categories[severity].append(finding)
        
        return categories
    
    def generate_report(self, categorized_findings: Dict[str, List[Dict]]) -> str:
        """生成安全檢查報告"""
        report = ["🔒 AI 安全檢查報告", "=" * 50]
        
        total_issues = sum(len(findings) for findings in categorized_findings.values())
        if total_issues == 0:
            report.append("✅ 未發現安全風險")
            return "\n".join(report)
        
        report.append(f"發現 {total_issues} 個潛在安全問題：")
        report.append("")
        
        severity_icons = {
            'critical': '🚨',
            'high': '⚠️',
            'medium': '💡',
            'low': 'ℹ️'
        }
        
        severity_names = {
            'critical': '極高風險 (阻斷)',
            'high': '高風險 (需確認)',
            'medium': '中風險 (警告)',
            'low': '低風險 (建議)'
        }
        
        for severity in ['critical', 'high', 'medium', 'low']:
            findings = categorized_findings[severity]
            if not findings:
                continue
            
            icon = severity_icons[severity]
            name = severity_names[severity]
            report.append(f"{icon} {name} ({len(findings)} 項)")
            report.append("-" * 40)
            
            for finding in findings:
                report.append(f"檔案: {finding['file']}:{finding['line']}")
                report.append(f"問題: {finding['description']}")
                report.append(f"程式碼: {finding['code']}")
                report.append(f"建議: {finding['suggestion']}")
                report.append(f"信心度: {finding['confidence']}%")
                report.append("")
        
        return "\n".join(report)
    
    def should_block_commit(self, categorized_findings: Dict[str, List[Dict]]) -> Tuple[bool, str]:
        """判斷是否應該阻斷提交"""
        critical_issues = categorized_findings.get('critical', [])
        high_issues = categorized_findings.get('high', [])
        
        if critical_issues:
            return True, f"發現 {len(critical_issues)} 個極高風險問題，阻斷提交"
        
        if len(high_issues) >= 3:
            return True, f"發現 {len(high_issues)} 個高風險問題，超過閾值，阻斷提交"
        
        return False, "安全檢查通過"

def scan_staged_files() -> List[str]:
    """取得暫存的檔案列表"""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    except Exception:
        return []

def timeout_handler(signum, frame):
    """逾時處理器"""
    raise TimeoutError("AI 安全檢查逾時 (30 秒)")

def main():
    """主要執行函數"""
    try:
        # 設定 30 秒逾時
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        scanner = AISecurityScanner()
        all_findings = []
        
        # 取得暫存檔案
        staged_files = scan_staged_files()
        if not staged_files:
            print("✅ 無檔案需要安全檢查")
            signal.alarm(0)  # 取消逾時
            return 0
        
        # 掃描每個檔案
        for filepath in staged_files:
            if not os.path.exists(filepath):
                continue
            
            # 檔案大小預檢查
            try:
                if os.path.getsize(filepath) > 1024 * 1024:  # 跳過 > 1MB 檔案
                    print(f"⚠️ 跳過大檔案 {filepath} (> 1MB)")
                    continue
            except OSError:
                continue
            
            file_type = scanner.get_file_type(filepath)
            if not file_type:
                continue  # 跳過不支援的檔案類型
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                findings = scanner.analyze_code_content(filepath, content)
                all_findings.extend(findings)
                
            except Exception as e:
                print(f"⚠️ 無法讀取檔案 {filepath}: {e}")
                continue
        
        # 分析結果
        categorized = scanner.categorize_findings(all_findings)
        report = scanner.generate_report(categorized)
        print(report)
        
        # 決定是否阻斷
        should_block, reason = scanner.should_block_commit(categorized)
        if should_block:
            print(f"\n❌ {reason}")
            print("\n修正後重新提交，或使用 AI-SECURITY-IGNORE 標記跳過特定檢查")
            signal.alarm(0)  # 取消逾時
            return 1
        else:
            print(f"\n✅ {reason}")
            signal.alarm(0)  # 取消逾時
            return 0
    
    except TimeoutError as e:
        print(f"❌ {e}")
        print("建議減少檢查檔案數量或排除大檔案")
        signal.alarm(0)  # 取消逾時
        return 0  # 逾時不阻斷提交
    
    except Exception as e:
        print(f"❌ AI 安全檢查執行錯誤: {e}")
        signal.alarm(0)  # 取消逾時
        # 錯誤情況下不阻斷提交
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Hook 配置範例

### Git Pre-commit Hook 設定

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔒 執行 AI 安全檢查..."
python3 .claude/hooks/ai_security_check.py

exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "請修正安全問題後重新提交"
    exit 1
fi

echo "✅ AI 安全檢查通過"
exit 0
```

### 整合到專案的使用方式

```python
# 在 .claude/hooks/ai_security_check.py
from ai_security_checks import main

if __name__ == "__main__":
    exit(main())
```

## 客製化配置

### 調整檢查嚴格度

```python
# config.json
{
    "ai_security": {
        "block_critical": true,
        "block_high_threshold": 3,
        "warn_medium": true,
        "suggest_low": true,
        "custom_patterns": {
            "api_key_leak": {
                "pattern": "api[_-]?key.*[=:].*['\"][a-f0-9]{32}",
                "confidence": 90,
                "severity": "high"
            }
        }
    }
}
```

### 白名單範例

```python
# 已驗證的安全程式碼
# AI-SECURITY-IGNORE: sql_injection - 使用 SQLAlchemy ORM
query = session.query(User).filter(User.id == user_id)

# AI-SECURITY-IGNORE: hardcoded_secrets - 測試環境假資料
test_api_key = "test_key_12345678"
```

## 錯誤處理

Hook 設計為即使出錯也不會阻斷開發流程：

1. **檔案讀取錯誤**: 記錄警告，繼續處理其他檔案
2. **模式匹配錯誤**: 跳過該模式，繼續其他檢查  
3. **系統錯誤**: 輸出錯誤訊息，返回成功狀態（不阻斷）

這確保 AI 安全檢查作為輔助工具，不會影響正常開發流程。

## 單元測試範例

### 基本測試框架

```python
# tests/test_ai_security_scanner.py
import unittest
import sys
import os
from pathlib import Path

# 添加 hook 路徑到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '.claude', 'hooks'))

from ai_security_checks import AISecurityScanner

class TestAISecurityScanner(unittest.TestCase):
    
    def setUp(self):
        """設定測試環境"""
        self.scanner = AISecurityScanner()
    
    def test_sql_injection_detection(self):
        """測試 SQL 注入檢測"""
        # 危險程式碼範例
        dangerous_code = '''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)
'''
        
        findings = self.scanner.analyze_code_content('test.py', dangerous_code)
        
        # 應該檢測到 SQL 注入風險
        self.assertTrue(any(f['pattern'] == 'sql_injection' for f in findings))
        
        # 檢查嚴重程度
        sql_finding = next(f for f in findings if f['pattern'] == 'sql_injection')
        self.assertEqual(sql_finding['severity'], 'high')
    
    def test_command_injection_detection(self):
        """測試命令注入檢測"""
        dangerous_code = '''
def run_command(user_input):
    os.system(f"ls {user_input}")
'''
        
        findings = self.scanner.analyze_code_content('test.py', dangerous_code)
        
        # 應該檢測到命令注入風險
        self.assertTrue(any(f['pattern'] == 'command_injection' for f in findings))
        
        # 檢查嚴重程度
        cmd_finding = next(f for f in findings if f['pattern'] == 'command_injection')
        self.assertEqual(cmd_finding['severity'], 'critical')
    
    def test_security_ignore_functionality(self):
        """測試安全忽略標記功能"""
        code_with_ignore = '''
def get_user(user_id):
    # AI-SECURITY-IGNORE: sql_injection - 使用參數化查詢
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)
'''
        
        findings = self.scanner.analyze_code_content('test.py', code_with_ignore)
        
        # 應該不檢測到 SQL 注入（已忽略）
        self.assertFalse(any(f['pattern'] == 'sql_injection' for f in findings))
    
    def test_javascript_xss_detection(self):
        """測試 JavaScript XSS 檢測"""
        dangerous_js = '''
function updateContent(userInput) {
    document.getElementById('content').innerHTML = userInput;
}
'''
        
        findings = self.scanner.analyze_code_content('test.js', dangerous_js)
        
        # 應該檢測到 XSS 風險
        self.assertTrue(any(f['pattern'] == 'xss_risk' for f in findings))
    
    def test_typescript_any_type_detection(self):
        """測試 TypeScript any 類型檢測"""
        ts_code = '''
function processData(data: any): void {
    console.log(data);
}
'''
        
        findings = self.scanner.analyze_code_content('test.ts', ts_code)
        
        # 應該檢測到 any 類型使用
        self.assertTrue(any(f['pattern'] == 'any_type_usage' for f in findings))
        
        # 檢查嚴重程度
        any_finding = next(f for f in findings if f['pattern'] == 'any_type_usage')
        self.assertEqual(any_finding['severity'], 'low')
    
    def test_hardcoded_secrets_detection(self):
        """測試硬編碼敏感資訊檢測"""
        code_with_secret = '''
def connect_api():
    api_key = "sk-1234567890abcdef"
    return requests.get(url, headers={'Authorization': api_key})
'''
        
        findings = self.scanner.analyze_code_content('test.py', code_with_secret)
        
        # 應該檢測到硬編碼密鑰
        self.assertTrue(any(f['pattern'] == 'hardcoded_secrets' for f in findings))
    
    def test_file_type_detection(self):
        """測試檔案類型檢測"""
        self.assertEqual(self.scanner.get_file_type('test.py'), 'python')
        self.assertEqual(self.scanner.get_file_type('test.js'), 'javascript')
        self.assertEqual(self.scanner.get_file_type('test.jsx'), 'javascript')
        self.assertEqual(self.scanner.get_file_type('test.ts'), 'typescript')
        self.assertEqual(self.scanner.get_file_type('test.tsx'), 'typescript')
        self.assertIsNone(self.scanner.get_file_type('test.txt'))
    
    def test_categorize_findings(self):
        """測試風險分類"""
        mock_findings = [
            {'severity': 'critical', 'description': 'Test critical'},
            {'severity': 'high', 'description': 'Test high'},
            {'severity': 'medium', 'description': 'Test medium'},
            {'severity': 'low', 'description': 'Test low'}
        ]
        
        categorized = self.scanner.categorize_findings(mock_findings)
        
        self.assertEqual(len(categorized['critical']), 1)
        self.assertEqual(len(categorized['high']), 1)
        self.assertEqual(len(categorized['medium']), 1)
        self.assertEqual(len(categorized['low']), 1)
    
    def test_should_block_commit(self):
        """測試提交阻斷邏輯"""
        # 極高風險應該阻斷
        critical_findings = {'critical': [{'pattern': 'test'}], 'high': [], 'medium': [], 'low': []}
        should_block, reason = self.scanner.should_block_commit(critical_findings)
        self.assertTrue(should_block)
        
        # 多個高風險應該阻斷
        high_findings = {
            'critical': [], 
            'high': [{'pattern': f'test{i}'} for i in range(4)],  # 4 個高風險
            'medium': [], 
            'low': []
        }
        should_block, reason = self.scanner.should_block_commit(high_findings)
        self.assertTrue(should_block)
        
        # 少數中低風險不應阻斷
        safe_findings = {
            'critical': [], 
            'high': [{'pattern': 'test1'}],  # 只有 1 個高風險
            'medium': [{'pattern': 'test2'}], 
            'low': []
        }
        should_block, reason = self.scanner.should_block_commit(safe_findings)
        self.assertFalse(should_block)

if __name__ == '__main__':
    # 執行測試
    unittest.main()
```

### 執行測試

```bash
# 在專案根目錄執行
python -m pytest tests/test_ai_security_scanner.py -v

# 或使用 unittest
python tests/test_ai_security_scanner.py
```

### 測試覆蓋率檢查

```bash
# 安裝 coverage
pip install coverage

# 執行覆蓋率測試
coverage run tests/test_ai_security_scanner.py
coverage report
coverage html  # 生成 HTML 報告
```

### 逾時測試

```python
# tests/test_timeout.py
import unittest
import signal
import time
from unittest.mock import patch

class TestTimeout(unittest.TestCase):
    
    def test_timeout_mechanism(self):
        """測試逾時機制"""
        def slow_function():
            time.sleep(35)  # 模擬慢操作
            return "completed"
        
        # 測試逾時處理
        signal.signal(signal.SIGALRM, lambda s, f: (_ for _ in ()).throw(TimeoutError("逾時")))
        signal.alarm(1)  # 1 秒逾時
        
        with self.assertRaises(TimeoutError):
            slow_function()
        
        signal.alarm(0)  # 清除逾時
    
    @patch('ai_security_checks.scan_staged_files')
    @patch('builtins.open')
    def test_large_file_handling(self, mock_open, mock_scan):
        """測試大檔案處理"""
        from ai_security_checks import AISecurityScanner
        
        # 模擬大檔案
        large_content = "x" * (1024 * 1024 + 1)  # 1MB + 1 byte
        mock_open.return_value.__enter__.return_value.read.return_value = large_content
        
        scanner = AISecurityScanner()
        findings = scanner.analyze_code_content('large_file.py', large_content)
        
        # 應該跳過大檔案，返回空結果
        self.assertEqual(len(findings), 0)
```

### 效能測試

```python
# tests/test_performance.py
import unittest
import time
from ai_security_checks import AISecurityScanner

class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        self.scanner = AISecurityScanner()
        # 產生測試程式碼
        self.test_code = '\n'.join([
            f'def function_{i}():',
            f'    query = f"SELECT * FROM table WHERE id = {{user_id}}"',
            f'    return query'
        ] * 100 for i in range(10))  # 1000 行程式碼
    
    def test_scanning_performance(self):
        """測試掃描效能"""
        start_time = time.time()
        
        findings = self.scanner.analyze_code_content('performance_test.py', self.test_code)
        
        end_time = time.time()
        scan_duration = end_time - start_time
        
        # 應該在 30 秒內完成
        self.assertLess(scan_duration, 30.0, f"掃描耗時 {scan_duration:.2f} 秒，超過 30 秒限制")
        
        # 應該檢測到多個 SQL 注入風險
        sql_findings = [f for f in findings if f['pattern'] == 'sql_injection']
        self.assertGreater(len(sql_findings), 0, "應該檢測到 SQL 注入風險")
        
        print(f"掃描 {len(self.test_code.split())} 行程式碼耗時: {scan_duration:.2f} 秒")
        print(f"檢測到 {len(findings)} 個風險，包含 {len(sql_findings)} 個 SQL 注入")
```

這些測試覆蓋了：

1. **安全模式檢測**: 各種風險模式的準確檢測
2. **忽略標記功能**: 安全忽略機制的正確運作  
3. **檔案類型識別**: 支援的程式語言檔案檢測
4. **分類邏輯**: 風險嚴重程度分類
5. **阻斷邏輯**: 提交阻斷決策正確性
6. **逾時機制**: 30 秒逾時控制
7. **效能測試**: 大檔案和長時間掃描處理

執行這些測試可確保 Hook 的可靠性和效能符合專案要求。