#!/usr/bin/env python3
"""
Performance Constraints Testing
測試Task 4的效能約束實施
"""

import os
import sys
import time
import threading
import multiprocessing
import unittest
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class TestTimeoutConstraints(unittest.TestCase):
    """超時約束測試"""

    def test_30_second_timeout_enforcement(self):
        """測試30秒超時執行"""

        def mock_security_check(duration):
            """模擬耗時安全檢查"""
            time.sleep(duration)
            return f"completed after {duration}s"

        def enforce_timeout(func, args, timeout=30):
            """超時執行器"""
            import signal

            class TimeoutException(Exception):
                pass

            def timeout_handler(signum, frame):
                raise TimeoutException("Operation timed out")

            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

            try:
                result = func(*args)
                signal.alarm(0)  # Cancel alarm
                return result
            except TimeoutException:
                return "TIMEOUT"
            finally:
                signal.signal(signal.SIGALRM, old_handler)

        # 測試正常執行（快速完成）
        result = enforce_timeout(mock_security_check, (1,), timeout=5)
        self.assertEqual(result, "completed after 1s", "快速執行失敗")

        # 測試超時控制（模擬長時間檢查）- 使用shorter timeout for testing
        if os.name != 'nt':  # Unix systems only
            result = enforce_timeout(mock_security_check, (3,), timeout=1)
            self.assertEqual(result, "TIMEOUT", "超時控制失敗")

    def test_timeout_with_threading(self):
        """測試執行緒方式的超時控制"""

        def long_running_task():
            """長時間執行的任務"""
            time.sleep(5)
            return "task completed"

        def run_with_timeout(func, timeout_seconds):
            """使用執行緒實現超時控制"""
            result = [None]
            exception = [None]

            def target():
                try:
                    result[0] = func()
                except Exception as e:
                    exception[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout=timeout_seconds)

            if thread.is_alive():
                return "TIMEOUT"
            elif exception[0]:
                raise exception[0]
            else:
                return result[0]

        # 測試超時
        start_time = time.time()
        result = run_with_timeout(long_running_task, 2)
        duration = time.time() - start_time

        self.assertEqual(result, "TIMEOUT", "超時控制失敗")
        self.assertLess(duration, 3, "超時時間控制不準確")

    def test_async_timeout_control(self):
        """測試異步超時控制"""

        async def async_security_check(delay):
            """異步安全檢查"""
            await asyncio.sleep(delay)
            return f"async completed after {delay}s"

        async def run_async_tests():
            """執行異步測試"""
            # 測試正常完成
            try:
                result = await asyncio.wait_for(async_security_check(1), timeout=3)
                self.assertEqual(result, "async completed after 1s")
            except asyncio.TimeoutError:
                self.fail("正常執行不應該超時")

            # 測試超時控制
            with self.assertRaises(asyncio.TimeoutError):
                await asyncio.wait_for(async_security_check(3), timeout=1)

        # 執行異步測試
        asyncio.run(run_async_tests())


class TestParallelExecution(unittest.TestCase):
    """並行執行測試"""

    def test_threadpool_parallel_execution(self):
        """測試執行緒池並行執行"""

        def security_check(check_id, duration=1):
            """模擬安全檢查"""
            time.sleep(duration)
            return f"check_{check_id}_completed"

        def parallel_security_checks(check_count=4, max_workers=4, timeout=30):
            """並行執行安全檢查"""
            start_time = time.time()
            results = []

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 提交所有任務
                futures = []
                for i in range(check_count):
                    future = executor.submit(security_check, i, 1)
                    futures.append(future)

                # 收集結果
                for future in futures:
                    try:
                        result = future.result(timeout=timeout // check_count)
                        results.append(result)
                    except TimeoutError:
                        results.append("TIMEOUT")

            execution_time = time.time() - start_time
            return results, execution_time

        # 測試4個並行檢查
        results, duration = parallel_security_checks(4, 4, 30)

        self.assertEqual(len(results), 4, "結果數量不正確")
        self.assertTrue(all("completed" in r for r in results), "並行執行失敗")
        self.assertLess(duration, 3, "並行執行時間過長")  # 4個1秒任務並行應該約1秒完成

    def test_concurrent_futures_execution(self):
        """測試concurrent.futures並行執行"""
        from concurrent.futures import as_completed

        def mock_layer_check(layer_id):
            """模擬安全層檢查"""
            time.sleep(0.5)  # 每層0.5秒
            return f"layer_{layer_id}_secure"

        def run_parallel_layer_checks():
            """並行執行多層安全檢查"""
            start_time = time.time()
            results = {}

            with ThreadPoolExecutor(max_workers=8) as executor:
                # 模擬8層安全檢查
                future_to_layer = {
                    executor.submit(mock_layer_check, layer): layer
                    for layer in range(1, 9)
                }

                # 收集結果
                for future in as_completed(future_to_layer, timeout=30):
                    layer = future_to_layer[future]
                    try:
                        result = future.result()
                        results[layer] = result
                    except Exception as exc:
                        results[layer] = f"ERROR: {exc}"

            execution_time = time.time() - start_time
            return results, execution_time

        results, duration = run_parallel_layer_checks()

        # 驗證所有8層都完成
        self.assertEqual(len(results), 8, "安全層檢查數量不完整")

        # 驗證並行效能：8個0.5秒任務並行應該約0.5秒完成
        self.assertLess(duration, 2, "8層並行檢查時間過長")

        # 驗證所有層都成功
        for layer_id, result in results.items():
            self.assertIn("secure", result, f"安全層 {layer_id} 檢查失敗")

    def test_performance_comparison(self):
        """測試順序執行vs並行執行效能比較"""

        def security_task(task_id):
            """安全檢查任務"""
            time.sleep(0.3)  # 每個任務0.3秒
            return f"task_{task_id}_done"

        # 順序執行
        start_time = time.time()
        sequential_results = []
        for i in range(5):
            result = security_task(i)
            sequential_results.append(result)
        sequential_time = time.time() - start_time

        # 並行執行
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            parallel_results = list(executor.map(security_task, range(5)))
        parallel_time = time.time() - start_time

        # 驗證結果一致性
        self.assertEqual(len(sequential_results), len(parallel_results))

        # 驗證效能提升
        speedup = sequential_time / parallel_time
        self.assertGreater(speedup, 2, f"並行效能提升不足: {speedup:.2f}x")

        print(f"順序執行: {sequential_time:.2f}s")
        print(f"並行執行: {parallel_time:.2f}s")
        print(f"效能提升: {speedup:.2f}x")


class TestGracefulDegradation(unittest.TestCase):
    """優雅降級測試"""

    def test_partial_failure_handling(self):
        """測試部分失敗處理"""

        def unreliable_check(check_id):
            """不可靠的安全檢查"""
            if check_id % 3 == 0:  # 每3個失敗一個
                raise Exception(f"Check {check_id} failed")
            time.sleep(0.1)
            return f"check_{check_id}_passed"

        def robust_security_scan(check_count=9):
            """健壯的安全掃描"""
            results = {}
            failed_checks = []

            with ThreadPoolExecutor(max_workers=4) as executor:
                future_to_check = {
                    executor.submit(unreliable_check, i): i
                    for i in range(check_count)
                }

                for future in as_completed(future_to_check, timeout=10):
                    check_id = future_to_check[future]
                    try:
                        result = future.result()
                        results[check_id] = result
                    except Exception as exc:
                        failed_checks.append(check_id)
                        results[check_id] = f"FAILED: {exc}"

            return results, failed_checks

        results, failed_checks = robust_security_scan(9)

        # 驗證部分成功
        self.assertEqual(len(results), 9, "結果數量不完整")
        self.assertEqual(len(failed_checks), 3, "失敗檢查數量不正確")

        # 驗證成功的檢查
        successful_checks = [k for k in results.keys() if k not in failed_checks]
        self.assertEqual(len(successful_checks), 6, "成功檢查數量不正確")

        # 驗證失敗的檢查有適當標記
        for failed_id in failed_checks:
            self.assertIn("FAILED", results[failed_id], f"失敗檢查 {failed_id} 未標記")

    def test_timeout_fallback(self):
        """測試超時回退機制"""

        def slow_security_check(check_id):
            """慢速安全檢查"""
            if check_id == 2:  # 檢查2故意很慢
                time.sleep(5)
            else:
                time.sleep(0.5)
            return f"check_{check_id}_completed"

        def timeout_aware_scan():
            """超時感知掃描"""
            results = {}
            timeout_checks = []

            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_check = {
                    executor.submit(slow_security_check, i): i
                    for i in range(3)
                }

                for future in as_completed(future_to_check, timeout=3):
                    check_id = future_to_check[future]
                    try:
                        result = future.result(timeout=2)  # 每個檢查最多2秒
                        results[check_id] = result
                    except TimeoutError:
                        timeout_checks.append(check_id)
                        results[check_id] = "TIMEOUT_FALLBACK"

            return results, timeout_checks

        results, timeout_checks = timeout_aware_scan()

        # 驗證超時回退
        self.assertIn(2, timeout_checks, "慢速檢查未超時")
        self.assertEqual(results[2], "TIMEOUT_FALLBACK", "超時回退機制失效")

        # 驗證正常檢查完成
        for check_id in [0, 1]:
            if check_id not in timeout_checks:
                self.assertIn("completed", results[check_id], f"檢查 {check_id} 未正常完成")

    def test_resource_constraint_handling(self):
        """測試資源約束處理"""

        def memory_intensive_check(size_mb):
            """記憶體密集型檢查"""
            # 分配指定大小的記憶體
            data = bytearray(size_mb * 1024 * 1024)
            time.sleep(0.1)
            del data
            return f"processed_{size_mb}MB"

        def resource_aware_execution():
            """資源感知執行"""
            import psutil

            # 獲取可用記憶體
            available_memory = psutil.virtual_memory().available / (1024 * 1024)  # MB

            # 根據可用記憶體調整檢查大小
            if available_memory > 1000:  # 超過1GB
                check_sizes = [100, 200, 300]  # 大型檢查
                max_workers = 3
            else:  # 記憶體較少
                check_sizes = [10, 20, 30]  # 小型檢查
                max_workers = 2

            results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(memory_intensive_check, size) for size in check_sizes]

                for future in futures:
                    try:
                        result = future.result(timeout=10)
                        results.append(result)
                    except Exception as exc:
                        results.append(f"ERROR: {exc}")

            return results, available_memory

        results, available_memory = resource_aware_execution()

        # 驗證執行完成
        self.assertEqual(len(results), 3, "資源感知執行不完整")

        # 驗證沒有記憶體錯誤
        error_results = [r for r in results if "ERROR" in r]
        self.assertEqual(len(error_results), 0, f"資源約束處理失敗: {error_results}")

        print(f"可用記憶體: {available_memory:.0f}MB")
        print(f"執行結果: {results}")


class TestPerformanceOptimization(unittest.TestCase):
    """效能最佳化測試"""

    def test_caching_mechanism(self):
        """測試快取機制"""
        cache = {}
        call_count = {}

        def expensive_security_check(file_path):
            """昂貴的安全檢查"""
            # 計算調用次數
            call_count[file_path] = call_count.get(file_path, 0) + 1

            # 檢查快取
            if file_path in cache:
                return cache[file_path]

            # 模擬昂貴操作
            time.sleep(0.5)
            result = f"security_scan_result_for_{file_path}"

            # 快取結果
            cache[file_path] = result
            return result

        # 第一次調用
        start_time = time.time()
        result1 = expensive_security_check("file1.py")
        first_call_time = time.time() - start_time

        # 第二次調用同一檔案（應該從快取返回）
        start_time = time.time()
        result2 = expensive_security_check("file1.py")
        cached_call_time = time.time() - start_time

        # 驗證結果一致性
        self.assertEqual(result1, result2, "快取結果不一致")

        # 驗證效能提升
        self.assertGreater(first_call_time, 0.4, "第一次調用時間過短")
        self.assertLess(cached_call_time, 0.1, "快取調用時間過長")

        # 驗證調用次數
        self.assertEqual(call_count["file1.py"], 1, "快取機制未生效，重複計算")

    def test_incremental_scanning(self):
        """測試漸進式掃描"""
        scanned_files = set()

        def incremental_security_scan(files, changed_files):
            """漸進式安全掃描"""
            scan_count = 0
            results = {}

            for file_path in files:
                if file_path in changed_files or file_path not in scanned_files:
                    # 只掃描變更或未掃描的檔案
                    time.sleep(0.1)  # 模擬掃描時間
                    results[file_path] = f"scanned_{file_path}"
                    scanned_files.add(file_path)
                    scan_count += 1
                else:
                    # 使用快取結果
                    results[file_path] = f"cached_{file_path}"

            return results, scan_count

        # 初始掃描
        all_files = ["file1.py", "file2.py", "file3.py", "file4.py"]
        results1, scan_count1 = incremental_security_scan(all_files, all_files)

        self.assertEqual(scan_count1, 4, "初始掃描計數錯誤")

        # 部分檔案變更後的掃描
        changed_files = ["file2.py", "file5.py"]
        new_files = all_files + ["file5.py"]
        results2, scan_count2 = incremental_security_scan(new_files, changed_files)

        self.assertEqual(scan_count2, 2, "漸進式掃描計數錯誤")  # 只掃描file2和file5

        # 驗證未變更檔案使用快取
        self.assertIn("cached_file1.py", results2["file1.py"])
        self.assertIn("cached_file3.py", results2["file3.py"])

        # 驗證變更檔案重新掃描
        self.assertIn("scanned_file2.py", results2["file2.py"])
        self.assertIn("scanned_file5.py", results2["file5.py"])


if __name__ == '__main__':
    print("開始執行效能約束測試...")
    print("=" * 60)

    # 設定測試套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 載入測試類別
    test_classes = [
        TestTimeoutConstraints,
        TestParallelExecution,
        TestGracefulDegradation,
        TestPerformanceOptimization
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 效能統計
    print("\n" + "=" * 60)
    print("效能約束測試完成")
    print(f"總測試數: {result.testsRun}")
    print(f"失敗數: {len(result.failures)}")
    print(f"錯誤數: {len(result.errors)}")

    if result.failures:
        print("\n失敗測試:")
        for test, trace in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\n錯誤測試:")
        for test, trace in result.errors:
            print(f"  - {test}")

    sys.exit(0 if result.wasSuccessful() else 1)