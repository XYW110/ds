#!/usr/bin/env python3
"""
简化版日投入限额功能测试
"""

import os
import sys
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, 'src')

def test_basic_functionality():
    """测试基本功能"""
    print("[TEST] Testing basic daily limit functionality...")

    try:
        # Test 1: 配置加载
        from src.config.config_manager import get_config
        config = get_config()
        daily_limit_config = config.daily_limit

        print(f"[OK] Config loaded successfully")
        print(f"  Daily limit: {daily_limit_config.daily_limit_usdt} USDT")
        print(f"  Reset time: {daily_limit_config.reset_hour}:00")
        print(f"  Timezone: {daily_limit_config.reset_timezone}")

        # Test 2: 数据库初始化
        from src.utils.daily_limit_manager import DailyLimitManager
        manager = DailyLimitManager(daily_limit_config)

        print(f"[OK] Database initialized successfully")

        # Test 3: 基本操作
        stats = manager.get_daily_stats()
        print(f"[OK] Got daily stats: {stats.get('total_usdt_invested', 0):.2f} USDT invested")

        # Test 4: 限额检查
        can_trade, reason = manager.check_trade_limit(100, "BUY")
        print(f"[OK] Limit check (100 USDT): {can_trade} - {reason}")

        # Test 5: 时间处理
        current_date = manager.get_current_date()
        next_reset = manager.get_next_reset_time()
        print(f"[OK] Current date: {current_date}")
        print(f"[OK] Next reset: {next_reset.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        return True

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_position_manager():
    """测试仓位管理器集成"""
    print("\n[TEST] Testing position manager integration...")

    try:
        # 模拟交易所适配器
        class MockExchange:
            def fetch_balance(self):
                return {'USDT': {'free': 5000.0}}

            def calculate_position_size(self, usdt_amount, symbol):
                return usdt_amount / 50000  # ��设BTC价格50000

        from src.execution.position_manager import PositionManager

        position_manager = PositionManager(MockExchange())

        # 检查限额状态
        status = position_manager.get_daily_limit_status()
        print(f"[OK] Limit status: enabled={status.get('enabled', False)}")

        # 测试仓位计算
        signal_data = {'signal': 'BUY', 'confidence': 'HIGH'}
        market_data = {
            'symbol': 'BTC/USDT:USDT',
            'price': 50000,
            'technical_data': {'rsi': 45},
            'trend_analysis': {'overall': '震荡上涨'}
        }

        position_size = position_manager.calculate_position_size(signal_data, market_data)
        print(f"[OK] Position size calculated: {position_size:.6f}")

        return True

    except Exception as e:
        print(f"[ERROR] Position manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("[Daily Limit Functionality Test]")
    print("=" * 50)

    tests = [
        ("Basic functionality", test_basic_functionality),
        ("Position manager integration", test_position_manager)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[ERROR] {test_name} test exception: {e}")
            results.append((test_name, False))

    print(f"\n[RESULT] Testing completed!")

    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)

    print(f"[RESULT] Test results: {passed_count}/{total_count} passed")

    print("\nDetailed results:")
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")

    if passed_count == total_count:
        print("\n[SUCCESS] All tests passed!")
    else:
        print(f"\n[PARTIAL] {passed_count}/{total_count} tests passed")

if __name__ == "__main__":
    main()