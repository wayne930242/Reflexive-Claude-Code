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
        
        findings = []
        lines = content.split('\n')
        
        # 取得對應語言的風險模式
        language_patterns = AI_RISK_PATTERNS.get(file_type, {})
        if file_type == 'typescript':
            # TypeScript 繼承 JavaScript 模式
            language_patterns.update(AI_RISK_PATTERNS.get('javascript', {}))
        
        for line_num, line in enumerate(lines, 1):
            for pattern_name, pattern_info in language_patterns.items():
                # 檢查是否有忽略標記
                if self.has_security_ignore(line, pattern_name):
                    continue
                
                # 執行模式匹配
                if re.search(pattern_info['pattern'], line, re.IGNORECASE):
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

def main():
    """主要執行函數"""
    try:
        scanner = AISecurityScanner()
        all_findings = []
        
        # 取得暫存檔案
        staged_files = scan_staged_files()
        if not staged_files:
            print("✅ 無檔案需要安全檢查")
            return 0
        
        # 掃描每個檔案
        for filepath in staged_files:
            if not os.path.exists(filepath):
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
            return 1
        else:
            print(f"\n✅ {reason}")
            return 0
    
    except Exception as e:
        print(f"❌ AI 安全檢查執行錯誤: {e}")
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