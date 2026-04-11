# AI 安全模式參考

## 統計數據

2026 年研究顯示：
- **62%** 的 AI 生成程式碼包含安全漏洞
- **38%** 的開發者無法識別 AI 程式碼中的安全問題
- **74%** 的 AI 漏洞集中在 5 個高風險模式

## AI 程式碼高風險模式

### 1. 注入攻擊模式
```python
# 危險：直接字串拼接
query = f"SELECT * FROM users WHERE id = {user_id}"

# 危險：格式化字串
os.system(f"rm -rf {user_path}")
```

**信心分數:** 95% (極高風險)

### 2. 硬編碼敏感資訊
```python
# 危險：硬編碼密鑰
api_key = "sk-1234567890abcdef"
password = "admin123"
```

**信心分數:** 90% (極高風險)

### 3. 不安全的檔案操作
```python
# 危險：路徑遍歷
file_path = request.get('path')
with open(file_path, 'r') as f:
    content = f.read()
```

**信心分數:** 85% (高風險)

### 4. 權限提升模式
```python
# 危險：不檢查權限
if user.role == 'admin':
    delete_all_data()
```

**信心分數:** 80% (高風險)

### 5. 輸入驗證缺失
```python
# 危險：未驗證輸入
eval(user_input)
exec(code_from_api)
```

**信心分數:** 95% (極高風險)

## 檢測策略

### Python Regex 模式

```python
AI_RISK_PATTERNS = {
    'sql_injection': {
        'pattern': r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']|f["\'].*\{.*\}.*FROM',
        'confidence': 90,
        'description': 'SQL 注入風險：字串拼接查詢'
    },
    'command_injection': {
        'pattern': r'(os\.system|subprocess\.call|eval|exec)\s*\(\s*f?["\'].*\{.*\}',
        'confidence': 95,
        'description': '命令注入風險：格式化字串執行'
    },
    'hardcoded_secrets': {
        'pattern': r'(password|api_key|secret|token)\s*=\s*["\'][a-zA-Z0-9_\-]{8,}["\']',
        'confidence': 85,
        'description': '硬編碼敏感資訊'
    },
    'path_traversal': {
        'pattern': r'open\s*\(\s*(request\.|user_|input_)',
        'confidence': 80,
        'description': '路徑遍歷風險：未驗證檔案路徑'
    },
    'dangerous_eval': {
        'pattern': r'\b(eval|exec)\s*\(',
        'confidence': 95,
        'description': '危險程式碼執行：eval/exec'
    }
}
```

### JavaScript 模式

```javascript
const AI_JS_PATTERNS = {
    'xss_risk': {
        pattern: /innerHTML\s*=.*\+|document\.write\s*\(/,
        confidence: 85,
        description: 'XSS 風險：動態 HTML 注入'
    },
    'prototype_pollution': {
        pattern: /__proto__|constructor\s*\[.*\]|\.prototype\s*\[/,
        confidence: 90,
        description: '原型污染風險'
    }
};
```

## 品質關卡設計

### 三層檢驗架構

```
Layer 1: 語法檢查 (Confidence >= 95%)
├── 阻斷部署
└── 強制修正

Layer 2: 安全掃描 (Confidence >= 80%)
├── 警告提示
└── 需確認繼續

Layer 3: 最佳實踐 (Confidence >= 60%)
├── 建議改進
└── 可選修正
```

### 信心分數門檻

- **95-100%**: 極高風險，阻斷部署
- **80-94%**: 高風險，需人工確認
- **60-79%**: 中風險，警告提示
- **<60%**: 低風險，建議改進

## 實施建議

1. **預提交檢查**: 在 Git hooks 中實施第一層檢查
2. **CI/CD 整合**: 在管道中添加完整三層掃描
3. **開發時檢查**: IDE 插件即時提示
4. **定期審計**: 定時全程式碼基掃描

## 誤報處理

### 白名單機制
```python
# 允許標記跳過檢查
# AI-SECURITY-IGNORE: sql_injection - 已驗證參數安全性
query = f"SELECT * FROM table WHERE id = {validated_id}"
```

### 上下文分析
檢查是否有對應的安全措施：
- 輸入驗證
- 參數化查詢
- 權限檢查
- 錯誤處理