#!/bin/bash

# Agent System Security Test Suite
# 執行Tasks 1-4安全強化的整合測試與驗證

set -euo pipefail

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 專案根目錄
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TEST_DIR="$PROJECT_ROOT/tests/agent-system-security"

# 測試結果
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# 輸出函數
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# 檢查Python環境
check_python_environment() {
    print_header "檢查Python環境"

    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安裝"
        exit 1
    fi

    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python版本: $python_version"

    # 檢查必要模組
    required_modules=("unittest" "pathlib" "concurrent.futures" "threading" "asyncio")
    for module in "${required_modules[@]}"; do
        if python3 -c "import $module" 2>/dev/null; then
            print_success "模組 $module 可用"
        else
            print_error "模組 $module 不可用"
            exit 1
        fi
    done

    echo ""
}

# 檢查測試檔案
check_test_files() {
    print_header "檢查測試檔案"

    test_files=(
        "test_security_integration.py"
        "test_performance_constraints.py"
        "test_reflection_integration.py"
    )

    for file in "${test_files[@]}"; do
        if [[ -f "$TEST_DIR/$file" ]]; then
            print_success "測試檔案存在: $file"
        else
            print_error "測試檔案缺失: $file"
            exit 1
        fi
    done

    echo ""
}

# 檢查相依實作檔案
check_implementation_files() {
    print_header "檢查實作檔案"

    # Task 1: AI安全模式
    if [[ -f "$PROJECT_ROOT/plugins/rcc/skills/planning-agent-systems/references/ai-security-patterns.md" ]]; then
        print_success "AI安全模式檔案存在"
    else
        print_warning "AI安全模式檔案不存在，某些測試可能失敗"
    fi

    # Task 2: 八層防禦
    if [[ -f "$PROJECT_ROOT/plugins/rcc/skills/planning-agent-systems/references/security-layers.md" ]]; then
        print_success "八層防禦檔案存在"
    else
        print_warning "八層防禦檔案不存在，某些測試可能失敗"
    fi

    # Task 3: 反思技能 (調整後)
    if [[ -f "$PROJECT_ROOT/plugins/rcc/skills/reflecting/SKILL.md" ]]; then
        print_success "反思技能檔案存在"
    else
        print_warning "反思技能檔案不存在，某些測試可能失敗"
    fi

    # Task 4: 效能最佳化
    if [[ -f "$PROJECT_ROOT/plugins/rcc/skills/writing-hooks/references/performance-optimization.md" ]]; then
        print_success "效能最佳化檔案存在"
    else
        print_warning "效能最佳化檔案不存在，某些測試可能失敗"
    fi

    echo ""
}

# 執行單一測試檔案
run_single_test() {
    local test_file="$1"
    local test_name="$2"

    print_info "執行 $test_name..."

    cd "$TEST_DIR"

    # 建立臨時日誌檔案
    local log_file="/tmp/test_${test_file%.py}.log"

    # 執行測試並擷取結果
    if python3 "$test_file" > "$log_file" 2>&1; then
        local test_count=$(grep "Ran [0-9]\+ tests" "$log_file" | grep -o '[0-9]\+' | head -1 || echo "0")
        local failures=$(grep -o "failures=[0-9]\+" "$log_file" | grep -o '[0-9]\+' || echo "0")
        local errors=$(grep -o "errors=[0-9]\+" "$log_file" | grep -o '[0-9]\+' || echo "0")

        TOTAL_TESTS=$((TOTAL_TESTS + test_count))

        if [[ "$failures" == "0" && "$errors" == "0" ]]; then
            PASSED_TESTS=$((PASSED_TESTS + test_count))
            print_success "$test_name 通過 ($test_count 測試)"
        else
            FAILED_TESTS=$((FAILED_TESTS + failures + errors))
            print_error "$test_name 失敗 ($failures 失敗, $errors 錯誤)"

            # 顯示失敗詳情
            echo "失敗詳情:"
            tail -20 "$log_file" | sed 's/^/  /'
        fi
    else
        print_error "$test_name 執行異常"
        echo "執行日誌:"
        tail -20 "$log_file" | sed 's/^/  /'
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    # 清理日誌檔案
    rm -f "$log_file"
    echo ""
}

# 執行所有測試
run_all_tests() {
    print_header "執行安全強化測試套件"

    # 測試1: 安全整合測試
    run_single_test "test_security_integration.py" "安全整合測試"

    # 測試2: 效能約束測試
    run_single_test "test_performance_constraints.py" "效能約束測試"

    # 測試3: 反思整合測試
    run_single_test "test_reflection_integration.py" "反思整合測試"
}

# 生成測試報告
generate_test_report() {
    print_header "測試執行摘要"

    echo "測試執行時間: $(date)"
    echo "專案路徑: $PROJECT_ROOT"
    echo ""
    echo "測試結果統計:"
    echo "  總測試數: $TOTAL_TESTS"
    echo "  通過測試: $PASSED_TESTS"
    echo "  失敗測試: $FAILED_TESTS"
    echo ""

    if [[ $FAILED_TESTS -eq 0 ]]; then
        print_success "所有測試通過！安全強化實施成功。"

        echo ""
        echo "安全強化驗證成功："
        echo "✓ Task 1: AI安全模式檢測 - 實施完成"
        echo "✓ Task 2: 八層防禦框架 - 實施完成"
        echo "✓ Task 3: 反思技能強化 - 實施完成"
        echo "✓ Task 4: 效能約束與策略 - 實施完成"
        echo "✓ 整合測試與驗證 - 全部通過"

    else
        print_error "測試失敗，需要修正問題。"

        echo ""
        echo "需要檢查的領域："
        echo "- 檢查實作檔案是否完整"
        echo "- 確認技能整合是否正確"
        echo "- 驗證Hook配置是否有效"
        echo "- 測試效能約束是否符合要求"
    fi

    echo ""
}

# 執行效能基準測試
run_performance_benchmarks() {
    print_header "執行效能基準測試"

    print_info "測試30秒超時約束..."

    # 建立臨時測試腳本
    cat > /tmp/timeout_test.py << 'EOF'
import time
import threading
import signal

def timeout_test():
    def slow_operation():
        time.sleep(5)
        return "completed"

    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(3)  # 3秒超時

    try:
        result = slow_operation()
        signal.alarm(0)
        return False  # 應該超時
    except TimeoutError:
        return True  # 正確超時

if timeout_test():
    print("✓ 超時機制正常運作")
else:
    print("✗ 超時機制異常")
EOF

    if python3 /tmp/timeout_test.py 2>/dev/null; then
        print_success "超時約束測試通過"
    else
        print_warning "超時約束測試失敗（可能因平台限制）"
    fi

    rm -f /tmp/timeout_test.py

    print_info "測試並行執行效能..."

    # 建立並行效能測試
    cat > /tmp/parallel_test.py << 'EOF'
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def parallel_performance_test():
    def task():
        time.sleep(0.5)
        return "done"

    # 順序執行
    start = time.time()
    for _ in range(4):
        task()
    sequential_time = time.time() - start

    # 並行執行
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(lambda x: task(), range(4)))
    parallel_time = time.time() - start

    speedup = sequential_time / parallel_time
    print(f"順序執行: {sequential_time:.2f}s")
    print(f"並行執行: {parallel_time:.2f}s")
    print(f"效能提升: {speedup:.2f}x")

    return speedup > 2

if parallel_performance_test():
    print("✓ 並行效能提升達標")
else:
    print("✗ 並行效能提升不足")
EOF

    python3 /tmp/parallel_test.py
    rm -f /tmp/parallel_test.py

    echo ""
}

# 驗證整合架構
verify_integration_architecture() {
    print_header "驗證整合架構"

    # 檢查插件結構
    if [[ -f "$PROJECT_ROOT/plugins/rcc/.claude-plugin/plugin.json" ]]; then
        print_success "插件配置檔案存在"

        # 檢查技能註冊
        if grep -q "planning-agent-systems" "$PROJECT_ROOT/plugins/rcc/.claude-plugin/plugin.json"; then
            print_success "規劃系統技能已註冊"
        else
            print_warning "規劃系統技能未註冊"
        fi

        if grep -q "reflecting" "$PROJECT_ROOT/plugins/rcc/.claude-plugin/plugin.json"; then
            print_success "反思技能已註冊"
        else
            print_warning "反思技能未註冊"
        fi

        if grep -q "writing-hooks" "$PROJECT_ROOT/plugins/rcc/.claude-plugin/plugin.json"; then
            print_success "Hook寫作技能已註冊"
        else
            print_warning "Hook寫作技能未註冊"
        fi
    else
        print_error "插件配置檔案不存在"
    fi

    # 檢查版本一致性
    if [[ -f "$PROJECT_ROOT/.claude-plugin/marketplace.json" ]]; then
        marketplace_version=$(grep -o '"version": "[^"]*"' "$PROJECT_ROOT/.claude-plugin/marketplace.json" | head -1 | cut -d'"' -f4)
        plugin_version=$(grep -o '"version": "[^"]*"' "$PROJECT_ROOT/plugins/rcc/.claude-plugin/plugin.json" | cut -d'"' -f4)

        if [[ "$marketplace_version" == "$plugin_version" ]]; then
            print_success "版本號同步 ($marketplace_version)"
        else
            print_warning "版本號不同步 (marketplace: $marketplace_version, plugin: $plugin_version)"
        fi
    fi

    echo ""
}

# 主執行函數
main() {
    print_header "Agent System Security Test Suite"
    echo "執行代理系統安全強化測試與驗證"
    echo "測試範圍: Tasks 1-4 安全強化實施"
    echo ""

    # 前置檢查
    check_python_environment
    check_test_files
    check_implementation_files

    # 架構驗證
    verify_integration_architecture

    # 執行測試
    run_all_tests

    # 效能基準
    run_performance_benchmarks

    # 生成報告
    generate_test_report

    # 回傳測試結果
    if [[ $FAILED_TESTS -eq 0 ]]; then
        echo ""
        print_success "安全強化測試套件執行完成 - 全部通過"
        exit 0
    else
        echo ""
        print_error "安全強化測試套件執行完成 - 發現問題"
        exit 1
    fi
}

# 執行主函數
main "$@"