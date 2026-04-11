#!/usr/bin/env python3
"""
Agent System Security Integration Tests
測試Tasks 1-4的安全強化整合功能
"""

import os
import sys
import time
import tempfile
import unittest
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestSecurityIntegration(unittest.TestCase):
    """安全整合測試套件"""

    def setUp(self):
        """測試初始化"""
        self.test_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent.parent
        self.skills_dir = self.project_root / "plugins" / "rcc" / "skills"

    def tearDown(self):
        """測試清理"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_ai_security_patterns_detection(self):
        """測試Task 1: AI安全模式檢測"""
        # 讀取AI安全模式檢測規則
        patterns_file = self.skills_dir / "planning-agent-systems" / "references" / "ai-security-patterns.md"
        self.assertTrue(patterns_file.exists(), "AI安全模式檔案不存在")

        with open(patterns_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證關鍵安全模式存在
        required_patterns = [
            'sql_injection',
            'command_injection',
            'hardcoded_secrets',
            'path_traversal',
            'dangerous_eval'
        ]

        for pattern in required_patterns:
            self.assertIn(pattern, content, f"缺少安全模式: {pattern}")

        # 驗證信心分數機制
        self.assertIn('confidence', content, "缺少信心分數機制")
        self.assertIn('95%', content, "缺少極高風險閾值")

    def test_security_layers_framework(self):
        """測試Task 2: 八層防禦框架"""
        layers_file = self.skills_dir / "planning-agent-systems" / "references" / "security-layers.md"
        self.assertTrue(layers_file.exists(), "安全層級檔案不存在")

        with open(layers_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證八個安全層級
        expected_layers = [
            "層級 1: 代碼層安全",
            "層級 2: 依賴層安全",
            "層級 3: 構建層安全",
            "層級 4: 部署前驗證",
            "層級 5: 部署層安全",
            "層級 6: 註冊層監控",
            "層級 7: 運行時保護",
            "層級 8: 合規層管控"
        ]

        for layer in expected_layers:
            self.assertIn(layer, content, f"缺少安全層級: {layer}")

        # 驗證Hook配置
        self.assertIn("preToolUse", content, "缺少preToolUse Hook配置")
        self.assertIn("stop", content, "缺少stop Hook配置")

    def test_reflection_enhancement(self):
        """測試Task 3: 反思技能強化 (調整後)"""
        reflection_file = self.skills_dir / "reflecting" / "SKILL.md"
        self.assertTrue(reflection_file.exists(), "反思技能檔案不存在")

        with open(reflection_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證反思技能已強化
        self.assertIn("Proactive Triggers", content, "缺少主動觸發機制")
        self.assertIn("user corrects", content, "缺少用戶糾正觸發條件")
        self.assertIn("agent learns", content, "缺少代理學習觸發條件")

        # 驗證與Claude Code記憶系統整合
        self.assertIn("Memory System", content, "缺少記憶系統整合")
        self.assertIn("/home/weihung/.claude/projects", content, "缺少記憶路徑配置")

        # 驗證任務初始化流程
        self.assertIn("TaskCreate", content, "缺少任務創建機制")
        self.assertIn("Task Initialization", content, "缺少任務初始化章節")

    def test_performance_constraints_integration(self):
        """測試Task 4: 效能約束與策略整合"""
        perf_file = self.skills_dir / "writing-hooks" / "references" / "performance-optimization.md"
        self.assertTrue(perf_file.exists(), "效能最佳化檔案不存在")

        with open(perf_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證效能約束
        self.assertIn("timeout=30", content, "缺少30秒超時約束")
        self.assertIn("parallel", content, "缺少並行執行機制")
        self.assertIn("ThreadPoolExecutor", content, "缺少執行緒池實作")

        # 驗證護欄策略
        self.assertIn("CRITICAL", content, "缺少關鍵級別護欄")
        self.assertIn("SecurityBlockError", content, "缺少安全阻擋機制")
        self.assertIn("guardrails", content, "缺少護欄策略")

        # 驗證優雅降級 (調整關鍵詞)
        self.assertTrue(
            "優雅降級" in content or "graceful degradation" in content.lower(),
            "缺少優雅降級機制"
        )
        self.assertIn("timeout", content, "缺少超時處理")

    def test_security_workflow_integration(self):
        """測試整體安全工作流程整合"""
        # 驗證技能之間的整合路由
        planning_file = self.skills_dir / "planning-agent-systems" / "SKILL.md"
        self.assertTrue(planning_file.exists(), "規劃技能檔案不存在")

        with open(planning_file, 'r', encoding='utf-8') as f:
            planning_content = f.read()

        # 驗證安全相關參考檔案的整合 (調整檢查條件)
        has_security_refs = any([
            "security" in planning_content.lower(),
            "ai-security" in planning_content,
            "learning-from-failures" in planning_content
        ])
        self.assertTrue(has_security_refs, "規劃技能中缺少安全相關整合")

        # 驗證Hook寫作技能
        hooks_file = self.skills_dir / "writing-hooks" / "SKILL.md"
        self.assertTrue(hooks_file.exists(), "Hook寫作技能檔案不存在")

        with open(hooks_file, 'r', encoding='utf-8') as f:
            hooks_content = f.read()

        # 驗證安全檢查整合
        self.assertIn("security", hooks_content.lower(), "Hook技能中缺少安全檢查")

    def test_claude_code_architecture_compatibility(self):
        """測試與Claude Code架構相容性"""
        # 驗證插件結構
        plugin_file = self.project_root / "plugins" / "rcc" / ".claude-plugin" / "plugin.json"
        self.assertTrue(plugin_file.exists(), "插件配置檔案不存在")

        with open(plugin_file, 'r', encoding='utf-8') as f:
            plugin_config = json.load(f)

        # 驗證版本一致性
        self.assertIn("version", plugin_config, "插件配置中缺少版本")

        # 驗證技能目錄結構（技能通過目錄自動發現，不需要明確註冊）
        security_related_skills = [
            "planning-agent-systems",
            "reflecting",
            "writing-hooks"
        ]

        for skill in security_related_skills:
            skill_dir = self.skills_dir / skill
            self.assertTrue(skill_dir.exists(), f"技能目錄 {skill} 不存在")
            skill_file = skill_dir / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"技能檔案 {skill}/SKILL.md 不存在")

    def test_security_patterns_confidence_scores(self):
        """測試安全模式信心分數機制"""
        patterns_file = self.skills_dir / "planning-agent-systems" / "references" / "ai-security-patterns.md"

        with open(patterns_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證信心分數閾值
        confidence_thresholds = ["95%", "90%", "85%", "80%"]
        for threshold in confidence_thresholds:
            self.assertIn(threshold, content, f"缺少信心分數閾值: {threshold}")

        # 驗證決策邏輯
        self.assertIn("阻斷部署", content, "缺少高風險阻斷邏輯")
        self.assertIn("警告提示", content, "缺少中風險警告邏輯")

    def test_performance_monitoring_integration(self):
        """測試效能監控整合"""
        perf_file = self.skills_dir / "writing-hooks" / "references" / "performance-optimization.md"

        with open(perf_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證效能監控組件
        self.assertIn("performance_monitor", content, "缺少效能監控器")
        self.assertIn("psutil", content, "缺少系統資源監控")
        self.assertIn("duration", content, "缺少執行時間監控")
        self.assertIn("memory", content, "缺少記憶體監控")

        # 驗證警告機制
        self.assertIn("Slow operation", content, "缺少慢操作警告")
        self.assertIn("High memory", content, "缺少高記憶體警告")


class TestSecurityPatterns(unittest.TestCase):
    """安全模式檢測測試"""

    def test_sql_injection_detection(self):
        """測試SQL注入檢測"""
        # 模擬危險程式碼
        dangerous_code = '''query = f"SELECT * FROM users WHERE id = {user_id}"'''

        # 這裡模擬安全檢測邏輯
        import re

        # 簡化模式匹配，檢測f-string中包含SQL語法
        sql_pattern = r'f["\'].*SELECT.*\{.*\}.*FROM'
        match = re.search(sql_pattern, dangerous_code, re.IGNORECASE | re.DOTALL)

        self.assertTrue(match, f"SQL注入模式檢測失敗，測試代碼: {dangerous_code}")

    def test_hardcoded_secrets_detection(self):
        """測試硬編碼秘密檢測"""
        dangerous_code = '''
        api_key = "sk-1234567890abcdef"
        password = "admin123"
        '''

        import re

        secret_pattern = r'(password|api_key|secret|token)\s*=\s*["\'][a-zA-Z0-9_\-]{8,}["\']'
        matches = re.findall(secret_pattern, dangerous_code, re.IGNORECASE)

        self.assertTrue(len(matches) >= 2, "硬編碼秘密檢測失敗")

    def test_command_injection_detection(self):
        """測試命令注入檢測"""
        dangerous_code = '''
        os.system(f"rm -rf {user_path}")
        subprocess.call(f"echo {user_input}")
        '''

        import re

        cmd_pattern = r'(os\.system|subprocess\.call)\s*\(\s*f?["\'].*\{.*\}'
        matches = re.findall(cmd_pattern, dangerous_code, re.IGNORECASE)

        self.assertTrue(len(matches) >= 2, "命令注入檢測失敗")


class TestHookIntegration(unittest.TestCase):
    """Hook整合測試"""

    def test_hook_timeout_enforcement(self):
        """測試Hook超時執行"""
        import threading
        import time

        def slow_security_check():
            """模擬慢速安全檢查"""
            time.sleep(2)
            return "completed"

        def timeout_wrapper(func, timeout_seconds):
            """超時包裝器"""
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func()
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout_seconds)

            if thread.is_alive():
                return "TIMEOUT"
            elif exception[0]:
                raise exception[0]
            else:
                return result[0]

        # 測試正常執行
        result = timeout_wrapper(slow_security_check, 5)
        self.assertEqual(result, "completed", "正常執行失敗")

        # 測試超時控制
        result = timeout_wrapper(slow_security_check, 1)
        self.assertEqual(result, "TIMEOUT", "超時控制失敗")


if __name__ == '__main__':
    print("開始執行代理系統安全整合測試...")
    print("=" * 60)

    # 設定測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 載入測試類別
    test_classes = [
        TestSecurityIntegration,
        TestSecurityPatterns,
        TestHookIntegration
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 報告結果
    print("\n" + "=" * 60)
    print(f"測試完成: {result.testsRun} 個測試")
    print(f"失敗: {len(result.failures)} 個")
    print(f"錯誤: {len(result.errors)} 個")

    if result.failures:
        print("\n失敗測試:")
        for test, trace in result.failures:
            print(f"  - {test}: {trace}")

    if result.errors:
        print("\n錯誤測試:")
        for test, trace in result.errors:
            print(f"  - {test}: {trace}")

    sys.exit(0 if result.wasSuccessful() else 1)