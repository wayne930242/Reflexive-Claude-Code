#!/usr/bin/env python3
"""
Reflection Integration Tests
測試Task 3調整後的反思技能整合功能
"""

import os
import sys
import time
import tempfile
import unittest
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestReflectionEnhancement(unittest.TestCase):
    """反思技能強化測試"""

    def setUp(self):
        """測試初始化"""
        self.test_dir = tempfile.mkdtemp()
        self.project_root = Path(__file__).parent.parent.parent
        self.skills_dir = self.project_root / "plugins" / "rcc" / "skills"
        self.memory_dir = Path.home() / ".claude" / "projects" / "-home-weihung-Reflexive-Claude-Code" / "memory"

    def tearDown(self):
        """測試清理"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_proactive_reflection_triggers(self):
        """測試主動反思觸發條件"""
        reflection_file = self.skills_dir / "reflecting" / "SKILL.md"
        self.assertTrue(reflection_file.exists(), "反思技能檔案不存在")

        with open(reflection_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證主動觸發條件
        required_triggers = [
            "User corrects your approach",
            "Agent discovers unexpected patterns",
            "Failed assumptions are revealed",
            "New knowledge emerges",
            "User provides feedback",
            "Workflow gaps or improvement opportunities"
        ]

        for trigger in required_triggers:
            self.assertIn(trigger, content, f"缺少觸發條件: {trigger}")

        # 驗證觸發章節存在
        self.assertIn("Proactive Triggers", content, "缺少主動觸發章節")
        self.assertIn("When to self-trigger reflection", content, "缺少自觸發說明")

    def test_memory_system_integration(self):
        """測試與Claude Code記憶系統整合"""
        reflection_file = self.skills_dir / "reflecting" / "SKILL.md"

        with open(reflection_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證記憶系統整合說明
        self.assertIn("Integration with Memory System", content, "缺少記憶系統整合章節")
        self.assertIn("/home/weihung/.claude/projects", content, "缺少記憶路徑說明")
        self.assertIn("built-in memory system", content, "缺少內建記憶系統說明")
        self.assertIn("No additional memory management needed", content, "缺少記憶管理說明")

        # 驗證報告自動整合
        self.assertIn("automatically feed into", content, "缺少自動整合說明")

    def test_task_based_workflow_structure(self):
        """測試基於任務的工作流程結構"""
        reflection_file = self.skills_dir / "reflecting" / "SKILL.md"

        with open(reflection_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證任務初始化結構
        self.assertIn("Task Initialization (MANDATORY)", content, "缺少任務初始化章節")
        self.assertIn("TaskCreate", content, "缺少TaskCreate機制")

        # 驗證5個主要任務
        expected_tasks = [
            "Task 1: Analyze conversation",
            "Task 2: Extract knowledge",
            "Task 3: Produce reflection report",
            "Task 4: Review report quality",
            "Task 5: Route to planning"
        ]

        for task in expected_tasks:
            self.assertIn(task, content, f"缺少任務: {task}")

        # 驗證任務執行規則
        self.assertIn("status=\"in_progress\"", content, "缺少任務進度狀態")
        self.assertIn("status=\"completed\"", content, "缺少任務完成狀態")

    def test_learning_extraction_mechanism(self):
        """測試學習擷取機制"""
        reflection_file = self.skills_dir / "reflecting" / "SKILL.md"

        with open(reflection_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 驗證事件分析
        event_types = [
            "correction",
            "error",
            "discovery",
            "repetition"
        ]

        for event_type in event_types:
            self.assertIn(event_type, content, f"缺少事件類型: {event_type}")

        # 驗證學習格式
        learning_components = [
            "context:",
            "insight:",
            "evidence:",
            "suggested_component:",
            "rationale:"
        ]

        for component in learning_components:
            self.assertIn(component, content, f"缺少學習組件: {component}")

        # 驗證組件類型
        component_types = ["rule", "law", "skill", "hook", "doc"]
        for comp_type in component_types:
            self.assertIn(comp_type, content, f"缺少組件類型: {comp_type}")

    def test_reflection_report_generation(self):
        """測試反思報告生成"""
        # 檢查報告模板
        template_file = self.skills_dir / "reflecting" / "references" / "report-template.md"
        self.assertTrue(template_file.exists(), "反思報告模板不存在")

        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 驗證報告結構
        required_sections = [
            "Session Context",
            "Events",
            "Learnings",
            "Component Recommendations",
            "Completeness Checklist"
        ]

        for section in required_sections:
            self.assertIn(section, template_content, f"報告模板缺少章節: {section}")

    def test_user_correction_trigger_simulation(self):
        """模擬用戶糾正觸發反思"""

        class MockReflectionContext:
            """模擬反思上下文"""

            def __init__(self):
                self.events = []
                self.learnings = []

            def detect_user_correction(self, conversation_text):
                """檢測用戶糾正事件"""
                correction_indicators = [
                    "actually",
                    "correction",
                    "that's wrong",
                    "should be",
                    "let me clarify",
                    "not quite right"
                ]

                corrections = []
                for indicator in correction_indicators:
                    if indicator.lower() in conversation_text.lower():
                        corrections.append({
                            "type": "correction",
                            "indicator": indicator,
                            "context": "User provided correction",
                            "timestamp": time.time()
                        })

                return corrections

            def should_trigger_reflection(self, events):
                """判斷是否應該觸發反思"""
                if not events:
                    return False

                # 如果有糾正事件，立即觸發
                correction_events = [e for e in events if e.get("type") == "correction"]
                return len(correction_events) > 0

        # 測試用戶糾正檢測
        mock_context = MockReflectionContext()

        # 模擬包含糾正的對話
        conversation_with_correction = """
        User: Actually, that's not quite right. The security check should use async/await pattern.
        Assistant: Let me clarify the implementation...
        """

        corrections = mock_context.detect_user_correction(conversation_with_correction)
        self.assertGreater(len(corrections), 0, "未檢測到用戶糾正")

        # 測試觸發決策
        should_trigger = mock_context.should_trigger_reflection(corrections)
        self.assertTrue(should_trigger, "糾正事件未觸發反思")

    def test_agent_learning_trigger_simulation(self):
        """模擬代理學習觸發反思"""

        class MockAgentLearning:
            """模擬代理學習檢測"""

            def detect_learning_events(self, conversation_text):
                """檢測代理學習事件"""
                learning_indicators = [
                    "I discovered",
                    "I learned",
                    "unexpected pattern",
                    "new insight",
                    "it turns out",
                    "I realize now"
                ]

                events = []
                for indicator in learning_indicators:
                    if indicator.lower() in conversation_text.lower():
                        events.append({
                            "type": "discovery",
                            "indicator": indicator,
                            "context": "Agent discovered new pattern",
                            "timestamp": time.time()
                        })

                return events

            def extract_learnings(self, events):
                """從事件中擷取學習"""
                learnings = []

                for event in events:
                    learning = {
                        "context": "Pattern discovery during execution",
                        "insight": f"New understanding from {event['indicator']}",
                        "evidence": event["context"],
                        "suggested_component": "rule",  # 簡化為規則
                        "rationale": "Pattern can be codified as project convention"
                    }
                    learnings.append(learning)

                return learnings

        # 測試代理學習檢測
        mock_learning = MockAgentLearning()

        conversation_with_learning = """
        I discovered that the security patterns we implemented have a high false positive rate.
        It turns out that the confidence threshold needs adjustment for JavaScript files.
        """

        learning_events = mock_learning.detect_learning_events(conversation_with_learning)
        self.assertGreater(len(learning_events), 0, "未檢測到代理學習事件")

        # 測試學習擷取
        learnings = mock_learning.extract_learnings(learning_events)
        self.assertEqual(len(learnings), len(learning_events), "學習擷取數量不符")

        # 驗證學習結構
        for learning in learnings:
            required_fields = ["context", "insight", "evidence", "suggested_component", "rationale"]
            for field in required_fields:
                self.assertIn(field, learning, f"學習記錄缺少欄位: {field}")

    def test_reflection_quality_validation(self):
        """測試反思品質驗證"""

        class MockReflectionValidator:
            """模擬反思品質驗證器"""

            def validate_completeness(self, report_data):
                """驗證報告完整性"""
                errors = []

                # 檢查必要章節
                required_sections = ["events", "learnings", "components"]
                for section in required_sections:
                    if section not in report_data:
                        errors.append(f"Missing section: {section}")

                # 檢查事件與學習對應
                if "events" in report_data and "learnings" in report_data:
                    if len(report_data["learnings"]) == 0 and len(report_data["events"]) > 0:
                        errors.append("Events found but no learnings extracted")

                # 檢查組件建議
                if "learnings" in report_data:
                    for learning in report_data["learnings"]:
                        if "suggested_component" not in learning:
                            errors.append("Learning missing component suggestion")

                return len(errors) == 0, errors

        # 測試完整報告
        validator = MockReflectionValidator()

        complete_report = {
            "events": [
                {"type": "correction", "context": "User corrected approach", "outcome": "Fixed"}
            ],
            "learnings": [
                {
                    "context": "Security implementation",
                    "insight": "Timeout needed for long checks",
                    "evidence": "User correction about performance",
                    "suggested_component": "rule",
                    "rationale": "Performance constraint should be codified"
                }
            ],
            "components": [
                {"type": "rule", "path": "CLAUDE.md", "summary": "30-second timeout rule"}
            ]
        }

        is_valid, errors = validator.validate_completeness(complete_report)
        self.assertTrue(is_valid, f"完整報告驗證失敗: {errors}")

        # 測試不完整報告
        incomplete_report = {
            "events": [{"type": "error", "context": "Something failed"}],
            "learnings": []  # 有事件但無學習
        }

        is_valid, errors = validator.validate_completeness(incomplete_report)
        self.assertFalse(is_valid, "不完整報告應該驗證失敗")
        self.assertIn("no learnings extracted", str(errors), "未檢測到學習缺失")


class TestReflectionIntegrationFlow(unittest.TestCase):
    """反思整合流程測試"""

    def test_end_to_end_reflection_workflow(self):
        """測試端到端反思工作流程"""

        class MockReflectionWorkflow:
            """模擬完整反思工作流程"""

            def __init__(self):
                self.current_task = 0
                self.tasks = [
                    "analyze_conversation",
                    "extract_knowledge",
                    "produce_report",
                    "review_quality",
                    "route_to_planning"
                ]
                self.task_status = {}

            def execute_workflow(self, conversation_data):
                """執行完整工作流程"""
                results = {}

                try:
                    # Task 1: 分析對話
                    events = self.analyze_conversation(conversation_data)
                    self.update_task_status("analyze_conversation", "completed")
                    results["events"] = events

                    # Task 2: 擷取知識
                    learnings = self.extract_knowledge(events)
                    self.update_task_status("extract_knowledge", "completed")
                    results["learnings"] = learnings

                    # Task 3: 生成報告
                    report = self.produce_report(events, learnings)
                    self.update_task_status("produce_report", "completed")
                    results["report"] = report

                    # Task 4: 品質審查
                    quality_check = self.review_quality(report)
                    self.update_task_status("review_quality", "completed")
                    results["quality_passed"] = quality_check

                    # Task 5: 路由到規劃
                    if quality_check:
                        planning_result = self.route_to_planning(report)
                        self.update_task_status("route_to_planning", "completed")
                        results["planning_routed"] = planning_result

                    return True, results

                except Exception as e:
                    return False, {"error": str(e)}

            def analyze_conversation(self, data):
                """分析對話"""
                return [
                    {"type": "correction", "context": "User feedback", "outcome": "Improved"}
                ]

            def extract_knowledge(self, events):
                """擷取知識"""
                return [
                    {
                        "context": "Security implementation",
                        "insight": "Need better error handling",
                        "suggested_component": "hook"
                    }
                ]

            def produce_report(self, events, learnings):
                """生成報告"""
                return {
                    "timestamp": "2026-04-12",
                    "events": events,
                    "learnings": learnings,
                    "components": []
                }

            def review_quality(self, report):
                """品質審查"""
                return len(report.get("events", [])) > 0 and len(report.get("learnings", [])) > 0

            def route_to_planning(self, report):
                """路由到規劃"""
                return True  # 模擬成功路由

            def update_task_status(self, task, status):
                """更新任務狀態"""
                self.task_status[task] = status

        # 執行完整工作流程
        workflow = MockReflectionWorkflow()

        conversation_data = {
            "user_corrections": ["Security timeout too aggressive"],
            "agent_discoveries": ["Found performance bottleneck in parallel execution"]
        }

        success, results = workflow.execute_workflow(conversation_data)

        # 驗證工作流程成功
        self.assertTrue(success, f"工作流程執行失敗: {results}")

        # 驗證所有任務完成
        for task in workflow.tasks:
            self.assertEqual(workflow.task_status.get(task), "completed", f"任務 {task} 未完成")

        # 驗證結果完整性
        self.assertIn("events", results, "缺少事件分析結果")
        self.assertIn("learnings", results, "缺少學習擷取結果")
        self.assertIn("report", results, "缺少報告生成結果")
        self.assertTrue(results.get("quality_passed"), "品質審查失敗")
        self.assertTrue(results.get("planning_routed"), "規劃路由失敗")

    def test_memory_system_integration_simulation(self):
        """模擬記憶系統整合"""

        class MockMemoryIntegration:
            """模擬記憶系統整合"""

            def __init__(self, memory_base_path):
                self.memory_path = Path(memory_base_path)
                self.stored_reflections = []

            def store_reflection_report(self, report):
                """儲存反思報告到記憶系統"""
                # 模擬儲存到Claude Code記憶系統
                timestamp = report.get("timestamp", "unknown")
                filename = f"{timestamp}-reflection.md"

                # 模擬檔案內容
                content = self.format_report_for_memory(report)

                # 記錄儲存動作（實際應該寫檔案）
                self.stored_reflections.append({
                    "filename": filename,
                    "content": content,
                    "path": self.memory_path / filename
                })

                return True

            def format_report_for_memory(self, report):
                """格式化報告為記憶系統格式"""
                events = report.get("events", [])
                learnings = report.get("learnings", [])

                formatted = f"""# Reflection Report {report.get("timestamp")}

## Events
{len(events)} events captured

## Learnings
{len(learnings)} learnings extracted

## Integration Status
- Automatically integrated into Claude Code memory system
- Available for future planning and decision making
"""
                return formatted

            def retrieve_reflection_history(self):
                """檢索反思歷史"""
                return self.stored_reflections

        # 測試記憶整合
        memory_path = self.test_dir / "mock_memory"
        memory_integration = MockMemoryIntegration(memory_path)

        sample_report = {
            "timestamp": "2026-04-12",
            "events": [{"type": "correction", "context": "Test"}],
            "learnings": [{"insight": "Test learning", "suggested_component": "rule"}]
        }

        # 儲存報告
        stored = memory_integration.store_reflection_report(sample_report)
        self.assertTrue(stored, "反思報告儲存失敗")

        # 檢索歷史
        history = memory_integration.retrieve_reflection_history()
        self.assertEqual(len(history), 1, "反思歷史檢索失敗")

        # 驗證格式
        stored_report = history[0]
        self.assertIn("2026-04-12-reflection.md", stored_report["filename"])
        self.assertIn("Claude Code memory system", stored_report["content"])


if __name__ == '__main__':
    print("開始執行反思整合測試...")
    print("=" * 60)

    # 設定測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 載入測試類別
    test_classes = [
        TestReflectionEnhancement,
        TestReflectionIntegrationFlow
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 報告結果
    print("\n" + "=" * 60)
    print("反思整合測試完成")
    print(f"測試數量: {result.testsRun}")
    print(f"失敗: {len(result.failures)}")
    print(f"錯誤: {len(result.errors)}")

    if result.failures:
        print("\n失敗測試:")
        for test, trace in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\n錯誤測試:")
        for test, trace in result.errors:
            print(f"  - {test}")

    sys.exit(0 if result.wasSuccessful() else 1)