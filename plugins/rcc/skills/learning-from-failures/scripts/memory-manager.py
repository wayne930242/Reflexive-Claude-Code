#!/usr/bin/env python3
"""
Memory Manager for Learning from Failures System

Manages institutional memory storage, pattern extraction, and warning generation
for agent system failures and learning outcomes.
"""

import json
import os
import sys
import argparse
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import re


@dataclass
class FailureRecord:
    """記錄失敗案例的資料結構"""
    id: str
    type: str
    component: str
    description: str
    context: Dict[str, Any]
    timestamp: str
    severity: str = "medium"
    resolved: bool = False


@dataclass
class Pattern:
    """學習模式的資料結構"""
    id: str
    name: str
    category: str
    context_criteria: Dict[str, Any]
    problem_description: str
    detection_methods: List[str]
    prevention_steps: List[str]
    examples: List[str]
    severity: str
    created: str
    last_triggered: str
    trigger_count: int = 0


@dataclass
class Warning:
    """警告訊息的資料結構"""
    pattern_id: str
    message: str
    priority: int
    context_match_score: float
    recommended_actions: List[str]


class MemoryManager:
    """管理學習記憶的主要類別"""

    def __init__(self, base_path: Optional[str] = None):
        if base_path is None:
            # 預設使用專案根目錄下的 docs/agent-system/memory
            script_dir = Path(__file__).parent.absolute()
            project_root = script_dir.parent.parent.parent.parent
            base_path = project_root / "docs" / "agent-system" / "memory"

        self.base_path = Path(base_path)
        self.patterns_dir = self.base_path / "patterns"
        self.failures_dir = self.base_path / "failures"
        self.preventions_dir = self.base_path / "preventions"

        # 確保目錄存在
        self._ensure_directories()

    def _ensure_directories(self):
        """確保所有必要目錄存在"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.patterns_dir.mkdir(exist_ok=True)
        self.failures_dir.mkdir(exist_ok=True)
        self.preventions_dir.mkdir(exist_ok=True)

    def _generate_id(self, content: str) -> str:
        """產生唯一 ID"""
        return hashlib.md5(content.encode()).hexdigest()[:8]

    def _current_timestamp(self) -> str:
        """取得當前時間戳"""
        return datetime.now().isoformat()

    def record_failure(self, failure_type: str, component: str, description: str,
                      context: Optional[Dict[str, Any]] = None,
                      severity: str = "medium") -> str:
        """記錄失敗案例"""
        if context is None:
            context = {}

        failure_id = self._generate_id(f"{failure_type}-{component}-{description}")
        timestamp = self._current_timestamp()

        failure = FailureRecord(
            id=failure_id,
            type=failure_type,
            component=component,
            description=description,
            context=context,
            timestamp=timestamp,
            severity=severity
        )

        # 儲存到 JSON 檔案
        failure_file = self.failures_dir / f"{failure_id}.json"
        with open(failure_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(failure), f, indent=2, ensure_ascii=False)

        print(f"✅ 失敗案例已記錄: {failure_id}")
        print(f"   類型: {failure_type}")
        print(f"   元件: {component}")
        print(f"   描述: {description}")

        return failure_id

    def extract_pattern(self, failure_id: Optional[str] = None,
                       pattern_name: Optional[str] = None,
                       category: str = "code",
                       context_criteria: Optional[Dict[str, Any]] = None) -> str:
        """從失敗案例提取模式"""
        if context_criteria is None:
            context_criteria = {}

        # 如果提供失敗 ID，從失敗記錄載入資訊
        if failure_id:
            failure_file = self.failures_dir / f"{failure_id}.json"
            if failure_file.exists():
                with open(failure_file, 'r', encoding='utf-8') as f:
                    failure_data = json.load(f)

                if not pattern_name:
                    pattern_name = f"{failure_data['type']} Pattern"

                context_criteria.update(failure_data.get('context', {}))

        if not pattern_name:
            pattern_name = "Unnamed Pattern"

        pattern_id = self._generate_id(pattern_name)
        timestamp = self._current_timestamp()

        pattern = Pattern(
            id=pattern_id,
            name=pattern_name,
            category=category,
            context_criteria=context_criteria,
            problem_description="需要填入具體問題描述",
            detection_methods=["需要填入檢測方法"],
            prevention_steps=["需要填入預防步驟"],
            examples=[failure_id] if failure_id else [],
            severity="medium",
            created=timestamp,
            last_triggered=timestamp
        )

        # 儲存模式
        pattern_file = self.patterns_dir / f"{pattern_id}.json"
        with open(pattern_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(pattern), f, indent=2, ensure_ascii=False)

        # 產生 Markdown 檔案
        self._generate_pattern_markdown(pattern)

        print(f"✅ 模式已提取: {pattern_id}")
        print(f"   名稱: {pattern_name}")
        print(f"   類別: {category}")

        return pattern_id

    def _generate_pattern_markdown(self, pattern: Pattern):
        """產生模式的 Markdown 文件"""
        md_content = f"""---
id: {pattern.id}
category: {pattern.category}
severity: {pattern.severity}
created: {pattern.created}
last_triggered: {pattern.last_triggered}
trigger_count: {pattern.trigger_count}
---

# Pattern: {pattern.name}

## Context
{self._format_context_criteria(pattern.context_criteria)}

## Problem
{pattern.problem_description}

## Detection
{self._format_list_items(pattern.detection_methods)}

## Prevention
{self._format_list_items(pattern.prevention_steps)}

## Examples
{self._format_examples(pattern.examples)}

## Related Patterns
- [待補充相關模式連結]

## Mitigation
如果發生此模式:
1. 立即回應步驟
2. 損害評估
3. 恢復程序
"""

        md_file = self.patterns_dir / f"{pattern.id}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)

    def _format_context_criteria(self, criteria: Dict[str, Any]) -> str:
        """格式化情境條件"""
        if not criteria:
            return "待定義具體情境條件"

        lines = []
        for key, value in criteria.items():
            lines.append(f"- **{key}:** {value}")

        return '\n'.join(lines)

    def _format_list_items(self, items: List[str]) -> str:
        """格式化清單項目"""
        return '\n'.join(f"- {item}" for item in items)

    def _format_examples(self, examples: List[str]) -> str:
        """格式化範例清單"""
        if not examples:
            return "- 目前無相關範例"

        lines = []
        for example in examples:
            # 嘗試載入失敗記錄以取得詳細資訊
            failure_file = self.failures_dir / f"{example}.json"
            if failure_file.exists():
                with open(failure_file, 'r', encoding='utf-8') as f:
                    failure_data = json.load(f)
                lines.append(f"- **{example}:** {failure_data['description']}")
            else:
                lines.append(f"- {example}")

        return '\n'.join(lines)

    def get_relevant_patterns(self, context: Dict[str, Any],
                             threshold: float = 0.4) -> List[Pattern]:
        """取得相關的模式"""
        relevant_patterns = []

        # 載入所有模式
        for pattern_file in self.patterns_dir.glob("*.json"):
            try:
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    pattern_data = json.load(f)

                pattern = Pattern(**pattern_data)
                match_score = self._calculate_context_match(context, pattern.context_criteria)

                if match_score >= threshold:
                    relevant_patterns.append(pattern)

            except Exception as e:
                print(f"⚠️  載入模式失敗 {pattern_file}: {e}", file=sys.stderr)

        # 依匹配度排序
        relevant_patterns.sort(
            key=lambda p: self._calculate_context_match(context, p.context_criteria),
            reverse=True
        )

        return relevant_patterns

    def _calculate_context_match(self, context1: Dict[str, Any],
                                context2: Dict[str, Any]) -> float:
        """計算情境匹配度"""
        if not context1 or not context2:
            return 0.0

        common_keys = set(context1.keys()) & set(context2.keys())
        if not common_keys:
            return 0.0

        matches = 0
        for key in common_keys:
            if context1[key] == context2[key]:
                matches += 1
            elif self._is_similar_value(context1[key], context2[key]):
                matches += 0.5

        return matches / len(common_keys)

    def _is_similar_value(self, value1: Any, value2: Any) -> bool:
        """判斷兩個值是否相似"""
        if isinstance(value1, str) and isinstance(value2, str):
            # 簡單的字串相似性檢查
            value1_lower = value1.lower()
            value2_lower = value2.lower()

            # 檢查是否包含相同的關鍵字
            words1 = set(re.findall(r'\w+', value1_lower))
            words2 = set(re.findall(r'\w+', value2_lower))

            if words1 & words2:  # 有共同詞彙
                return True

        return False

    def generate_warnings(self, context: Dict[str, Any]) -> List[Warning]:
        """產生相關警告"""
        relevant_patterns = self.get_relevant_patterns(context)
        warnings = []

        for pattern in relevant_patterns:
            match_score = self._calculate_context_match(context, pattern.context_criteria)

            # 產生警告訊息
            if match_score >= 0.7:
                priority = 3  # 高優先級
                message_prefix = "🔴 高風險警告"
            elif match_score >= 0.4:
                priority = 2  # 中優先級
                message_prefix = "🟡 中度風險警告"
            else:
                continue  # 跳過低匹配度

            message = f"""{message_prefix}: {pattern.name}

**情境匹配度:** {match_score:.1%}
**問題:** {pattern.problem_description}
**建議檢查:** {', '.join(pattern.detection_methods[:2])}
**預防措施:** {', '.join(pattern.prevention_steps[:2])}

**歷史觸發次數:** {pattern.trigger_count}
"""

            warning = Warning(
                pattern_id=pattern.id,
                message=message,
                priority=priority,
                context_match_score=match_score,
                recommended_actions=pattern.prevention_steps
            )

            warnings.append(warning)

        # 依優先級排序
        warnings.sort(key=lambda w: w.priority, reverse=True)

        return warnings

    def list_failures(self) -> List[FailureRecord]:
        """列出所有失敗記錄"""
        failures = []

        for failure_file in self.failures_dir.glob("*.json"):
            try:
                with open(failure_file, 'r', encoding='utf-8') as f:
                    failure_data = json.load(f)
                failures.append(FailureRecord(**failure_data))
            except Exception as e:
                print(f"⚠️  載入失敗記錄失敗 {failure_file}: {e}", file=sys.stderr)

        return failures

    def list_patterns(self) -> List[Pattern]:
        """列出所有模式"""
        patterns = []

        for pattern_file in self.patterns_dir.glob("*.json"):
            try:
                with open(pattern_file, 'r', encoding='utf-8') as f:
                    pattern_data = json.load(f)
                patterns.append(Pattern(**pattern_data))
            except Exception as e:
                print(f"⚠️  載入模式失敗 {pattern_file}: {e}", file=sys.stderr)

        return patterns


def main():
    """命令列介面"""
    parser = argparse.ArgumentParser(
        description="Memory Manager for Learning from Failures",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--base-path',
        type=str,
        help="Base path for memory storage (default: docs/agent-system/memory)"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # record-failure 指令
    record_parser = subparsers.add_parser('record-failure', help='Record a failure case')
    record_parser.add_argument('--type', required=True, help='Failure type')
    record_parser.add_argument('--component', required=True, help='Affected component')
    record_parser.add_argument('--description', required=True, help='Failure description')
    record_parser.add_argument('--context', help='Context as JSON string')
    record_parser.add_argument('--severity', default='medium',
                              choices=['critical', 'high', 'medium', 'low'],
                              help='Failure severity')

    # extract-pattern 指令
    extract_parser = subparsers.add_parser('extract-pattern', help='Extract pattern from failure')
    extract_parser.add_argument('--failure-id', help='Failure ID to extract from')
    extract_parser.add_argument('--name', help='Pattern name')
    extract_parser.add_argument('--category', default='code',
                               choices=['code', 'workflow', 'security'],
                               help='Pattern category')
    extract_parser.add_argument('--context', help='Context criteria as JSON string')

    # get-warnings 指令 (從 stdin 讀取 JSON)
    warnings_parser = subparsers.add_parser('get-warnings', help='Get warnings for context')
    warnings_parser.add_argument('--format', choices=['text', 'json'], default='text',
                                help='Output format')

    # list 指令
    list_parser = subparsers.add_parser('list', help='List stored data')
    list_parser.add_argument('type', choices=['failures', 'patterns'], help='Type to list')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        manager = MemoryManager(args.base_path)

        if args.command == 'record-failure':
            context = {}
            if args.context:
                context = json.loads(args.context)

            failure_id = manager.record_failure(
                failure_type=args.type,
                component=args.component,
                description=args.description,
                context=context,
                severity=args.severity
            )

        elif args.command == 'extract-pattern':
            context_criteria = {}
            if args.context:
                context_criteria = json.loads(args.context)

            pattern_id = manager.extract_pattern(
                failure_id=args.failure_id,
                pattern_name=args.name,
                category=args.category,
                context_criteria=context_criteria
            )

        elif args.command == 'get-warnings':
            # 從 stdin 讀取 JSON 情境
            try:
                context_input = sys.stdin.read().strip()
                if not context_input:
                    print("❌ 請提供 JSON 情境資料", file=sys.stderr)
                    sys.exit(1)

                context = json.loads(context_input)
                warnings = manager.generate_warnings(context)

                if args.format == 'json':
                    warnings_data = [asdict(w) for w in warnings]
                    print(json.dumps(warnings_data, indent=2, ensure_ascii=False))
                else:
                    if warnings:
                        for warning in warnings:
                            print(warning.message)
                            print("─" * 50)
                    else:
                        print("✅ 未發現相關風險警告")

            except json.JSONDecodeError as e:
                print(f"❌ JSON 格式錯誤: {e}", file=sys.stderr)
                sys.exit(1)

        elif args.command == 'list':
            if args.type == 'failures':
                failures = manager.list_failures()
                print(f"📋 共 {len(failures)} 筆失敗記錄:")
                for failure in failures:
                    print(f"  {failure.id}: {failure.type} - {failure.description[:50]}...")

            elif args.type == 'patterns':
                patterns = manager.list_patterns()
                print(f"📋 共 {len(patterns)} 個學習模式:")
                for pattern in patterns:
                    print(f"  {pattern.id}: {pattern.name} ({pattern.category})")

    except Exception as e:
        print(f"❌ 執行錯誤: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()